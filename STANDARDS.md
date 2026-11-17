# TIMID engineering standard

Every TIMID addon follows one standard, at every level: the suite as a whole, each addon, each module, each function. Each level follows the rules that apply to it, front end (what players see) and back end (logic, data, APIs) alike. A release needs every level to pass.

## The documents

| Concern | Document | In short |
|---|---|---|
| Look, feel, words | [STYLE.md](STYLE.md) | settings in the game's window, house windows and popups, plain words, works alone and richer together |
| Code structure | [ENGINEERING.md](ENGINEERING.md) | one job per module, private by default, one-way dependencies, APIs between addons, one source of truth |
| Performance | [PERFORMANCE.md](PERFORMANCE.md) | the player never feels the addons: budgets, event-driven, spread out, stable memory, paper first |
| Security and safety | this file, section 3 | privacy, untrusted input, combat safety, saved data |
| Testing | this file, section 4 | what each level is tested with |

## 1. The levels

| Level | What it is | Rules that apply |
|---|---|---|
| **Suite** | all TIMID addons together, the kit, the hub | one kit for shared pieces; versioned APIs between addons with contract tests; one brand and one look; one reporting system; together inside the frame budget |
| **Addon** | one addon | works alone; settings, report window, TIMID panel row, help and What's new per the style guide; login cost and saved-data size reported; its own tests and changelog |
| **Module** | one file | one job; a small public table; one-way dependencies; no other addon's internals; about 800 lines at most |
| **Function** | one function | one job; deciding apart from doing; inputs as arguments; no allocation or global lookups in hot paths; its cost growth known; guarded at the edge |

## 2. The concerns at each level

| | Suite | Addon | Module | Function |
|---|---|---|---|---|
| **Front end** | one brand, one look, popups behave the same | style guide pages, words, defaults quiet | view apart from model | a redraw only draws |
| **Structure** | kit shared, APIs only | modules with one job | private by default | one job |
| **Performance** | 1 to 2 ms together in a busy frame | its own budget, coalesced events | caches with rules, pools | no hot-path garbage, known Big-O |
| **Correctness** | contract tests between addons | before-and-after tests | one source of truth | unit tests, every fix has its test |
| **Security** | no secrets, nothing classified in public | private data stays local | imported text validated | game calls guarded |
| **Data** | API versions | saved data versioned, capped, migrated once | one owner per piece of state | no hidden side effects |

## 3. Security and safety

- **Privacy.** Nothing about a player's character, gold or account leaves the game except what they choose to paste. Reports carry no character names. Saved data stays in the player's own files.
- **Nothing classified in public.** Classified addons are never named on any public page, file or post.
- **Untrusted input.** Imported text (queue lists, shopping lists) is parsed defensively: size limits, known fields only, unknown lines reported and skipped, never run as code.
- **Combat and taint safety.** Nothing touches protected frames or actions in combat; such work waits until combat ends. Addons never write to the game's own tables in ways that taint them.
- **Saved data.** Every saved table has a version, a size cap and a one-time migration for old shapes. Never change a player's saved settings except through a marked one-time move.
- **No secrets** in any repo, commit or post.

## 4. Testing

| Level | Tested with |
|---|---|
| Function | unit tests for every public function; every bug fix adds the test that would have caught it |
| Module | its public table tested alone with exact inputs |
| Addon | the addon's suite; before-and-after (golden) tests of its engines; perf workloads with budgets; the static checker |
| Suite | contract tests between addons (what one sends, the other accepts); end-to-end flows; a short in-game checklist per release; the in-game `/timid perf` baseline |

## 5. Conformance

- **A scorecard per addon** lists every rule at every level as pass, fail or not applicable, with file and line. A release needs no fails, or each one owned by an issue.
- **Reviews** use the checklists in each document. A change that makes any level worse is sent back.
- **Automated where possible:** the test suites, the static checker (hot paths, size, coupling), perf budgets and contract tests run with every change.
