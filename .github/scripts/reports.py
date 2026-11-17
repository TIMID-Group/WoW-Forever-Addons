#!/usr/bin/env python3
"""Rebuild the Reports section of this README from every TIMID addon repo's issues.

Run by .github/workflows/reports.yml every hour (and by hand from the Actions tab). It reads with a
read-only token (the HUB_READ_TOKEN secret), because the addon repos are private, and rewrites only
what sits between <!-- reports:start --> and <!-- reports:end -->.

Which repos count:
  * an addon repo carries the topic "timid-addon"; its name in the list comes from its .toc Title;
  * a repo that also carries the topic "room-404" is classified: its reports are counted under
    Room 404 and never named or linked.
Older reports filed on this hub before each addon had its own forms are listed under their addon by
label, and every other hub issue (except access requests) under TIMID Group.

With PROJECT_TITLE set (and a token that may write org projects), it also adds every issue to that
org project board: open ones land in "Ideas" (a problem in "Planned"), closed ones move to "Released".
Cards you moved yourself are left where you put them, unless their issue closes.
"""
import json
import os
import re
import sys
import urllib.request

API = "https://api.github.com"
GH = "https://github.com"
SHOWN = 20
TIMID = "TIMID Group"
TOKEN = os.environ.get("HUB_READ_TOKEN", "")
ORG = os.environ.get("ORG", "TIMID-Group")
HUB = os.environ.get("HUB", f"{ORG}/WoW-Forever-Addons")
README = os.environ.get("README", "README.md")


def call(url, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
                                          "User-Agent": "timid-reports"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode()), r.headers.get("Link", "")


def pages(url):
    out = []
    while url:
        got, link = call(url)
        out += got
        m = re.search(r'<([^>]+)>;\s*rel="next"', link or "")
        url = m.group(1) if m else None
    return out


def issues(slug):
    got = pages(f"{API}/repos/{slug}/issues?state=all&per_page=100")
    return [{"number": i["number"], "title": i["title"], "state": i["state"].upper(), "url": i["html_url"],
             "closedAt": i.get("closed_at") or "", "labels": [l["name"] for l in i.get("labels", [])],
             "node_id": i["node_id"]}
            for i in got if "pull_request" not in i]


def title_of(slug):
    name = slug.split("/")[1]
    try:
        got, _ = call(f"{API}/repos/{slug}/contents/{name}/{name}.toc")
        import base64
        text = base64.b64decode(got["content"]).decode("utf-8", "replace")
    except Exception:
        return re.sub(r"^Forever", "", name)
    m = re.search(r"^## Title:\s*(.*?)\s*$", text, re.M)
    t = re.sub(r"\|c[0-9a-fA-F]{8}|\|r", "", m.group(1)) if m else name
    t = re.sub(r"^\s*<TIMID>\s*", "", t).strip()
    return re.sub(r"^Forever\s+", "", t)


def done(i):
    return i["state"] == "CLOSED"


def line(i, prefix):
    title = re.sub(r"^#\d+\s*·\s*", "", i["title"].strip())
    m = re.match(r"^([^:]{1,40}):\s+(.+)$", title)
    if prefix and m:
        said, name = m.group(1).strip().lower(), prefix.lower()
        if said in (name, "forever " + name) or name.endswith(" " + said):
            title = m.group(2)[:1].upper() + m.group(2)[1:]
    bug = "bug" in i["labels"] or title.startswith("Problem report")
    title = (title or "(no title)").replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]").replace("<", "&lt;")
    return f"- {'🐞' if bug else '💡'} [{title}]({i['url']}) · #{i['number']}"


def fold(name, items, see_all):
    opened = sorted((i for i in items if not done(i)), key=lambda i: -i["number"])
    closed = sorted((i for i in items if done(i)), key=lambda i: (i["closedAt"], i["number"]), reverse=True)
    out = [f"<details>\n<summary><b>{name}</b> ({len(opened)} open, {len(closed)} done)</summary>\n"]
    shown = (opened + closed)[:SHOWN]
    for head, part in (("Open", [i for i in shown if not done(i)]), ("Done", [i for i in shown if done(i)])):
        if part:
            out.append(f"**{head}**\n")
            out += [line(i, name) for i in part]
            out.append("")
    if not items:
        out.append("Nothing reported yet.\n")
    more = f" (the newest {SHOWN} are above)" if len(items) > SHOWN else ""
    out.append(f"[See all]({see_all}){more}\n")
    out.append("</details>\n")
    return out


