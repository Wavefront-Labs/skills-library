---
id: computing-software.cybersecurity-defensive.wazuh.custom-decoders-and-exclusion
name: custom-decoders-and-exclusion
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [custom-decoders, local-decoder, decoder-exclude, program-name, order]
level: practitioner
status: docs-checked
description: "Add custom Wazuh decoders in local_decoder.xml and modify a default decoder by copying it and excluding the original with decoder_exclude."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/decoders/custom.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add decoders to `/var/ossec/etc/decoders/local_decoder.xml`; for larger sets create separate files in `/var/ossec/etc/decoders/`.

The page's pattern is a parent decoder that uses `<program_name>` to match the program, and a child decoder that uses `<parent>`, `<regex>` and `<order>` (for example `user, srcip`).

Test with `/var/ossec/bin/wazuh-logtest`. Saving the file is enough for testing, but restart the manager to generate alerts: `systemctl restart wazuh-manager` or `service wazuh-manager restart`.

Modifying a default decoder:
1. Copy the file from `/var/ossec/ruleset/decoders/` to `/var/ossec/etc/decoders/`.
2. `chown wazuh:wazuh` and `chmod 660` the copy.
3. In `/var/ossec/etc/ossec.conf` add `<decoder_exclude>ruleset/decoders/<file>.xml</decoder_exclude>` inside `<ruleset>`. The example uses `0310-ssh_decoders.xml`.
4. Edit the copy and restart the manager.

Failure modes:
- Excluding an original decoder stops you receiving its upstream updates. Your copy stays unchanged across upgrades, so merge relevant changes by hand.
- Default decoders may not parse custom or non-standard log formats correctly, which is the usual reason to write one.

## Checked

2026-11-08: confirmed against the Wazuh docs page Custom decoders (read in full): local_decoder.xml and directory recommendation, the example parent and child decoders, wazuh-logtest, restart commands, the copy, chown, chmod and decoder_exclude procedure for 0310-ssh_decoders.xml, and the update caveat. Nothing removed.
Method: documentation only; no commands were run.
