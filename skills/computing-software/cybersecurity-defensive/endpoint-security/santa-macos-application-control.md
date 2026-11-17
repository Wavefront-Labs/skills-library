---
id: computing-software.cybersecurity-defensive.endpoint-security.santa-macos-application-control
name: santa-macos-application-control
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [application-control, santa, macos, binary-authorization, lockdown-mode, monitor-mode, northpole, rudolph, teams-id-rules]
level: advanced
status: draft
description: "Run Santa on macOS for binary authorisation: monitor then lockdown mode, TeamID/signing ID rules, sync servers, and handling developer machines."
sources: ["Santa documentation (northpolesec.github.io/santa, originally google/santa)", "Apple Platform Security Guide (Gatekeeper, notarization)", "CIS Control 2.5 (allowlist authorized software)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Santa on macOS

**Goal:** control which binaries execute on macOS fleets beyond Gatekeeper, with rules managed
centrally and visibility of everything that runs.

## About
Santa (originally Google, now maintained by North Pole Security) uses the Endpoint Security
framework to allow/block executions by rules. Modes:
- **Monitor**: logs all executions, blocks only explicit block rules.
- **Lockdown**: blocks everything not explicitly allowed (or signed by allowed certificates/teams).

## Rule types (most to least preferred for allowing)
| Rule | Scope |
|---|---|
| TeamID | All software from a developer team (e.g. `EQHXZ8M8AV` Google) |
| SigningID | Specific signed binary (`TeamID:com.vendor.app`) |
| Certificate | Leaf signing certificate SHA-256 |
| CDHash | Specific code directory hash |
| Binary | File SHA-256 (exact file) |
Plus path regex allow/block via configuration (use sparingly).

## Deploy
1. Install the package and a configuration profile via MDM (system extension approval, full disk access, notification permissions).
2. Configure a **sync server** (Workshop, Rudolph, Zentral, Moroz or North Pole's commercial service) for rules and event upload.
3. Start in Monitor mode; collect executions for weeks; derive TeamID rules for common software.
4. Move groups of machines to Lockdown, starting with users with stable software needs.
5. Provide a self-service approval flow ("unknown binary blocked" notification with a link) for user-requested software, reviewed by IT/security.

## Commands
```
santactl status
santactl fileinfo /Applications/App.app/Contents/MacOS/App
santactl rule --allowlist --teamid --identifier EQHXZ8M8AV       # local testing only; prefer sync server
santactl sync
```

## Gotchas
- Developer machines compile binaries constantly: use compiler rules (transitive allowlisting) or keep them in Monitor with stronger EDR.
- Interpreters (Python, osascript) execute scripts Santa does not see as binaries; combine with EDR.
- Missing MDM approval for the system extension = Santa silently not running.

## Verify
- [ ] `santactl status` reports the expected mode and recent sync.
- [ ] Unknown unsigned binary is blocked on a Lockdown test machine.
