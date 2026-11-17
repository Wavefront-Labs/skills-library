---
id: computing-software.cybersecurity-defensive.wazuh.agent-queue-antiflooding
name: agent-queue-antiflooding
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [client-buffer, antiflooding, queue-size, events-per-second, leaky-bucket]
level: practitioner
status: docs-checked
description: "Tune the Wazuh agent client_buffer leaky-bucket queue: queue_size and events_per_second defaults, the 202 to 205 buffer alerts, and where flooded agents drop events."
sources:
  - https://documentation.wazuh.com/current/user-manual/agent/agent-management/antiflooding.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Agents buffer events and forward them to the manager at a capped rate (a leaky bucket).

`<client_buffer>` in `ossec.conf` has `<disabled>` (default `no`), `<queue_size>` (default 5000 events) and `<events_per_second>` (default 500 EPS). `ossec.conf` is at `/var/ossec/etc/` (Linux), `%ProgramFiles(x86)%\ossec-agent\` (Windows), `/Library/Ossec/etc/` (macOS). Restart the agent after editing.

Overrides: centralized `agent.conf` overrides local settings. `agent.min_eps` in `internal_options.conf` sets a minimum EPS that overrides the manager-set limit.

Buffer alerts by rule ID:
- 202: warning at 90% full (default)
- 203: buffer full, new events are dropped
- 204: flooding, when the buffer stays above the warning level longer than `agent.tolerance`
- 205: normal, when usage falls below 70% (default)

Gotcha: a flooded agent drops events, and the 204 alert warns the agent will probably not recover to normal by itself. Advanced tuning knobs are `logcollector.max_lines` and `wazuh_modules.max_eps` in `internal_options.conf`.

## Checked

2026-11-03. Confirmed against the Wazuh page "Wazuh agent queue": leaky bucket, `<client_buffer>` with `<disabled>`, `<queue_size>` 5000 and `<events_per_second>` 500 defaults, config file paths per OS, restart commands, centralized override and `agent.min_eps`, alerts 202 (90%), 203, 204 (`agent.tolerance`) and 205 (70%), and `logcollector.max_lines` / `wazuh_modules.max_eps`. Removed: the `<WAZUH_AGENT_DIR>` placeholder, "treat as incidents" and the "Practical use" advice (not on the page).

Method: documentation only; no commands were run.
