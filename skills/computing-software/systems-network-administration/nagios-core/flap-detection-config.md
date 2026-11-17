---
id: computing-software.systems-network-administration.nagios-core.flap-detection-config
name: flap-detection-config
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, enable-flap-detection, flap-detection-enabled, low-flap-threshold, high-flap-threshold, flap-detection-options, flapping-config]
level: practitioner
status: docs-checked
description: "Enable and tune Nagios Core flap detection: global enable_flap_detection plus per-object flag, global and per-object thresholds, and flap_detection_options."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/flapping.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuring flap detection

Both must be 1:
1. Global `enable_flap_detection` in `nagios.cfg`.
2. Per object `flap_detection_enabled` in the host/service definition.

Set the global to 0 to disable everywhere; set the per-object flag to 0 for one item.

## Thresholds
| Scope | Global | Per object |
|---|---|---|
| Host | `low_host_flap_threshold`, `high_host_flap_threshold` | `low_flap_threshold`, `high_flap_threshold` |
| Service | `low_service_flap_threshold`, `high_service_flap_threshold` | same |

Global values apply unless the object sets its own (0 in a definition means use the global).

## Restrict states
`flap_detection_options` (host `o,d,u`; service `o,w,c,u`) limits which states feed the calculation. Omitted = all.

## Notifications
Flapping itself suppresses problem/recovery notices; you can include `f` in `notification_options` to receive FLAPPINGSTART/STOP notices.

Internals: `computing-software.systems-network-administration.nagios-core.flap-detection-algorithm`.

Self-check: a service that starts flapping gets a log message and a non-persistent comment.

## Checked

2026-11-04. Confirmed on the Flapping page: enable_flap_detection and flap_detection_enabled both needed, the global and object threshold variable table, flap_detection_options restricting states, flapping start/stop notifications and suppression of other notifications; 0 meaning use the global threshold on the object definitions page. Replaced the unconfirmed web UI icon check with the documented log message and comment.

Method: documentation only; no commands were run.