def main():
    if not TOKEN:
        print("no HUB_READ_TOKEN: nothing to do")
        return 0
    repos = pages(f"{API}/orgs/{ORG}/repos?per_page=100&type=all")
    addons = sorted((r for r in repos if "timid-addon" in (r.get("topics") or [])), key=lambda r: r["name"])
    secret = [r for r in addons if "room-404" in (r.get("topics") or [])]
    public = [r for r in addons if r not in secret]
    hub_issues = [i for i in issues(HUB) if "access" not in i["labels"]]
    names = {r["full_name"]: title_of(r["full_name"]) for r in public}
    labels = set(names.values())
    out = ["## 🗂️ Reports\n",
           "What has been reported and suggested, per addon: open first, then done. An addon's reports are on its own "
           "page, so its links open for people who have that addon. 🐞 a problem, 💡 an idea.\n"]
    every = []
    for r in sorted(public, key=lambda r: names[r["full_name"]]):
        slug, name = r["full_name"], names[r["full_name"]]
        own = issues(slug)
        older = [i for i in hub_issues if set(i["labels"]) & labels == {name}]
        every += own
        out += fold(name, own + older, f"{GH}/{slug}/issues?q=is%3Aissue")
    timid = [i for i in hub_issues if len(set(i["labels"]) & labels) != 1]
    every += hub_issues
    out += fold(TIMID, timid, f"{GH}/{HUB}/issues?q=is%3Aissue+-label%3Aaccess")
    if secret:
        got = [i for r in secret for i in issues(r["full_name"])]
        every += got
        out.append(f"🚪 **Room 404** ({sum(1 for i in got if not done(i))} open, {sum(1 for i in got if done(i))} done)\n")
    text = open(README, encoding="utf-8").read()
    start, end = "<!-- reports:start -->\n", "<!-- reports:end -->"
    a, b = text.find(start), text.find(end)
    if a < 0 or b < 0:
        print("no reports marks in the README: nothing written")
    else:
        new = text[:a + len(start)] + "\n" + "\n".join(out) + "\n" + text[b:]
        if new != text:
            open(README, "w", encoding="utf-8").write(new)
            print("reports updated")
        else:
            print("reports unchanged")
    if os.environ.get("PROJECT_TITLE"):
        board(every)
    return 0


def gql(query, **v):
    got, _ = call(f"{API}/graphql", {"query": query, "variables": v})
    if got.get("errors"):
        raise RuntimeError(got["errors"])
    return got["data"]


def board(every):
    title = os.environ["PROJECT_TITLE"]
    d = gql("query($o:String!){organization(login:$o){projectsV2(first:20){nodes{id title field(name:\"Status\"){... on ProjectV2SingleSelectField{id options{id name}}}}}}}", o=ORG)
    proj = next((p for p in d["organization"]["projectsV2"]["nodes"] if p["title"] == title), None)
    if not proj or not proj.get("field"):
        print(f"no project board called {title} with a Status field")
        return
    opt = {o["name"]: o["id"] for o in proj["field"]["options"]}
    have, cursor = {}, None
    while True:
        d = gql("query($p:ID!,$c:String){node(id:$p){... on ProjectV2{items(first:100,after:$c){pageInfo{hasNextPage endCursor} nodes{id content{... on Issue{id}} fieldValueByName(name:\"Status\"){... on ProjectV2ItemFieldSingleSelectValue{name}}}}}}}", p=proj["id"], c=cursor)
        it = d["node"]["items"]
        for n in it["nodes"]:
            if n.get("content"):
                have[n["content"]["id"]] = (n["id"], (n.get("fieldValueByName") or {}).get("name"))
        if not it["pageInfo"]["hasNextPage"]:
            break
        cursor = it["pageInfo"]["endCursor"]

    def status(item, name):
        if name in opt:
            gql("mutation($p:ID!,$i:ID!,$f:ID!,$o:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{singleSelectOptionId:$o}}){projectV2Item{id}}}",
                p=proj["id"], i=item, f=proj["field"]["id"], o=opt[name])

    added = moved = 0
    for i in every:
        if i["node_id"] not in have:
            if done(i):
                continue                      # old closed issues stay off the board
            item = gql("mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}",
                       p=proj["id"], c=i["node_id"])["addProjectV2ItemById"]["item"]["id"]
            status(item, "Planned" if "bug" in i["labels"] else "Ideas")
            added += 1
        else:
            item, now = have[i["node_id"]]
            if done(i) and now != "Released":
                status(item, "Released")
                moved += 1
    print(f"board: {added} added, {moved} moved to Released")


if __name__ == "__main__":
    sys.exit(main())
