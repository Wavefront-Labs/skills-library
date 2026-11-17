---
id: computing-software.systems-network-administration.keepalived.misc-check
name: misc-check
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, misc-check, health-checking, misc-path, custom-script, real-server]
level: practitioner
status: docs-checked
description: "MISC_CHECK runs a user script on the director to judge a real server; misc_path takes the full script path, with arguments in double quotes; script returns 0 or 1."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/software_design.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MISC_CHECK

Availability check by user script, run on the director (not on the real server).

```
real_server 192.168.100.6 80 {
    weight 1
    MISC_CHECK {
        misc_path "/path/to/check.sh <arg>"
    }
}
```
- `misc_path`: the full path to the script, optionally followed by arguments inside double quotes.
- The script must return 0 or 1 (a binary pass/fail).

The page documents no other MISC_CHECK keywords and no semantics for which value means which; test with a known-good and known-bad server before relying on it.

Verify: a script run by hand returns the expected status for healthy and unhealthy backends.

## Checked

2026-11-04. Confirmed misc_path, the quoting rule for arguments, execution on the director and the 0 or 1 result on the configuration synopsis and Software Design pages. Nothing removed.

Method: documentation only; no commands were run.
