---
id: computing-software.qa-testing-engineering.cypress.debugging-with-pause-debugger-and-command-log
name: debugging-with-pause-debugger-and-command-log
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cy-pause, command-log, cypress-debugging, cy-debug, time-travel]
level: practitioner
status: verified
description: "Debug Cypress tests: time-travel in the command log, cy.pause and step-through, .debug(), debugger inside .then, console output, and debugging in CI runs."
sources:
  - https://docs.cypress.io/app/guides/debugging
  - https://docs.cypress.io/api/commands/pause
  - https://docs.cypress.io/api/commands/debug
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging with cy.pause, debugger and the command log

## Command log time travel
In `cypress open`, hover a command to see the DOM snapshot at that moment; click to pin it, and inspect before/after states (for actions). Click a command to print details (yielded subject, matched elements) to the DevTools console.

## cy.pause
```js
cy.get('[data-cy=basket]').click();
cy.pause();                       // stops the queue; use "Next" to step one command, "Resume" to continue
cy.get('[data-cy=total]').should('contain', '£36');
```
Ignored in `cypress run` headless mode.

## debugger and .debug()
```js
cy.get('[data-cy=rows]').then(($rows) => {
  debugger;                      // DevTools must be open; runs when the command executes
});
cy.get('[data-cy=rows]').debug();   // logs subject and pauses in debugger
```
A bare `debugger` statement outside `.then` triggers before commands run (queue not executed yet), so it is useless there.

## Console and Node logs
- `cy.log('message')` shows in the command log.
- `cy.task('log', msg)` prints in the terminal (CI logs).
- Browser `console` output is not in CI logs by default (a `console.log` and a `cy.log` in a spec produced no terminal output in a `cypress run`); capture with plugins like `cypress-terminal-report` (exists on npm, 7.x).

## Debugging CI failures
- Screenshots on failure (default in run mode) and videos (opt-in since Cypress 13).
- `DEBUG=cypress:* npx cypress run` for Cypress internals (server, network proxy); `DEBUG=cypress:* npx cypress verify` printed `cypress:cli` debug lines.
- Test Replay in Cypress Cloud for full DOM/network replay.
- Reproduce locally with the same browser and viewport: `npx cypress run --browser chrome --spec cypress/e2e/x.cy.js --headed`.

## Gotchas
- `.only` left in a spec silences the rest of the suite; lint for it (`eslint-plugin-mocha` `no-exclusive-tests`).

## Verify
Checked on Cypress 16.2.0: `cy.pause()`/`.debug()` do not stall `cypress run`; failure screenshots are written by default; the docs page confirms a bare `debugger` runs before the commands. A failing test can be stepped through with pause, and CI failures carry screenshots and terminal logs sufficient to diagnose.
