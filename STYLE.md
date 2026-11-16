# House style for the Forever addons

How every addon in this family looks, behaves and takes reports, so a player who knows one knows them
all. **Forever Workbench 1.3.0 is the reference implementation**: when this page and Workbench
disagree, Workbench wins and this page gets fixed.

Reference files (in `TIMID-Group/ForeverWorkbench`, folder `ForeverWorkbench/`):

| What | File |
|---|---|
| Settings declared once: sections, defaults, checks | `Core.lua` (`ns.SECTIONS`, `ns.SETTINGS`, `ns.WHATS_NEW`, `ns.REPORT_URL`) |
| Front page, sidebar pages, Housekeeping, opening a page | `Libs/ForeverKit/ForeverKit.lua`, called from `Options.lua` |
| Report window | `Libs/ForeverKit/ForeverKit.lua`, called from `UI/Report.lua` |
| Drop-down and the other widgets | `Libs/ForeverKit/ForeverKit.lua` (`Kit.Dropdown`) |
| Tests for all of the above | `tests/spec_y_pages.lua`, `tests/spec_h_settings.lua` |

## 1. Settings live in the game's own settings window

Options, AddOns, *Addon Name*. Never a separate options window of our own. `/<cmd>` with nothing
after it opens the front page, unless the addon has a main window of its own ([classified], Quest
Leftovers): then plain `/<cmd>` opens that window, and `/<cmd> settings` opens the front page.

### ForeverKit draws every page and every report window

The pages and the report window are not written by each addon: they are drawn by **ForeverKit**,
one library every Forever addon carries, so they cannot drift apart. The master copy is
`release-kit/ForeverKit/ForeverKit.lua`; each addon ships an identical copy at
`Libs\ForeverKit\ForeverKit.lua`, listed in its `.toc` after the other libraries. It registers with
LibStub as `ForeverKit-1.0` with a whole-number minor, so the game keeps the newest copy loaded and
every addon draws with it. Its API only grows: a newer minor keeps every older call working. Each
addon's tests check that its copy is byte for byte the master. Every measure a page uses (the
control column, the row height, the button height, heading spacing) is in one table, `Kit.LAYOUT`.

