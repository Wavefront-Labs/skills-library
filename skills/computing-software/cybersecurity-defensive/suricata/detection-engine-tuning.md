---
id: computing-software.cybersecurity-defensive.suricata.detection-engine-tuning
name: detection-engine-tuning
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [mpm-algo, hyperscan, detect-profile, sgh-mpm-context]
level: advanced
status: docs-checked
description: "Tune detection: mpm-algo (ac, ac-ks, hs), sgh-mpm-context, detect.profile and custom group sizes, grouping ports and prefilter defaults."
sources: ["https://docs.suricata.io/en/latest/performance/tuning-considerations.html", "https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Detection tuning

- `mpm-algo`: `ac` default in tuning docs; Hyperscan (`hs`) is best where supported (recommended on x86_64); `ac-ks` beats `ac` on commodity hardware without Hyperscan.
- `detect.sgh-mpm-context`: `auto`, `single` or `full`. `full` helps with `ac` and `ac-ks`; avoid with Hyperscan (long startup), prefer a higher profile or larger custom groups.
- `detect.profile`: `low`, `medium`, `high` or `custom`; the YAML sample defaults to `medium`. With `high` both group counts default to 75. `custom-values` sets `toclient-groups` and `toserver-groups`; raising them generally helps at minor memory cost.
- `inspection-recursion-limit` 3000, `stream-tx-log-limit` 4, `guess-applayer-tx: no`.
- `grouping`: `tcp-priority-ports`, `udp-priority-ports`.
- `prefilter.default`: `mpm` or `auto`.

## Checked

2026-11-04. Confirmed against Tuning Considerations (mpm-algo, sgh-mpm-context, detect.profile, 75 default groups) and the suricata.yaml configuration page (sample `profile: medium`, `inspection-recursion-limit: 3000`, `stream-tx-log-limit: 4`, `guess-applayer-tx: no`, grouping priority ports, prefilter default, Hyperscan on x86_64).

Method: documentation only; no commands were run.
