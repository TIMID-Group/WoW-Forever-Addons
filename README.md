<div align="center">

<a href="https://github.com/TIMID-Group"><img src="https://raw.githubusercontent.com/TIMID-Group/WoW-Forever-Addons/main/media/brand/timid-banner.png" alt="TIMID Group: Technological Integration and Managerial Innovation Department. Connected systems. Better builds." width="100%"></a>

# 🧩 WoW Forever Addons

<sub>by [TIMID Group](https://github.com/TIMID-Group) · connected systems. better builds.</sub>

**Small, focused addons for WoW Forever:** the auction house, professions, fishing and quest clean-up.

[Addons](#-the-addons) · [Install](#-install) · [Let an AI do it](#3-let-an-ai-agent-do-it) · [Updating](#-updating) · [Troubleshooting](#-troubleshooting) · [Bugs and ideas](#-bugs-and-ideas) · [FAQ](#-faq)

</div>

> [!TIP]
> **📣 New: TIMID Group: one button, one panel, one home for every addon.** [Read the announcement, with screenshots](https://github.com/TIMID-Group/WoW-Forever-Addons/discussions/31).

> [!NOTE]
> **The addons are invite only.** Each addon is a private repo and access is per addon: the ones you were given open normally, the rest show a 404 until you're invited. **Want one?** [Request access](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=request_access.yml): tick the addons and submit. **Anyone can [report a problem](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=bug_report.yml) or [suggest an idea](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=feature_request.yml)**, invited or not. This page is public, so requests and reports here can be read by anyone; an access request is removed once it's answered.

## 📚 The addons

| | Addon | What it does | Latest | Command | Access |
| --- | --- | --- | --- | --- | --- |
| 🛠️ | **[Forever Crafting Ledger](https://github.com/TIMID-Group/ForeverCraftingLedger)** | What every recipe of every profession earns: each material from your cheapest vendor or the auction house, the product sold to a vendor or auctioned. Named shopping lists with your own prices. Reads Auctionator's prices. | [1.6.0](https://github.com/TIMID-Group/ForeverCraftingLedger/releases/latest) | `/fcl` | 🔒 invite only ([request](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=request_access.yml)) |
| 🛠️ | **[Forever Fishing Chart](https://github.com/TIMID-Group/ForeverFishingChart)** | Fishing waters on the world map: catches, skill checks and time-of-day rates, plus a fish finder and your own catch log. | [1.6.0](https://github.com/TIMID-Group/ForeverFishingChart/releases/latest) | `/ffc` | 🔒 invite only ([request](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=request_access.yml)) |
| 💰 | **[[classified]](https://github.com/TIMID-Group/[classified])** | Hold a price ceiling on the auction house. Posts your wall when nothing is listed at or below your price, buys what undercuts it, and tracks every session's profit and gold per hour. | [1.7.0](https://github.com/TIMID-Group/[classified]/releases/latest) | `[classified]` | 🔒 invite only ([request](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=request_access.yml)) |
| 📜 | **[Forever Quest Leftovers](https://github.com/TIMID-Group/ForeverQuestLeftovers)** | Looks through your bags and bank for items no quest needs any more, says why, and says what to do with each one. Dungeon keys, attunements and boss summons are listed as worth keeping. It only advises. | [0.10.0](https://github.com/TIMID-Group/ForeverQuestLeftovers/releases/latest) | `/leftovers` | 🔒 invite only ([request](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=request_access.yml)) |
| 🛠️ | **[Forever Workbench](https://github.com/TIMID-Group/ForeverWorkbench)** | Makes the profession window richer. Shows materials on hand and items in bags on every recipe, buys the vendor materials for a recipe while leaving bag space to craft, sells what you crafted, and runs a crafting queue. | [2.2.0](https://github.com/TIMID-Group/ForeverWorkbench/releases/latest) | `/workbench` | 🔒 invite only ([request](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=request_access.yml)) |

Each addon page has the details, commands and a full guide.

## 📦 Install

All three use the same release zip, so you can mix them and switch any time.

| | 1. WowUp | 2. Manual | 3. AI agent |
| --- | --- | --- | --- |
| **Best for** | Set and forget | No extra software | You already use Claude Code |
| **Updates** | Automatic | Download again | Run the prompt again |
| **You need** | [WowUp](https://wowup.io) + a GitHub token | Nothing | Claude Code + the GitHub CLI |

First, **accept your invites**: one per addon, by email or from the banner on each addon's page. They expire after 7 days.

### 1. WowUp (recommended)

1. **Make a GitHub token** (once): [create one here](https://github.com/settings/tokens/new?scopes=repo&description=WowUp%20%28WoW%20Forever%20addons%29). It's pre-filled with the `repo` scope; choose an expiry and press *Generate token*.
   > **Use a classic token.** Fine-grained tokens can't see repos you were invited to as a collaborator, so WowUp would find nothing.
2. In WowUp: **Options → Addons → GitHub Personal Access Token**, paste it.
3. Pick your **WoW Forever** installation at the top (WowUp recognises the `_forever_` folder; if it's missing, add it under *Options → WoW Installations*).
4. **Get Addons → Install from URL**, paste an addon's link, install. Repeat for each:

```text
https://github.com/TIMID-Group/ForeverCraftingLedger
https://github.com/TIMID-Group/ForeverFishingChart
https://github.com/TIMID-Group/[classified]
https://github.com/TIMID-Group/ForeverQuestLeftovers
https://github.com/TIMID-Group/ForeverWorkbench
```

WowUp shows updates from then on.

### 2. Manual

1. On the addon's page, open **Latest release** and download `<Addon>-X.Y.Z-forever.zip` under *Assets* (not *Source code*).
2. Extract it into `World of Warcraft/_forever_/Interface/AddOns/`, giving `AddOns/<Addon>/<Addon>.toc`.
3. Restart the game, or `/reload`.

### 3. Let an AI agent do it

> [!TIP]
> Paste this into **Claude Code** (or another coding agent that can run commands). It installs every addon you have access to; run it again later to update. It needs the [GitHub CLI](https://cli.github.com) logged in as you (`gh auth login`).

```text
Install or update my WoW Forever addons from GitHub: every addon repo I can access in the org (names starting with "Forever").

Context: the addons are private repos in the GitHub org TIMID-Group. Every release has an asset
named <Repo>-<version>-forever.zip that holds one top-level folder <Repo>/ with <Repo>.toc in it.
I can only see the repos I have been invited to.

1. Check the GitHub CLI is installed and logged in (`gh auth status`). If it isn't, stop and tell
   me how to set it up.
2. List the addon repos I can access: `gh repo list TIMID-Group --limit 100 --json name --jq '.[].name'` and keep the names starting with `Forever`.
3. Find my WoW Forever folder: `_forever_` inside my World of Warcraft install (Windows
   default: C:\Program Files (x86)\World of Warcraft\_forever_). If you can't find it, ask me.
   The target is `_forever_/Interface/AddOns/`.
4. For each addon: download the latest release's zip with
   `gh release download --repo TIMID-Group/<Repo> --pattern '*-forever.zip' --dir <a temp folder>`,
   check it contains `<Repo>/<Repo>.toc` at the top, delete the old `AddOns/<Repo>` folder if
   there is one, and extract the new folder in its place.
5. Never touch the `WTF` folder (my settings and history live there) or any other addon.
6. Finish with a table: addon, installed version (the `## Version` line in the .toc), and
   whether it was new, updated or already current. Remind me to type /reload in game, or to
   restart it.
```

## 🧭 The TIMID button

With **two or more** TIMID addons installed, their minimap buttons fold into **one TIMID Group button**, so your minimap stays clean however many you use. With just one, its own button shows as always.

| Do this | To |
| --- | --- |
| **Left-click** the TIMID button | open the TIMID panel beside it: a row per TIMID addon with its icon, name and a live status line |
| **Left-click** a row in the panel | open that addon, as its own button does |
| **Right-click** a row in the panel | open its settings |
| **Hover** a row in the panel | see its usual tooltip |
| **Drag** the TIMID button | move it (one spot for all of them, remembered) |
| Click the TIMID button again, click anywhere else, press **Escape**, or move the mouse away | close the panel |

Each row's status line says what that addon is doing now, for example the crafting queue's step in Workbench, running or paused in [classified], your zone's fishing skill in Fishing Chart, or how many items look left over in Quest Leftovers.

> [!TIP]
> Rather have every button on its own? Untick **TIMID minimap button** on the Housekeeping page of any TIMID addon's settings, right-click the TIMID button twice, or type `/timid separate` (`/timid group` brings the TIMID button back). It is remembered for all of them.

## 🔄 Updating

| If you installed with | To update |
| --- | --- |
| WowUp | It shows the update; press *Update* (or *Update All*). |
| Manual | Delete the old folder, extract the new zip. |
| AI agent | Run the same prompt again. |

Settings are never lost on update. To be emailed about new versions, open an addon's page and choose **Watch → Custom → Releases**.

## 🩺 Troubleshooting

<details>
<summary><b>An addon link shows 404</b></summary>

You're signed out, the invite isn't accepted yet, or you weren't invited to that addon. Ask for access.

</details>

<details>
<summary><b>WowUp says it can't find the addon or a valid release</b></summary>

Check the token is saved in *Options → Addons*, is a **classic** token with `repo`, and hasn't expired. Check you're on the *WoW Forever* installation, not Retail or Classic.

</details>

<details>
<summary><b>The addon isn't in the game's AddOns list</b></summary>

The folder is probably nested (`AddOns/[classified]/[classified]/...`). Move the inner folder up one level so the `.toc` sits directly inside `AddOns/<Addon>/`.

</details>

<details>
<summary><b>It says *out of date*</b></summary>

Tick **Load out of date AddOns** on the AddOns screen at character select.

</details>

<details>
<summary><b>I get a Lua error</b></summary>

Copy the full text (`/console scriptErrors 1` turns the pop-ups on) and [report a problem](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=bug_report.yml).

</details>

<details>
<summary><b>I want to reset an addon's settings</b></summary>

With the game closed, delete `WTF/Account/<account>/SavedVariables/<Addon>.lua`.

</details>

## 💬 Bugs and ideas

[**Report a problem**](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=bug_report.yml) or [**suggest an idea**](https://github.com/TIMID-Group/WoW-Forever-Addons/issues/new?template=feature_request.yml) for any of the addons, here on this page: one place for all of them, open to everyone, invited or not. Reports here are public; the report from the game holds nothing about your character, gold or account.

**From the game, the quick way:**

1. Press the small report button (**!**) beside the gear on the addon's window (right-click it for an idea), or **Report a problem** / **Suggest an idea** on any of its settings pages. The window stays open.
2. A small box shows a link, already selected: press **Ctrl+C**, then paste it into your web browser.
3. The form opens with the addon, where you were and the details from the game (the version, your changed settings and any errors the addon caught) already filled in. Write what happened in the boxes above the details, paste a screenshot with **Ctrl+V** if it helps, and press Submit.

> [!TIP]
> No title needed: each report is labelled and titled with its addon automatically. If a link ever opens with an empty Details box, use **Full report** in that small box (or `/wb report`, `[classified] report` and so on) and paste the text it gives you there.

## ❓ FAQ

**Is any of my game data shared?**  
No. Settings and history stay in your own `WTF` folder. The repos hold only the addons.

**Do I need all of them?**  
No. Each works on its own. Some light up extra features when another is installed; each addon page lists what it works with.

**Which game version?**  
WoW Forever only (the `_forever_` folder). They aren't built for Retail or Classic.

**Can I change the code?**  
Access is read-only. Ideas and bug reports are welcome as issues; if you'd like to send code, ask for write access.

**Why is there one TIMID button instead of five on my minimap?**  
With two or more TIMID addons, their buttons share one TIMID Group button; click it for a panel with all of them. Untick TIMID minimap button on any addon's Housekeeping page to give each its own button again.

<details>
<summary><b>For developers</b></summary>

- One repo per addon, named exactly like the addon folder (the `.toc` must match it).
- Tags are `vX.Y.Z`, equal to `## Version` in the `.toc`. Each release carries `<Addon>-X.Y.Z-forever.zip` and a BigWigs-style `release.json` (flavor `forever`) for addon managers.
- Repo layout: `<Addon>/` is shipped; `tests/` and `scripts/` are not.
- These pages are generated from the `.toc` files and in-addon guides on every release.

</details>

---

<p align="center"><a href="https://github.com/TIMID-Group"><img src="https://raw.githubusercontent.com/TIMID-Group/WoW-Forever-Addons/main/media/brand/timid-footer.png" alt="TIMID Group. Secure by design. Scalable by nature. Driven by data. Built for collaboration." width="100%"></a></p>

<p align="center"><b><a href="https://github.com/TIMID-Group">TIMID Group</a></b> · Technological Integration and Managerial Innovation Department<br><sub>Connected systems. Better builds.</sub></p>

<sub>Generated on every release. Versions above are the latest published.</sub>