- `Kit:NewOptions(spec)` returns an object with `:Build()`, `:Open(pageKey)`, `:Refresh()` and the
  tables `.rows`, `.pages`, `.buttons` (aliased to `ns.optionRows`, `ns.optionPages`,
  `ns.optionButtons`). The spec: `name`, `version`, `icon`, `short`, `command`, `intro`; `sections`
  ({ key, title, desc, help }); `settings` (the declared list: key, section, group, kind bool,
  choice, int, number, money or color, default, label, tip, min, max, unit, needs, requires,
  requiresFor, hidden, inline, sound, color, test); `get(key)`, `set(key, value)` returning ok and
  why, `reset(section or nil)`, `text(def, value)`, `enabled(def)`; `worksWith` (and `worksWithNote`,
  more words for an addon's line, since minor 2); `gettingStarted`
  and `whatsNew` lines; `housekeeping` ({ group, key, label, question, act, tip, line });
  `frontButtons` (the addon's own buttons at the top right of the front page); `extras` (something
  drawn under one setting's row); `report(kind, ctx)`, `test(kind)`, `clicked(def, value)` (a click
  sound, since minor 3), `print`, `guard`.
- `Kit:NewReport(spec)` returns `:Show(kind, ctx)`, `:Text(kind, ctx)` and (since minor 6)
  `:Link(kind, ctx)`, the form's link with the whole report in it (see section 2), and `:Pop(kind,
  ctx, button)`, the small box with that link. The spec: `name`, `short`, `addon`, `version`,
  `frameName`, `urls`, `settings`, `get`, `text`, and `details(kind, ctx)`, the addon's own lines
  (its error journal and debug lines), and `scrub(text)`, which takes anything personal out of the
  finished text (since minor 3); `command` ("/wb", named in a trimmed link's note) and
  `items(kind, ctx)` (lines about the things the addon looked at, trimmed after the debug lines)
  since minor 6. The settings spec's `reportLink` (the report, or a function returning it) makes
  the pages' report buttons give that small box too.
- The widgets are exported for the addon's own windows: `Kit.Button`, `Check`, `Edit`, `Dropdown`,
  `ColorSwatch`, `ConfirmButton`, `Tip`, `Heading`, `Words`, `Scroll`, `SetEnabled`.
- The way to the settings from an addon's own windows (since minor 5): `Kit.GearButton(parent,
  openSettings, env, opts)`, a 16 by 16 gear with the game's highlight and the tooltip "Settings" /
  "Opens <addon>'s settings. Right-clicking <icon> does the same."; `Kit.TitleGear(frame,
  openSettings, env, opts)`, that gear just left of the frame's close button, level with it;
  `Kit.SettingsOnRightClick(widget, openSettings, env, opts)`, a right-click on the widget opens the
  settings while its left-click keeps working, and its tooltip gains "Right-click: settings" (a
  picture or a line of words gets a clear frame over it that takes only the right-click); and
  `Kit.ClickHints(tt, what, drag)`, the lines "Left-click: <what>", "Right-click: settings" and
  "Drag: move this button" for a minimap button and an addon-menu entry. `opts` is the addon's name
  or { addon, icon, title, body, close, window }.
- The TIMID button (since minor 9): each addon calls `Kit.JoinLauncher({ addon, name, icon,
  dataObject, iconName, db, status })` once its LibDataBroker object and LibDBIcon button exist (`db`
  is a table in its saved variables, `ns.db.timid`), and `Kit.RefreshLauncher()` after it shows or
  hides its own button. With two or more members the kit registers one LibDBIcon button, "TIMID
  Group", with the TIMID logo, and hides the members' buttons (never their saved `hide`). Since minor
  11 a left-click opens the TIMID panel (the ring of minor 9 and 10 is gone): a small dark panel
  beside the button, with an orange edge and line under a "TIMID Group" header with the logo, one row
  per member in name order (its icon, its name in gold, its status in grey under the name, lit on
  hover) and the foot line "Left-click: open · Right-click: settings" in the hint green. A row's
  left-click and right-click are the member's own `dataObject.OnClick` (and close the panel); hovering
  shows the member's own `OnTooltipShow` beside the panel, without the drag line. The panel opens on
  the side of the button towards the middle of the screen, anchored to it and never clamped, so it
  never covers the button; a second click, Escape, a press anywhere else, or the mouse away from the
  panel and button for 0.6 seconds closes it. `status` is optional: a function returning a few words
  ("queue: step 2 of 3", "paused", "3 left over"), called guarded about once a second while the panel
  is open and cut with "..." to fit, so it must only read state the addon already has, never scan;
  nil or an error shows nothing. `Kit.OpenLauncherRing` and `Kit.CloseLauncherRing` are kept as
  aliases of `Kit.OpenLauncherPanel` and `Kit.CloseLauncherPanel`. Two right-clicks on the button
  (or `/timid separate`) show the buttons separately again; `/timid group` groups them. The state (grouped, the TIMID button's spot, when it changed) is read from the
  newest member db and written to all. Every addon puts `Kit.LauncherHousekeeping(function() return
  ns.db.timid end)` last in its `housekeeping` list: the tick "Group the TIMID addons' buttons into
  one" under TIMID minimap button. A housekeeping item may be such a tick since minor 9: `{ group,
  key, kind = "check", label, get, set, tip, line, default }`.
- The TIMID Group window (since minor 12): one window for the whole family, built once by the newest
  kit loaded (`ForeverKitTIMIDWindow`, `Kit.OpenTIMIDWindow()`), with the panel's look (orange edge,
  dark background). Header: the TIMID logo, "TIMID Group", the tagline in TIMID orange (`e8661c`) and
  "Technological Integration and Managerial Innovation Department" in grey over an orange line. Then
  one row per joined addon in name order (icon, name in gold, .toc version in grey, `status` under
  them), behaving exactly like the panel's rows; Report a problem and Suggest an idea for every TIMID
  addon at once (Addon = TIMID Group; details: the client, the kit minor, one line per addon, never
  trimmed, no settings lines); the hub address in a copy box; and the credits line. It opens from a
  click on the panel's "TIMID Group" header or `/timid` alone; `/timid group`, `separate`,
  `settings`, `report` and `idea` remain. Escape or its X closes it; its position is not saved.
- TIMID Group in the game's Settings (since minor 12): with two or more TIMID addons enabled and one
  shared kit (LibStub), the first addon to build its settings registers "TIMID Group" in the AddOns
  list, whose page is the window's view, and every TIMID addon's front page goes under it with its own
  pages under that. With one TIMID addon it keeps its own top-level entry, as before.

### Every page starts with the same header

Every page, the front page and the pages under it, starts with the same header band: the addon's
icon (32), its name in the large font and its version in grey, always in the same spot, so a player
always sees which addon they are in. A page under the front page then shows where it is: a
breadcrumb, "Settings » <page>", in the larger gold, with **All settings** (back to the front page)
and **Reset this page** at the right of that line. Then the page's two lines on its feature, then its
content, then its Help section.

### The front page

The addon's own entry in the sidebar. Top to bottom:

1. **The header band**: the icon, the name and the version in grey, as on every page.
2. **One line on what the addon does**, in plain words.
3. **Getting started**: three or four numbered steps that take a new player from nothing to the
   addon doing its job. Name buttons and tick boxes exactly as they appear, in gold
   (`|cffffd100Name|r`).
4. **Settings**: one row per sidebar page: an **Open** button, the page title in gold, and one line
   on what that page holds. The last row is Housekeeping.
5. **Help**: **Report a problem** and **Suggest an idea** buttons, and where to find the commands
   (`/<cmd> help`).
6. **Works with**: a heading, then one line per addon it talks to: a ready or not-ready check mark,
   the name, "(not installed)" when missing, and what that addon adds here ("auction prices in the
   Create tooltip, and Deep search"). Read each time the page shows. Declared once, as
   `ns.WORKS_WITH = { { name, found = function, adds } }`, with `ns.Found(name)`.
7. **What's new**: the last three versions, one line each, newest first (`ns.WHATS_NEW`).

### Sidebar pages

- **When:** an addon with more than about 15 settings gets one sidebar page per section, registered
  with `Settings.RegisterCanvasLayoutSubcategory` under the front page (as Questie and Auctionator
  do). Fewer than that can stay on the front page under a Settings heading.
- **Housekeeping is always the last page**: Reset all settings, and every button that forgets or
  deletes saved data, each with a line saying what it does.
- **Each page opens with:** the header band and the breadcrumb, with **All settings** and **Reset
  this page** at its right, then a description of the feature in two short lines at most (`help` on
  the section: what the feature does and the one thing to know; the front page's Open row keeps the
  one-line `desc`).
- **Every page is styled like the front page.** Its settings sit under gold section headings with a
  rule under them (the front page's `heading`), grouped by what they are about: each setting
  declares `group = "Recipe rows"` and a page with one group heads it "Settings". Housekeeping is
  grouped the same way (Settings, Saved data, and so on).
- **Every page ends with a Help section,** never a small link: the heading "Help with <page>", the
  same **Report a problem** and **Suggest an idea** buttons as the front page, and one line saying
  the page's settings go in with the report. The buttons give the prefilled link in the small
  box under the button pressed, with `{ area = page title, section = key }` (see section 2).
  Housekeeping has one too.
- **Rows:** a tick box or control per setting, its label (12 px, from 24, clicking it counts for a
  tick box), and a tooltip with what On and Off do, the allowed range and the default. Controls sit
  in one column at 370; every choice is a drop-down; a unit sits after its box; rows are 26 apart;
  a greyed-out setting fades its label and control once, never the row on top.
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
- **A setting that needs another addon** says so: `requires = "<name in WORKS_WITH>"` (and
  `requiresFor = "the auction house price"` when only part of it does). Its tooltip ends with
  "Uses X: installed." in green or "Needs X, which is not installed." in orange, worked out each
  time it shows.

### Telling players about other addons

Inform, never advertise. Another addon is mentioned only on the front page's Works with, in the
tooltip of a setting that uses it, in the guide's "What it needs", and as an optional dependency
in `.pkgmeta` (so CurseForge's page and app offer it). Never in chat, at login, in a popup, or in
an ordinary tooltip.

## 1b. Windows

Every window an addon opens on its own (a main window such as [classified]'s, the ledger, the fish
finder or the leftovers list, and every report window) behaves like the game's own windows:

- **The game's frame where it fits.** PortraitFrameTemplate (title bar, round portrait with the
  addon's icon, close button), falling back to BasicFrameTemplateWithInset, then a plain frame, on
  clients that lack it. The title is the name plus the version in grey. An addon whose window is
  deliberately its own look keeps it ([classified], by the owner's choice), as long as the rules below
  hold.
- **The game's layer.** Strata MEDIUM, `SetToplevel(true)`, and a raise when opened and when
  clicked, so the window used last is on top and other windows can come in front of it. Never
  HIGH or DIALOG for a window; only drop-down menus, which close on any click elsewhere, sit above.
- **One OnShow.** A later `SetScript("OnShow")` wipes an earlier `HookScript`; keep a single
  handler, or hook after the last SetScript.
- **Moving.** Draggable by its body or title, clamped to the screen, its position remembered per
  account, and a "Reset window position" button on the Housekeeping page.
- **Closing.** Escape closes it (UISpecialFrames), the close button says so in its tooltip.
- **Settings.** Settings are one click away from every addon window: a gear left of the close
  button, and right-click on the addon's own icon (portrait, minimap button, addon menu). Tooltips
  say so. In Workbench, the profession icon is the addon's icon (click toggles the strip, right-click
  settings), with the gear left of the close button like everywhere else. The gear replaces any
  Settings or Options button a window had: no window carries one of its own. [classified], which keeps
  its own look and has no portrait, takes the right-click on its title. Use `Kit.TitleGear` and
  `Kit.SettingsOnRightClick`.
- **Reporting.** A report button sits just left of the gear, the same 16 by 16, with its own
  symbol (the game's red exclamation, `HelpIcon-ReportAbuse`, or the next one the client has; a red
  "!" when it has none). Its tooltip: "Report a problem", "Gives you a link that opens the report
  form already filled in. Your window stays open, so you can take a screenshot." and, in green,
  "Right-click: suggest an idea". A click opens a small box (320 by 90) under it holding the
  prefilled link, already selected (Ctrl+C), the line "Ctrl+C, then paste it in your browser", a
  Problem / Idea switch, Full report (the report window) and an X; Escape closes it. The window
  stays open and uncovered, so the player pastes the link and then takes the screenshot. The box
  is the one thing besides a drop-down that sits on DIALOG, so a click in the window never hides
  it; it goes when its window closes. Its area is the window's name ("Profession window", "Fish
  finder"). Use `Kit.TitleReport(frame, function() return ns.report end, env, { area = ... })`
  after `Kit.TitleGear`. It adds a way in; every other one stays.
- **Sounds.** The game's IG_CHARACTER_INFO_OPEN and IG_CHARACTER_INFO_CLOSE.
- **Ways in.** A key binding to toggle it (Bindings.xml, category = the addon's name, plain-words
  name), the game's addon menu by the minimap (## AddonCompartmentFunc), and the minimap button.
  On both, a left-click does the addon's main thing (its window; the profession window for
  Workbench) and a right-click opens the settings. Their tooltips have one useful line, then
  `Kit.ClickHints`: "Left-click: ...", "Right-click: settings" and, on the minimap button only,
  "Drag: move this button", in the game's green.
- **Lists.** The game's scroll bar (ScrollFrameTemplate) that hides itself when everything fits.
- **Parts of the game's own windows** (Workbench's strip and pages) live inside those windows and
  follow them; they do not need their own layer rules.

## 2. Reports and ideas

Addons cannot reach the internet, so a report is a link the player copies and pastes: one copy,
one paste. The link opens exactly the right form with the Addon, Area and **Details from the game**
boxes already filled in, and there is nothing to title. The form asks the player's own questions in
ordinary boxes above the Details box (ForeverKit minor 7): the link never fills those.

- **The buttons and commands:** the report button beside every window's gear (section 1b), and
  **Report a problem** and **Suggest an idea** on the front page and in each page's Help section,
  give the prefilled link in a small box under the button. `/<cmd> report`, `/<cmd> idea` and the
  box's **Full report** open the report window. A **Problem / Idea** switch at its top right
  changes kind without losing the page. It shows three numbered steps:
  1. Copy this link (it is already selected: press Ctrl+C) and open it in your web browser. The
     details from the game are already filled in.
  2. Write what happened (or your idea) in the boxes above them. Paste a screenshot into the
     Screenshots box if it helps.
  3. Press Submit. You need a free GitHub account; reports there are public.

  Under them sits the report text itself, "If the page opens empty, copy this too and paste it in."
  The link box takes a link of any length (`SetMaxLetters(0)`).
- **The prefilled link.** GitHub fills a form field from the query parameter named after its `id`:
  `&report=` on the problem form, `&idea=` on the idea form, after `&area=`. In the report, a space
  is `+`, a newline `%0A`, and every other character but letters, digits and `- . _ ~` is
  percent-encoded byte by byte (`#` as `%23`, `+` as `%2B`, an accented letter as its UTF-8 bytes).
  Its rule lines are 32 wide, not 64, so more fits.
