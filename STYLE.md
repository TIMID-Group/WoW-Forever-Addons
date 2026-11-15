# House style for the Forever addons

How every addon in this family looks, behaves and takes reports, so a player who knows one knows them
all. **Forever Workbench 1.3.0 is the reference implementation**: when this page and Workbench
disagree, Workbench wins and this page gets fixed.

Reference files (in `TIMID-Group/ForeverWorkbench`, folder `ForeverWorkbench/`):

| What | File |
|---|---|
| Settings declared once: sections, defaults, checks | `Core.lua` (`ns.SECTIONS`, `ns.SETTINGS`, `ns.WHATS_NEW`, `ns.REPORT_URL`) |
| Front page, sidebar pages, Housekeeping, opening a page | `Options.lua` |
| Report window | `UI/Report.lua` |
| Drop-down widget | `UI/Widgets.lua` (`W.Dropdown`) |
| Tests for all of the above | `tests/spec_y_pages.lua`, `tests/spec_h_settings.lua` |

## 1. Settings live in the game's own settings window

Options, AddOns, *Addon Name*. Never a separate options window of our own. `/<cmd>` with nothing
after it opens the front page, unless the addon has a main window of its own ([classified], Quest
Leftovers): then plain `/<cmd>` opens that window, and `/<cmd> settings` opens the front page.

### The front page

The addon's own entry in the sidebar. Top to bottom:

1. **Title and version** (the version small and grey, as `ns.title`).
2. **One line on what the addon does**, in plain words.
3. **Getting started**: three or four numbered steps that take a new player from nothing to the
   addon doing its job. Name buttons and tick boxes exactly as they appear, in gold
   (`|cffffd100Name|r`).
4. **Settings**: one row per sidebar page: an **Open** button, the page title in gold, and one line
   on what that page holds. The last row is Housekeeping.
5. **Help**: **Report a problem** and **Suggest an idea** buttons, and where to find the commands
   (`/<cmd> help`).
6. **Works with**: the addons it talks to, each marked found or not installed, read each time the
   page shows.
7. **What's new**: the last three versions, one line each, newest first (`ns.WHATS_NEW`).

### Sidebar pages

- **When:** an addon with more than about 15 settings gets one sidebar page per section, registered
  with `Settings.RegisterCanvasLayoutSubcategory` under the front page (as Questie and Auctionator
  do). Fewer than that can stay on the front page under a Settings heading.
- **Housekeeping is always the last page**: Reset all settings, and every button that forgets or
  deletes saved data, each with a line saying what it does.
- **Each page opens with:** its title and a one-line description (the same line the front page
  shows), then **Reset this page** at the top right.
- **Rows:** a tick box or control per setting, its label, and a tooltip with what On and Off do,
  the allowed range and the default.
- **Old clients:** fall back to `InterfaceOptions_AddCategory` with `panel.parent` set.
- **Opening a page from a button:** use `C_SettingsUtil.OpenSettingsPanel` through
  `securecallfunction` when the client has it (out of combat), else `Settings.OpenToCategory`.
  Calling the Lua opener directly can draw a blocked-action message on newer clients.
- **Never change a setting's key, section key or default** when moving it between pages: saved
  settings are kept by key.

### Settings rules

- **Declared once:** every setting is declared once, in one list, with key, section, kind, default,
  label and tip. The pages, the resets and `/<cmd> set` are built from that list.
- **Light defaults for a fresh install:** nothing chatty, noisy or automatic is on until the player
  turns it on. An existing install keeps every value it has; a new setting gets its default.
- **Main switches grey out what hangs off them**, but never forget the choices under them.
- **Every reset or delete takes two presses**, and says what it will do on the first.
- **Sounds:** every sound has a drop-down to pick it (picking plays it) and a **Test** button. Play
  on the Master channel. Each choice falls back to another sound if this client lacks the file.

## 2. Reports and ideas

Addons cannot reach the internet, so a report is text the player copies and pastes. Make every step
deliberate: one link that opens exactly the right form, one block of text, nothing to title.

- **The buttons and commands:** **Report a problem** and **Suggest an idea** on the front page, and
  `/<cmd> report` and `/<cmd> idea`, open a window with three numbered steps:
  1. Copy this link and open it in your web browser (with a Select button beside the link box).
  2. Copy everything in the box below (already selected: Ctrl+C) and paste it into the form.
  3. Fill in the parts marked WRITE HERE and press Submit. There is no title to write.
- **The link opens one form, never a chooser:** `ns.REPORT_URLS.problem` is
  `.../issues/new?template=bug_report.yml`, `ns.REPORT_URLS.idea` is `...?template=feature_request.yml`.
  Never `issues/new/choose`.
