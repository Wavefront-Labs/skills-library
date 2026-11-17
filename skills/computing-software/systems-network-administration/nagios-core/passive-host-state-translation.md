---
id: computing-software.systems-network-administration.nagios-core.passive-host-state-translation
name: passive-host-state-translation
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, translate-passive-host-checks, passive-host-checks-are-soft, passive-host-state, failover, distributed-monitoring, unreachable]
level: advanced
status: docs-checked
description: "Use translate_passive_host_checks so DOWN/UNREACHABLE passive host results match the local Nagios view in failover setups; when to leave it off."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/passivestatetranslation.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/passivechecks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passive host state translation

`translate_passive_host_checks` (main config, default 0) makes Nagios convert DOWN/UNREACHABLE from a remote source into the state correct for the local instance. Otherwise a submitted host result is taken as truth with no reachability logic.

## Example
Nagios-A is primary and actively checks everything. Nagios-B and -C are backups fed passive results from A. Router-C and Router-D are both offline.
- A: Router-D DOWN, Router-C UNREACHABLE.
- B should show Router-C DOWN, Router-D UNREACHABLE.
- C should show both DOWN.
Without translation, C would wrongly show Router-D UNREACHABLE.

## When
- **On:** failover/redundant setups where each backup needs an accurate picture from its own position.
- **Off:** when the central server should see how each distributed instance views its own segment.

## Related
`passive_host_checks_are_soft` (default 0) makes passive host results SOFT instead of HARD.

See `computing-software.systems-network-administration.nagios-core.network-reachability-parents` for how local reachability works.

## Checked

2026-11-04. Confirmed on the Passive State Translation page (Nagios-A/B/C example, central server may prefer untranslated views) and the main configuration page (translate_passive_host_checks default 0, passive_host_checks_are_soft default 0 meaning HARD). Nothing removed.

Method: documentation only; no commands were run.
