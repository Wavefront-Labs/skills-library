---
id: computing-software.cybersecurity-defensive.wazuh.wazuh-logtest-usage
name: wazuh-logtest-usage
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [wazuh-logtest, rule-test, sessions, firedtimes, logtest-api]
level: practitioner
status: docs-checked
description: "Test Wazuh decoders and rules with wazuh-logtest: rule_test defaults, output phases, session tokens, firedtimes and the logtest API."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/testing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`/var/ossec/bin/wazuh-logtest` tests decoders and rules against sample logs on the server. Reach it from the dashboard (Tools, Ruleset test), the command line, or the server API. It uses the same rules as the analysis engine.

Output phases: pre-decoding, decoding, filtering (rules), then "Alert to be generated".

Configuration `<rule_test>` in `ossec.conf`:
- `enabled`: `yes` (default)
- `threads`: `1` (1 to 128 or `auto`)
- `max_sessions`: `64` (1 to 500)
- `session_timeout`: `15m` (s, m, h; max 365d)

Each session loads its own rules and decoders, and a `firedtimes` counter tracks matches for the session. Idle sessions close after the timeout; at the session limit the longest idle one closes. In a cluster the master node processes logs.

Example: repeating an sshd invalid-user log eight times within two minutes triggers rule 5712 instead of 5710, which only works inside one session.

API: `PUT /logtest` runs a test; `DELETE /logtest/sessions/{token}` closes a session.

Gotchas:
- A missing or invalid token starts a new session and reloads rules. Keep the token to preserve `firedtimes` history.
- The page lists `wazuh`/`wazuh` as default API credentials. Change them, or take generated ones from `wazuh-install-files.tar`.

## Checked

2026-11-08: confirmed against the Wazuh docs page Testing decoders and rules (read in full): the access options, output phases, rule_test defaults and ranges, session behaviour, the rule 5710 and 5712 example, the two API endpoints, session token behaviour and the default API credentials. Nothing removed.
Method: documentation only; no commands were run.