- **The report text** is plain text in capital sections, the way the big addons (RestedXP) do it:

  ```
  ################################################################
  ##  FOREVER WORKBENCH: PROBLEM REPORT
  ##  Fill in the parts marked WRITE HERE, then press Submit.
  ################################################################

  ----------------------------------------------------------------
    1. WHAT HAPPENED?
  ----------------------------------------------------------------
  WRITE HERE:
  ...  2. WHAT DID YOU EXPECT TO HAPPEN?   3. HOW CAN WE MAKE IT HAPPEN AGAIN?

  ################################################################
  ##  DO NOT CHANGE OR REMOVE ANYTHING BELOW THIS LINE.
  ##  Details from the game. Nothing about your character or gold.
  ################################################################
  Version, client and locale, settings changed, problems caught, debug lines, other addons
  ######################### END OF REPORT ########################
  ```

  An idea asks 1. WHAT WOULD HELP? and 2. WHAT ARE YOU TRYING TO DO?, and its details are the
  version, client, changed settings and other addons.
- **Never in a report:** the character's name, realm, guild, gold, account, or exact map position.
  A test checks this.
- **Every addon keeps an error journal:** errors caught by its guard are printed once and kept in
  its saved variables (up to 40), so a report can include them.

**The GitHub side** is generated by `docs.py` for every repo:

- **Two forms:** Report a problem (label `bug`) and Suggest an idea (label `enhancement`).
- **One required paste box** each, shown as plain text, with the CAPS skeleton as a faint placeholder
  for anyone not in the game, and an optional box for screenshots.
- **No title to write:** each form fills in its own ("Problem report", "Idea"). The owner renames
  issues later if ever; the issue number is the real identifier.
- **No form-less issues:** blank issues are off.
- **Links point at the forms:** README links go straight to a form, never the chooser.

## 3. Chat

- **News goes to the shared "Addons" chat tab** (purchases, sales, trophies) and is off by default.
  Each addon offers a Create "Addons" chat button that reuses the tab if another addon made it.
- **Answers to a command or button the player just used** go to the main chat, unless the player
  asks otherwise.
- **Every line starts with the addon's short coloured name.**

## 4. Words

- **Plain words**, no jargon: "bag slots to leave free", not "inventory buffer".
- **Tooltips:** say what On does and what Off does.
- **No em dashes** anywhere: in-game text, guides, commit messages.
- **Every guide has the same sections**, in this order: Install, What it needs, How to use it,
  Settings, Commands, Reporting a problem or an idea, Testing status.

## 5. Releases, and being ready for CurseForge

Every repo carries the release kit, installed and kept in step by `forever kit` from `release-kit/`:

| File | What it is for |
|---|---|
| `CHANGELOG.md` | Every version, newest first, as `## [X.Y.Z] - YYYY-MM-DD` then bullets a player would understand: **a bold one-line summary**, then a sentence of detail. Changed defaults say that existing players keep their values. API changes go under `### For addon authors`. |
| `scripts/changelog.py` | Pulls one version's section out of CHANGELOG.md. |
| `.pkgmeta` | Tells the BigWigs packager to lift `<Addon>/<Addon>` to the top of the zip and to ship `LICENSE`. |
| `.github/workflows/package.yml` | Runs the packager on every tag: always builds the package (kept as the run's artifact), uploads to CurseForge or Wago only once that site's key secret and project ID exist. |
| `LICENSE` | MIT, copyright TIMID Group. A copy also ships inside the addon folder. |

Rules:

- **No notes, no release:** `forever publish` refuses a version without its changelog section, and
  that section becomes the GitHub release notes (and the CurseForge and Wago notes). Write the
  section when the version is bumped.
- **What's new matches the changelog:** the front page's What's new line for a version is the
  summary of its changelog section.
- **The `.toc` carries:** `## Title`, `## Notes`, `## Version` (a literal version, so the installed
  copy shows it), `## Author: TIMID Group`, `## X-License: MIT`, `## X-Website` (the repo), and
  `## IconTexture`. Add `## X-Curse-Project-ID` and `## X-Wago-ID` the day the project is created
  on those sites.
- **Credit what you borrow:** any data or code taken from elsewhere is credited in a `NOTICE.md`
  inside the addon folder, with the source's licence text where it asks for it.
- **Never upload** anything that reads or ships the `WTF` folder.

To list an addon later: create the project on CurseForge, put its ID in the `.toc`, add the
repository secret `CF_API_KEY` (from the CurseForge API tokens page), and publish the next version.

## 6. Tests

Every addon has a test suite against a strict fake of the game client. A change to settings or pages
needs tests that:

- every setting appears on exactly its own section's page;
- every Open button on the front page opens its page;
- Reset this page resets only that page;
- the report holds the version and changed settings, and not the character's name or realm.
