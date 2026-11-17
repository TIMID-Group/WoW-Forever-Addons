# TIMID engineering standard

Every TIMID addon follows one standard. **Each kind of element has its own rules** (a loop is judged differently from a variable, a module differently from the suite), and a few rules cut across everything. Each element follows the rules for its kind plus the cross-cutting ones, front end (what players see) and back end (logic, data, APIs) alike. A release needs every element to pass.

## The qualities (ISO/IEC 25010)

"The best" means every addon meets a measurable bar on each software quality. These are the scorecard's columns.

| Quality | Means | Bar |
|---|---|---|
| **Performance efficiency** | fast, light, never felt | within the frame budget (`PERFORMANCE.md`); no checker regressions; saved data and login cost within limits |
| **Functional suitability** | does the right thing every time | before-and-after tests pass; previews and actions share one calculation; every bug has its test |
| **Reliability** | doesn't break; recovers | every failure mode handled (below); no Lua errors in the problem report; state survives a reload or disconnect |
| **Security** | private and safe | section 3 below |
| **Maintainability** | readable, modular, easy to change and test | `ENGINEERING.md`; files under about 800 lines; coupling not rising; public functions tested |
| **Usability** | easy and pleasant | `STYLE.md`; plain words; quiet defaults; every figure explains itself |
| **Compatibility** | plays well with the client and other addons | works alone; guarded API use; other addons only through their APIs |

**Reliability: what can go wrong, handled on purpose.** For every feature, write down and test: the server is slow or says no (a purchase fails, mail is empty or not yet arrived); a window closes mid-action (vendor, mailbox, auction house); the player moves, dies, enters combat or disconnects mid-run; another addon is missing, older or misbehaving; saved data is old, partial or damaged. Each has a defined, tested outcome: wait, retry, pause with a reason, or carry on safely. Never a silent wrong result.

## The lifecycle: every feature, start to finish

| Stage | What happens | Gate before the next stage |
|---|---|---|
| **1. Requirements** | the owner's ask, written as an issue in plain words; questions answered, not assumed | the owner agrees it says what they meant |
| **2. Design** | how it works for the player (`STYLE.md`) and inside (`ENGINEERING.md`): modules, data, APIs; its performance section (data size, Big-O, events, frame budget); its failure modes (reliability) | design reviewed against all seven qualities |
| **3. Implementation** | built to the element rules (section 2c), private by default, one source of truth | the static checker shows nothing worse |
| **4. Verification** | unit, module, contract, before-and-after and end-to-end tests; perf budgets; an independent review against the scorecard | every test green, scorecard green |
| **5. Release** | changelog, guide, version; an in-game checklist played by the owner first; then friends | the owner has played it |
| **6. Operation** | `/timid perf` and the problem reports show how it behaves in real play | real numbers inside the budget |
| **7. Maintenance** | every report becomes an issue; every fix adds its test; the standards themselves improve from what we learn | nothing gets worse over time |

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

## 2b. Rules that cut across everything

- Plain words, no em dashes, no character names, nothing classified in public.
- Works alone, richer together. Quiet by default.
- One source of truth. Every change has its test.

## 2c. Rules by kind of element

Each element follows its own rules. These are the main ones; the documents above have the detail.

**Variables**
- `local` always; a global only for a saved variable or a deliberate public table.
- Names say what the thing is (`freeSlots`, not `n`); booleans read as questions (`isOpen`, `hasMail`); constants in capitals (`MAX_ROUNDS`).
- Smallest scope that works; one meaning per variable; no reuse for something else.
- Units in the name where it matters (`copper`, `seconds`, `ms`).

**Loops**
- Numeric `for i = 1, #t` over arrays; `pairs` only for real maps, and never where the order matters.
- Hoist anything that doesn't change out of the loop (lengths, lookups, global functions as locals).
- No tables, closures or string building inside a hot loop; reuse a scratch table.
- Stop early when the answer is known; never loop inside a loop over the same data when an index would do.
- A loop over something that grows (bags, quests, auctions, queue steps) has a known cost and, if big, runs as a job across frames.

**Functions**
- One job; a name that says it (a verb: `SizeRound`, `TakeMail`).
- Inputs as arguments, results as return values; no hidden side effects.
- Deciding apart from doing: pure logic in one function, game calls in another.
- Short (about 50 lines); early returns over deep nesting.
- Guard game calls once, at the edge.

**Tables and data shapes**
- One shape per kind of record, documented where it is built; no fields that change meaning.
- Arrays and maps kept apart; never mix numeric and named keys in one table.
- Reuse (`wipe`) instead of rebuilding in hot paths.

**Strings and text**
- Player-facing words in one place per module, in plain house words; built once, not per frame.
- Text from outside (imports, chat) is untrusted: limited in size, parsed field by field.

**Events and timers**
- Register only while needed; coalesce bursts; unregister on hide or done.
- No OnUpdate or ticker that runs while nothing happens.

**UI frames**
- Built on first show, pooled and reused; a view only draws a snapshot, it never computes.
- Popups and windows follow the style guide; long lists draw only visible rows.

**Saved data**
- Versioned, capped, migrated once with a mark; never change a player's settings except by a marked one-time move.

**Modules (files)**
- One job, about 800 lines at most, private by default, one public table, dependencies one way.

**Addon APIs**
- Versioned (`API.v2`), `Supports(...)` for new parts, older callers keep working, contract-tested against every addon that calls them.

**An addon**
- Works alone; its pages, report window, TIMID row, help and What's new per the style guide; its login cost and saved-data size within budget; its own tests and changelog.

**The suite**
- Shared pieces only in the kit; addons talk only through APIs and kit signals; one brand, one look; together inside the frame budget.

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
