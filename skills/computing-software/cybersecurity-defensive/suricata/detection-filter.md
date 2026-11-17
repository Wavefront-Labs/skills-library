---
id: computing-software.cybersecurity-defensive.suricata.detection-filter
name: detection-filter
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [detection-filter, unique-on, scan-detection]
level: advanced
status: docs-checked
description: "Use detection_filter to alert on every match after a count in a window, including unique_on for port-scan patterns."
sources: ["https://docs.suricata.io/en/latest/rules/thresholding.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# detection_filter

`detection_filter: track <option>, count <N>, seconds <T>[, unique_on <src_port|dst_port>]`

- Alerts on every match after the count is reached within the time window. Threshold type `threshold` instead resets its counter and alerts each time the count is reached again.
- Neither action nor alert fires at the count limit, only after it.
- `unique_on` counts distinct source or destination ports in the window. It works only with TCP, UDP or SCTP rules and is rejected for other protocols and for `ip` rules.
- Docs example: 10 or more distinct destination ports from one source within 60 seconds, a vertical scan.

Track options are the same as threshold: `by_src`, `by_dst`, `by_both`, `by_rule`, `by_flow`.

Global defaults live under `detect.thresholds`: `hash-size` 16384, `memcap` 16mb.

## Checked

2026-11-04. Confirmed against the Thresholding Keywords page and the Thresholding Settings sample in the suricata.yaml configuration page.

Method: documentation only; no commands were run.
