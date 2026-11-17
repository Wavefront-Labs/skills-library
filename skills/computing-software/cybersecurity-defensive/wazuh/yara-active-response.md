---
id: computing-software.cybersecurity-defensive.wazuh.yara-active-response
name: yara-active-response
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [yara, yara-rules, active-response, fim-yara, malware-detection, yara-linux]
level: advanced
status: docs-checked
description: "Scan new or modified files with YARA from Wazuh FIM via active response, with Linux and Windows setup, rule IDs and a file-deleting script warning."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/malware-detection/fim-yara.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wazuh FIM detects new or modified files and triggers a YARA active response to scan them. Matches reach the manager, but you must add the decoders yourself.

Linux example (Ubuntu 22.04):
- Build YARA 4.5.5 into `/usr/local/bin`, install `jq`, and save rules to `/tmp/yara/rules/yara_rules.yar`.
- Put `yara.sh` in `/var/ossec/active-response/bin/` with mode 750 and owner `root:wazuh`.
- Monitor `/root/` with `<directories realtime="yes">` in the agent `ossec.conf`.
- Server: add `yara_decoder` and `yara_decoder1` to `local_decoder.xml`; add rules 100200 (modified) and 100201 (added) to `local_rules.xml`; add command `yara_linux` with `-yara_path` and `-yara_rules` in `extra_args`, bound to rules 100200,100201 with `location` `local`.

Windows 11 example: install Python 3 (added to PATH), the VC++ redistributable and YARA 4.5.5 (`yara64.exe`) under the agent's `active-response\bin\yara\` folder, plus `valhallaAPI` to fetch rules. Create `yara.bat`, monitor `<USER_PROFILES>\*\Downloads`. Server rules 111111 and 111112 (FIM), 111113 (grouping), 111114 (match, level 12); command `yara_windows` runs `yara.bat`.

Review matches in Threat Hunting by filtering `rule.groups` for `yara`.

Gotchas:
- The Windows script deletes any file matching a rule, so monitor only suitable directories.
- The Linux script waits for file size to stabilise before scanning.
- The page uses a placeholder API key and a demo Valhalla key.
- Disable Defender temporarily when testing with EICAR.

## Checked

2026-11-08. Read the whole FIM and YARA page. Confirmed: flow, YARA 4.5.5 and paths, yara.sh mode and owner, jq, realtime directories, decoders, rules 100200/100201 (Linux) and 111111-111114 (Windows, 111114 level 12), command and active-response blocks, Windows folder layout, valhallaAPI, delete-on-match yara.bat, Threat Hunting rule.groups filter. Removed: the specific Python 3.12.2 version (page says Python 3.X).
Method: documentation only; no commands were run.