- **The 6,000-character budget.** GitHub takes a link of 6,000 characters and fails above about
  6,500, so the whole link stays at or under 6,000 (`Kit.LINK_BUDGET`). A longer report is trimmed
  in this order: the other addons list, then debug and probe lines, then item or detail lines, then
  settings, and one line under the version says so: "Trimmed to fit the link: other addons list.
  /<cmd> report shows the full report." The questions, the version and client line and the problems
  caught are never trimmed.
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
- **From a settings page** (`{ area = page title, section = key }`), the
  details start with `Area: <page>` and `Settings on this page:` (every setting there, changed or
  not), and the link gains `&area=<page>`, which fills in the form's Area box.
- **Never in a report:** the character's name, realm, guild, gold, account, or exact map position.
  A test checks this.
- **Every addon keeps an error journal:** errors caught by its guard are printed once and kept in
  its saved variables (up to 40), so a report can include them.

**The GitHub side** is generated by `docs.py` for every repo:

- **Two forms:** Report a problem (label `bug`) and Suggest an idea (label `enhancement`).
- **An Area box,** filled in by the link when the report comes from a settings page.
- **One required paste box** each, shown as plain text, with the CAPS skeleton as a faint placeholder
  for anyone not in the game, and an optional box for screenshots.
- **No title to write:** each form fills in its own ("Problem report", "Idea"). The owner renames
  issues later if ever; the issue number is the real identifier.
