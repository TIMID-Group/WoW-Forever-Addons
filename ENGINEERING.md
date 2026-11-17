# Engineering rules for the Forever addons

How TIMID addon code is organised. These rules make bugs easier to find, code easier to test and change, and performance work easier (see `PERFORMANCE.md`). They sit beside `STYLE.md` (how things look) and are checked in every review.

## 1. One job per module

- Each file (module) does one thing and is named for it: `QueueRunner.lua` runs steps, `QueueSizing.lua` works out how much, `Mail.lua` takes mail. A file that needs "and" to describe it is two files.
- **Soft size cap: about 800 lines.** Past that, look for the second job hiding inside and split it out.
- One function, one job. If a function both decides and does, split the deciding (pure, testable) from the doing (talks to the game).

## 2. Private by default, a small public surface

- Everything is `local` unless another module needs it. Each module returns or registers **one table** with the few functions others may call (`ns.QueueSizing = { Round = ..., Group = ... }`).
- Don't put new names straight on `ns`. The shared namespace is for module tables, not loose functions.
- The public table is the contract: change inside a module freely, change its public functions carefully and with tests.

## 3. Dependencies point one way

- **UI → logic → data → game API.** Logic never calls UI; data never calls logic. The UI asks for a snapshot and draws it; logic says "changed" through the kit's events or dirty flags, and the UI decides when to redraw.
- No cycles between modules. If two modules need each other, the shared part becomes a third module.

## 4. Addons talk only through APIs

- One addon uses another only through its published API (`ForeverWorkbench.API.v2`, the Ledger's API) or the kit's neutral signals (`Kit.Busy`, `Kit.Events`). Never another addon's internals or saved data.
- APIs are versioned, check `Supports(...)` before using something new, and older callers keep working.

## 5. One source of truth

- Every calculation exists once. A preview (plan check, tooltip, card) and the code that acts (runner, buyer) call **the same function**. Two copies of the same arithmetic will drift, and the player sees the difference.
- Every piece of state has one owner module; others read it through that module.
- Shared pieces live in the kit ("Build it once" in `STYLE.md`).

## 6. Composition over inheritance

- Build behaviour by combining small parts (Lua mixins, plain tables of functions) rather than deep hierarchies. A step kind is a small table with `start`, `size`, `describe`; the runner composes them.

## 7. Easy to test

- Logic modules take what they need as arguments (bags, prices, the queue) instead of reaching for globals, so a test can hand them exact inputs.
- Every public function has tests; every bug fix adds the test that would have caught it.
- Before-and-after tests guard every refactor (`PERFORMANCE.md` 9c).

## 8. Readable

- Names say what things are. Comments say **why**, especially for a non-obvious pattern; the code says what.
- Fail safe: guard game calls once at the edge, not everywhere inside.

## 9. Review checklist

1. Does each changed file still have one job, and stay under about 800 lines?
2. Is anything new on `ns` that could be local or inside a module table?
3. Does any logic call the UI, or any module reach into another addon?
4. Is any calculation now in two places?
5. Are there tests for the public functions touched, and a before-and-after test for a refactor?
