<div align="center">

# 🧩 WoW Forever Addons

**Small, focused addons for WoW Forever:** the auction house, professions, fishing and quest clean-up.

[Addons](#-the-addons) · [Install](#-install) · [Let an AI do it](#3-let-an-ai-agent-do-it) · [Updating](#-updating) · [Troubleshooting](#-troubleshooting) · [Bugs and ideas](#-bugs-and-ideas) · [FAQ](#-faq)

</div>

> [!NOTE]
> **You're here because you were invited.** Each addon is a private repo and access is per addon: the ones you were given open normally, the rest show a 404. Want another? Just ask.

## 📚 The addons

| | Addon | What it does | Latest | Command |
| --- | --- | --- | --- | --- |
| 🛠️ | **[Forever Crafting Ledger](https://github.com/TIMID-Group/ForeverCraftingLedger)** | What every recipe of every profession earns: each material from your cheapest vendor or the auction house, the product sold to a vendor or auctioned. Named shopping lists with your own prices. Reads Auctionator's prices. | [1.1.0](https://github.com/TIMID-Group/ForeverCraftingLedger/releases/latest) | `/fcl` |
| 🛠️ | **[Forever Fishing Chart](https://github.com/TIMID-Group/ForeverFishingChart)** | Fishing waters on the world map: catches, skill checks and time-of-day rates, plus a fish finder and your own catch log. | [1.1.0](https://github.com/TIMID-Group/ForeverFishingChart/releases/latest) | `/ffc` |
| 💰 | **[[classified]](https://github.com/TIMID-Group/[classified])** | Hold a price ceiling on the auction house. Posts your wall when nothing is listed at or below your price, buys what undercuts it, and tracks every session's profit and gold per hour. | [1.1.0](https://github.com/TIMID-Group/[classified]/releases/latest) | `[classified]` |
| 📜 | **[Forever Quest Leftovers](https://github.com/TIMID-Group/ForeverQuestLeftovers)** | Looks through your bags and bank for items no quest needs any more, says why, and says what to do with each one. It only advises. It never sells or destroys anything. | [0.2.0](https://github.com/TIMID-Group/ForeverQuestLeftovers/releases/latest) | `/leftovers` |
| 🛠️ | **[Forever Workbench](https://github.com/TIMID-Group/ForeverWorkbench)** | Makes the profession window richer. Shows materials on hand and items in bags on every recipe, buys the vendor materials for a recipe while leaving bag space to craft, and sells what you crafted. | [1.3.1](https://github.com/TIMID-Group/ForeverWorkbench/releases/latest) | `/workbench` |

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

Copy the full text (`/console scriptErrors 1` turns the pop-ups on) and file a bug on that addon's page.

</details>

<details>
<summary><b>I want to reset an addon's settings</b></summary>

With the game closed, delete `WTF/Account/<account>/SavedVariables/<Addon>.lua`.

</details>

## 💬 Bugs and ideas

Open the addon's page → **Issues → New issue** and pick *Bug report* or *Idea*. The form asks for what's needed (version, what happened, any Lua error).

## ❓ FAQ

**Is any of my game data shared?**  
No. Settings and history stay in your own `WTF` folder. The repos hold only the addons.

**Do I need all of them?**  
No. Each works on its own. Some light up extra features when another is installed; each addon page lists what it works with.

**Which game version?**  
WoW Forever only (the `_forever_` folder). They aren't built for Retail or Classic.

**Can I change the code?**  
Access is read-only. Ideas and bug reports are welcome as issues; if you'd like to send code, ask for write access.

<details>
<summary><b>For developers</b></summary>

- One repo per addon, named exactly like the addon folder (the `.toc` must match it).
- Tags are `vX.Y.Z`, equal to `## Version` in the `.toc`. Each release carries `<Addon>-X.Y.Z-forever.zip` and a BigWigs-style `release.json` (flavor `forever`) for addon managers.
- Repo layout: `<Addon>/` is shipped; `tests/` and `scripts/` are not.
- These pages are generated from the `.toc` files and in-addon guides on every release.

</details>

---

<sub>Generated on every release. Versions above are the latest published.</sub>