- **No form-less issues:** blank issues are off.
- **Links point at the forms:** README links go straight to a form, never the chooser.

- **Filing.** Every report, idea and owner request made in chat becomes an issue on the hub, with
  its addon's label (added by the File reports workflow) and, for planned work, a milestone. A fix
  is answered on its issue, the issue is closed with the `fixed` label, the release notes link the
  issue, the CHANGELOG bullet ends "(#N on the WoW Forever Addons page)", and a line goes into
  `forever-admin/reports-log.csv`. Design decisions also go into the design doc's Decisions log.

## 2b. TIMID Group branding

Every Forever addon is a TIMID Group addon, and says so everywhere:

- **In the game:** ForeverKit (minor 8) draws the TIMID logo (`Libs/ForeverKit/timid.tga`, copied by
  `forever kit`) and "A TIMID Group addon · Connected systems. Better builds." at the foot of every
  settings front page. Each addon passes `addon = ADDON` in its options spec so the logo can be found.
- **On GitHub:** `docs.py` puts the TIMID logo, a "built by TIMID Group" badge and the values-strip
  footer on every addon page and the hub, and the logo on every form; `forever` adds the footer to
  every release's notes. Colours: orange `#e8661c`, navy `#0b1321`. Tagline: "Connected systems.
  Better builds." Brand pictures live in the hub's `media/brand/`.
- **Words:** "TIMID Group" in full the first time on a page; never an em dash in the brand lines.

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
  `## IconTexture`. Since #18 every TIMID addon is grouped on the game's AddOn List as DBM does it:
  `## Category: TIMID Group`, the old category kept for the docs as `## X-Category` (Professions,
  Auctions or Quests), and a tagged title, `## Title: |cffffd100<|r|cffe8661cTIMID|r|cffffd100>|r
  |cffffffffForever Workbench|r` with the addon's own full name (no `Title-enUS`). Add `## X-Curse-Project-ID` and `## X-Wago-ID` the day the project is created
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
