---
id: computing-software.qa-testing-engineering.exploratory-testing.random-and-monkey-testing
name: random-and-monkey-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [random-testing, monkey-testing, fuzzing, android-monkey, gremlins-js]
level: practitioner
status: docs-checked
description: "Run random and monkey testing: Android monkey and gremlins.js for web, seeded runs, stop-on-error behaviour and reproducing failures."
sources:
  - https://developer.android.com/studio/test/other-testing-tools/monkey
  - https://github.com/marmelab/gremlins.js
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Random and monkey testing

**Goal:** shake out crashes and robustness defects with large volumes of pseudo-random input, cheaply, in a random yet repeatable manner.

## Android: Monkey
The Monkey runs on an emulator or device and generates pseudo-random streams of user events (clicks, touches, gestures) and system-level events. Launch it from a shell in that environment:
```bash
adb shell monkey -p your.package.name -s 4242 --throttle 200 -v -v 20000
```
- `-s <seed>`: the same seed regenerates the same event sequence, so a failing run can be repeated.
- `-p <package>`: only activities in that package may be visited; attempts to navigate elsewhere are blocked. Repeat `-p` for each extra package the app needs (for example a contact picker).
- `--throttle <ms>`: fixed delay between events; without it events are sent as fast as possible.
- `--pct-touch`, `--pct-motion`, `--pct-trackball`, `--pct-nav`, `--pct-majornav`, `--pct-syskeys`, `--pct-appswitch`, `--pct-anyevent`: adjust event mix.
- `-v` (repeat for more): level 0 is quiet, level 1 shows individual events, level 2 adds setup detail about activities selected or not.
- By default the Monkey stops and reports on an unhandled exception or crash, an Application Not Responding error, and a permission (security exception) error. `--ignore-crashes`, `--ignore-timeouts` and `--ignore-security-exceptions` make it continue until the event count is done.
- `--kill-process-after-error` stops the failed process; `--monitor-native-crashes` reports native crashes in Android system code.

## Web: gremlins.js
A monkey testing library for the browser and Node.js. Gremlins click anywhere, fill forms, scroll, touch and type keys; mogwais only monitor (alert, fps, gizmo). The fps mogwai logs an error when frames per second drop below 10, and gizmo stops the horde after 10 errors. The default horde stops after roughly one minute.
```js
const horde = gremlins.createHorde({
  randomizer: new gremlins.Chance(1234),
  strategies: [gremlins.strategies.allTogether({ nb: 10000 })],
});
horde.unleash(); // returns a promise
```
- Seed the randomizer with `new gremlins.Chance(<seed>)` to make an attack repeatable.
- `species` and `mogwais` options pick which gremlins run; by default all are used. `gremlins.allSpecies` adds your own on top of the defaults.
- Strategies bundled: `distribution` (default, 10 ms delay), `allTogether` and `bySpecies`. `horde.stop()` ends an attack.
- Playwright: load the bundle with `page.addInitScript({ path: './node_modules/gremlins.js/dist/gremlins.min.js' })`, then `page.evaluate(() => gremlins.createHorde().unleash())`.
- Cypress: pass the tested window, `createHorde({ window: testedWindow })`.
- A custom logger object (`log`, `info`, `warn`, `error`) can store the activity for later replay.

## Turning hits into tests
1. Record the seed and the event log.
2. Replay with the same seed.
3. Write a deterministic regression test for the failing sequence.

## Gotchas
- No seed means no reproduction. Always log it.
- Random events can trigger destructive actions; run against disposable data and restrict the package or page area.

## Verify
Runs are seeded, crashes are triaged with seed and log, and each fixed crash has a deterministic regression test.

## Checked
2026-11-09: checked against the Android Monkey page (options, stop conditions, seed) and the gremlins.js README (species, mogwais, strategies, seeding, Cypress and Playwright usage; all read in full). Removed because the pages do not state them: the ISTQB source and the random-testing classification, the `// CRASH:` and `// NOT RESPONDING:` log markers, the unpkg script load, `nb` on the distribution strategy (README shows it on allTogether), the smart versus dumb monkey section, the sanitizer advice, and the bisect-to-shortest-prefix procedure. Tags `experience-based-testing` trimmed.

Method: documentation only; no commands were run.
