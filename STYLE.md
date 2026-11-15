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
after it opens the front page.

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

Addons cannot reach the internet, so a report is text the player copies and pastes.

- **The buttons and commands:** **Report a problem** and **Suggest an idea** on the front page, and
  `/<cmd> report` and `/<cmd> idea`, open a window with:
  - the address to paste into (`ns.REPORT_URL`, the repo's `issues/new/choose`), in a box of its own
    with a Select button;
  - the report, already selected for Ctrl+C. It is read-only: typing puts the text back.
- **A problem report holds:**
  - a short template at the top (what happened, what you expected, how to make it happen again);
  - then, inside a collapsed `<details>` block: the version, client build and locale, the settings
    changed from their defaults, the problems the addon caught (its error journal), its debug lines,
    and the other loaded addons with their versions.
- **An idea holds** a short template (what would help, what you are trying to do), the version,
  client and changed settings.
- **Never in a report:** the character's name, realm, guild, gold or account. A test checks this.
- **Every addon keeps an error journal:** errors caught by its guard are printed once and kept in
  its saved variables (up to 40), so a report can include them.

The GitHub side is the same for every repo: issue forms for bugs and ideas
(`.github/ISSUE_TEMPLATE/`, generated by `docs.py`), labels `bug` and `enhancement`.

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

## 5. Tests

Every addon has a test suite against a strict fake of the game client. A change to settings or pages
needs tests that:

- every setting appears on exactly its own section's page;
- every Open button on the front page opens its page;
- Reset this page resets only that page;
- the report holds the version and changed settings, and not the character's name or realm.
