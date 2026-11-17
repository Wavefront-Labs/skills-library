---
id: computing-software.qa-testing-engineering.exploratory-testing.session-based-exploratory-testing
name: session-based-exploratory-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [exploratory-testing, manual-testing, session-based-test-management, sbtm, test-charters, timeboxing, heuristics, sfdipot, fewhicca, tours, oracles, bug-reports, bug-reproduction, minimal-repro, debriefing, usability-observation, devtools, browser-console, network-tab, qa, rapid-software-testing, edge-cases]
level: practitioner
status: draft
description: "Run exploratory testing as accountable, time-boxed sessions: charters, heuristics to generate test ideas, live note-taking, minimal reproductions and bug reports a developer can act on."
sources: ["https://www.satisfice.com/download/session-based-test-management", "https://www.developsense.com/resources/", "Elisabeth Hendrickson, Explore It! (Pragmatic Bookshelf, 2013)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Session-based exploratory testing

**Goal:** find the bugs scripted checks miss — by designing and running tests at the
same time — while still producing a record of what was covered and what was found.

## 1. Write a charter (2 minutes)
A charter is the mission for one session. Format (from *Explore It!*):
> **Explore** *<target>* **with** *<resources/techniques>* **to discover** *<information>*.

Examples:
- Explore *checkout with saved cards* with *expired and declined test cards* to discover *how payment failures are reported and recovered*.
- Explore *CSV import* with *malformed, huge and non-UTF-8 files* to discover *data-loss or crash risks*.
Too broad ("test the app") gives a wander; too narrow ("click Save") is a script.

## 2. Time-box the session
60–90 minutes, uninterrupted, one charter. Afterwards record roughly what share went
to **testing** vs. **bug investigation/reporting** vs. **setup** — if setup dominates,
that's a testability problem worth reporting in itself.

## 3. Generate test ideas with heuristics
- **SFDIPOT** (product elements, from Rapid Software Testing): Structure, Function,
  Data, Interfaces, Platform, Operations, Time. Walk the list against your target.
- **Data attacks:** empty, very long (10k chars), Unicode/emoji/RTL text, leading/
  trailing spaces, special characters (`' " < > & ; %`), zero, negative, huge numbers,
  dates like 29 Feb and 31 Dec 23:59, other time zones.
- **Interruptions:** back button mid-flow, refresh after submit, double-click submit,
  two tabs editing the same record, network drop (DevTools › Network › Offline or a
  throttling profile), session expiry, sleep/resume.
- **Consistency oracles (FEW HICCUPPS):** does it behave like its history, the
  product's image, comparable products, user expectations, the stated claims,
  related parts of itself, the purpose, statutes/standards? A mismatch is a candidate bug.
- **Tours:** follow the money, the data's lifecycle (create → edit → export → delete),
  the busiest user's day, the configuration settings, the error messages.

## 4. Keep notes while you test
Timestamped, terse: what you tried, what you saw, questions, bugs, ideas for later
sessions. Keep DevTools open (Console for errors, Network for failed/slow calls and
status codes) — many "UI" bugs are visible there first. Screen-record if your tool
allows; it makes the hard-to-repeat bug reportable.

## 5. Turn a finding into a minimal reproduction
1. Reproduce it again from a clean state (new session, private window).
2. Strip steps until removing any one makes it disappear.
3. Vary one factor at a time (browser, account role, data value) to find the boundary of the bug.
4. If you can't reproduce reliably, report it anyway with the frequency ("3 of 10 tries") and everything you know.

## 6. Write a bug report developers act on
- **Title:** what's wrong, where, under what condition — "Order total ignores discount when quantity edited in cart".
- **Environment:** build/version, browser + OS, account type, test data used.
- **Steps** (numbered, minimal), **expected** (and its oracle), **actual**.
- **Evidence:** screenshot/recording, console errors, the failing request/response (with any tokens or personal data redacted).
- **Impact:** who hits it, how often, workaround — this drives priority.
One bug per report.

## 7. Debrief (10 minutes)
With a lead or developer: what the charter covered, bugs and issues found, what's
untested, new charters suggested. Use the debrief to steer the next session toward risk.

## 8. Usability observation
When watching a real user, stay silent; note where they hesitate, misclick or backtrack and
what they say they expected. Don't explain the UI — that's the finding.

## Unconfirmed / notes
Methodology summarised in my own words from the SBTM paper (Bach), Rapid Software
Testing material (Bach/Bolton) and *Explore It!*; mnemonic expansions as commonly
published — check the originals for current versions.

## Verify
- [ ] Each session has a written charter, a time-box and notes.
- [ ] Bugs have minimal steps, expected vs actual, environment and evidence.
- [ ] Sensitive data redacted from screenshots and network captures.
- [ ] Debrief recorded what was *not* covered and proposed follow-up charters.
