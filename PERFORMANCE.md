# Performance rules for the Forever addons

Every TIMID addon runs inside the game's own frame: one Lua thread, shared with the game client
and every other addon. Whatever an addon does between two frames, the player waits for. So the
first rule comes before every feature:

**The player must never feel the addons.** No hitches, no dropped frames, no garbage-collection
stutters, no lag in combat. A feature that cannot meet that is not finished.

This page is the rulebook. The shared pieces it names live in ForeverKit (from kit minor 18), so
no addon builds its own (see STYLE.md, "Build it once").

## 1. Budgets

| What | Limit |
|---|---|
| One event handler, one run | under 0.2 ms; anything bigger is a job (rule 4) |
| One addon, one frame, all its work | under 1 ms on average, 2 ms at most |
| A job's share of one frame | `Kit.Job` budget: 1 ms by default; 0.5 ms while another addon is busy at the auction house; 0 in combat unless it must run |
| A redraw | under 2 ms for a full window; rows that did not change are not touched |
| A hover (tooltip line) | a table lookup, nothing else |
| Garbage | none per frame while idle; a burst of 100 events makes at most a few KB |
| Idle | no OnUpdate script runs and no timer reschedules itself while nothing is happening |

Numbers are checked with `/timid perf` in game and with the perf workloads in the test harness
(rule 9) before and after every change that touches a hot path.

## 2. Do less work

- **Events, not polling.** React to the game's events. An OnUpdate script is allowed only for
  something that truly changes every frame (a drag, a cast bar, a countdown on screen), runs only
  while that thing is happening, and stops itself (hide the frame or clear the script) when it
  ends. A timed check uses `Kit.After`, not a frame counter.
