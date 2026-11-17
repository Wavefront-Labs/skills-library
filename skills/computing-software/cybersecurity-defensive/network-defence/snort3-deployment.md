---
id: computing-software.cybersecurity-defensive.network-defence.snort3-deployment
name: snort3-deployment
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [snort3, snort, ids-ips, snort-lua-config, pulledpork3, inline-ips, rule-management]
level: practitioner
status: docs-checked
description: "Deploy Snort 3: Lua configuration, DAQ modes for IDS vs inline IPS, PulledPork3 rule updates, policy selection, performance options and alert output to the SIEM."
sources: ["https://docs.snort.org/", "https://github.com/snort3/snort3", "https://github.com/shirkdog/pulledpork3", "https://www.snort.org/downloads"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snort 3

## Install and config
- Packages or build from source (snort3 + libdaq). Config is Lua: `snort.lua` and `snort_defaults.lua`.
- Set `HOME_NET` and `EXTERNAL_NET` accurately - most rules depend on them.
```lua
HOME_NET = '10.0.0.0/8 192.168.0.0/16'
EXTERNAL_NET = '!$HOME_NET'
ips = { enable_builtin_rules = true, variables = default_variables,
        include = RULE_PATH .. '/pulledpork.rules' }
-- enable a JSON or syslog alert output module here; take the module and field names from the Snort 3 manual
```
- Test config: `snort -c /usr/local/etc/snort/snort.lua -T`.

## Run modes
- Passive IDS on a SPAN/TAP: `snort -c snort.lua -i eth1 -l /var/log/snort -D`.
- Inline IPS: run with `-Q` (inline mode) on a DAQ module that supports inline operation, with the interface pair or queue set as in the Snort 3 manual; rules with `drop`/`block` actions take effect only inline.
- Multi-threading: see the Snort 3 manual for the packet-thread option and your DAQ module's load-balancing settings.

## Rules
- PulledPork3 (`pulledpork.py -c pulledpork.conf`) downloads Talos rules (registered/subscriber oinkcode), community rules and LightSPD packages, and applies a policy (`connectivity`, `balanced`, `security`, `max-detect` or `none`; the default is `connectivity`).
- Start with the `balanced` policy, tune with suppressions/thresholds (`suppress = { { gid = 1, sid = 1234, track = 'by_src', ip = '10.1.1.5' } }`).
- Snort 2 rules convert with `snort2lua`.

## Output
JSON alerts to a file shipped by a forwarder, or syslog alerts. Include `service` and
rule metadata for triage.

## Gotchas
- Inline mode failure behaviour: decide fail-open (bypass NIC) vs fail-closed.
- Rule updates need a reload or restart; test the config with `snort -T` and check the log for errors after each update.
- Encrypted traffic limits inspection; pair with TLS metadata analysis.

## Verify
- [ ] `snort -T` passes after each rule update (in the pipeline).
- [ ] A harmless test rule or test request that you wrote raises an alert in the SIEM.

## Checked

- Date: 2026-11-02.
- Confirmed against: snort3 README (-T config test, -Q inline mode, snort2lua) and PulledPork 3 README (pulledpork.py -c, Talos registered/subscriber oinkcode, community rules, LightSPD, policies connectivity, balanced, security, max-detect and none, default connectivity).
- Fixed: the recommended starting policy name ("balanced-ips" is not a policy; the default is connectivity).
- Removed: alert_json field list, afpacket/NFQ and fanout/-z flags, SIGHUP reload, JA4 and the external test URL (the Snort docs site returned a stub and the README does not state them).

Method: documentation only; no commands were run.