- **Coalesce bursts.** Events that come in bursts (BAG_UPDATE, GET_ITEM_INFO_RECEIVED,
  QUEST_LOG_UPDATE, Auctionator's database updates, MERCHANT_UPDATE) never run the work
  directly. They mark something dirty and ask for one run: `Kit.Coalesce` or the event bus's
  `bus:Coalesce`. One hundred events give one recompute.
- **Dirty flags.** Each piece of derived data has a flag (`Kit.Dirty`) set by what can change
  it and cleared by the one function that rebuilds it. Nothing is rebuilt that is not dirty.
- **Caches say how stale they may be.** Every cache (`Kit.Cache`) names what invalidates it
  ("bags", "prices", "recipes", "settings") and, when time matters, how old an answer may be.
  The comment above it says so in one line.
- **Lazy.** Nothing is built before it is needed: settings pages, windows, tabs, rows, big
  tables. Login builds only what the first frame shows.
- **Precompute static data.** Data that never changes in play (recipes, fishing tables, vendor
  prices) ships as ready-made lookup tables, keyed the way the code reads them.
- **Quiet during scans.** While an auction house scan floods item data (`Kit.ScanBusy`), addons
  wait for `Kit.OnScanQuiet` and then do their work once.

## 3. Do work cheaper

- **The right shape of table.** Look things up by key (`byItem[itemID]`), never by walking a
  list in a hot path. Sorted arrays and binary search for ranges; buckets for spatial data.
- **Locals for hot globals.** In a file with a hot path, game functions and globals used there
  are made upvalues at the top (`local GetTime = GetTime`), unless they must be read fresh
  because a test or another addon replaces them (say so in a comment).
- **No allocation in hot paths.** No new tables, closures or string building (`..`,
  `string.format`, `table.concat`) per event, per row or per frame. Reuse a scratch table;
  build text only when it changes; cache formatted money (`Kit.Money` is cached for this).
- **Guards once, not per call.** Check that an API exists when the file loads, not inside every
  call (a `pcall` with a new closure per call is an allocation).

## 4. Spread work out

- **Big jobs are time-sliced.** Any job that can take more than 1 ms (a plan for a long queue,
  a full bag or bank scan, building a big list) is a `Kit.Job`: a coroutine that calls
  `Kit.Breathe()` in its loops and gives the frame back when its budget (measured with
  `debugprofilestop`) is spent. It carries on next frame. The answer it gives must be the same as
  doing it all at once.
- **One budget per addon.** The kit's scheduler shares each frame between addons; a busy addon
  cannot starve the others or the game.
- **Combat waits.** Work the player cannot see in combat (rebuilding lists, saving, scans, big
  redraws) is put off with `Kit.OutOfCombat(addon, key, fn)` and done after combat, once. Protected
  frames are never touched in combat (`InCombatLockdown()`).
- **The busy addon comes first.** While an addon signals `Kit.Busy("auction")`, the others
  slow their redraws and pause their jobs. The buying itself is never throttled.

## 5. Keep memory stable

- **Pools, not new frames.** Rows, buttons, textures and font strings are taken from a pool
  (`Kit.Pool`) and given back on redraw. A window's second opening makes no new frames.
- **Recycle tables.** Scratch tables are wiped and reused (`wipe`), not replaced.
- **Saved variables stay small.** Every history, log or record has a cap (count or age) and is
  trimmed on login. The saved table has a version number and each migration is one marked,
  one-time step (`Kit.MigrateDefault`, `Kit.SeedSetting`). Nothing derived is saved: it is
  rebuilt.

## 6. Model and view apart

- **The data never draws.** Data code updates its tables and marks the view dirty; the view
  redraws on its own schedule (`Kit.Coalesce`, 4 a second at most) from one consistent snapshot.
- **A hidden window costs nothing.** A view that is not shown does not redraw; it redraws once
  when shown.
- **Redraw what changed.** Rows keep what they show; a row whose data did not change is not
  touched.

## 7. The shared core (ForeverKit)

Use these; never build another (see STYLE.md "Build it once").

| Need | Kit piece |
|---|---|
| A timer | `Kit.After` |
| A redraw cap or a burst folded into one run | `Kit.Coalesce` |
| Events, with coalescing and listening only while needed | `Kit.Events` (the bus) |
| Something changed, rebuild later | `Kit.Dirty` |
| A remembered answer with an invalidation rule | `Kit.Cache`, `Kit.Invalidate(tag)` |
| A long job spread over frames | `Kit.Job`, `Kit.Breathe` |
| Rows, buttons, textures, scratch tables | `Kit.Pool`, `Kit.Scratch` |
| Waiting for combat to end | `Kit.OutOfCombat` |
| Quiet during an auction house scan | `Kit.ScanBusy`, `Kit.OnScanQuiet` |
| Another addon is busy at the auction house | `Kit.Busy`, `Kit.IsBusy`, `Kit.OnBusy` |
| Timing a piece of work | `Kit.Ms`, `Kit.Measure` |

## 8. Only what this client has

The game is the WoW Forever client (a Classic-era game on a newer client, build 1.60.1). Every
game function an addon calls is checked against this client, not against retail or Classic
documentation. A function that may be missing is looked up once, guarded, and has a fallback
that keeps the feature working. A new API goes on the verified list (in the kit's comments) only
after it is seen working in game.

## 9. Measure, don't guess

- **Profile first.** Before optimising, measure: which handler, how often, how long, how much
  garbage. Fix the hottest path first.
- **`/timid perf`** shows, per addon: time per event, the longest frame, memory and its growth.
  It costs nothing while off. Its deep option turns on the game's script profiler
  (the `scriptProfile` setting) for function-level times; that slows every addon and needs a
  reload, so it is for a short test only, and it says so.
- **Perf workloads in the tests.** Each addon's test harness can time realistic bursts (100 bag
  events, opening each window, a long queue). A change to a hot path records the numbers before
  and after in its changelog or report.
- **Numbers in reviews.** A review of a hot-path change asks for the before and after numbers.

## 10. Checklist for every new feature

1. What events does it listen to, and can they come in bursts? Coalesce them.
2. Does anything run every frame or on a timer while nothing happens? It must not.
3. What does it build at login? Make it lazy.
4. Is there a loop over bags, recipes, quests or a queue in a handler? Make it a lookup, or a job.
5. Does a redraw make frames, tables or strings? Pool and reuse them.
6. Does it run in combat? Put it off unless the player needs it now.
7. Does it save anything new? Give it a cap and a version.
8. Is every game function it calls on this client? Guard it once.
9. Numbers before and after, from the perf workloads and `/timid perf`.
