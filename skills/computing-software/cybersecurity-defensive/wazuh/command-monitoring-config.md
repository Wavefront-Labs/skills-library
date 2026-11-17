---
id: computing-software.cybersecurity-defensive.wazuh.command-monitoring-config
name: command-monitoring-config
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [command-monitoring, wodle-command, full-command, remote-commands, rule-530, frequency]
level: practitioner
status: docs-checked
description: "Run commands on agents and alert on output using the Wazuh command wodle or localfile full_command, with defaults, scheduling, checksums and the remote_commands switch."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/command-monitoring/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two modules can run commands.

Command module `<wodle name="command">` defaults: `disabled` no, `ignore_output` no, `timeout` (seconds, no default listed; 0 waits indefinitely), `skip_verification` no, `run_on_start` yes, `interval` 2s. Checksum tags `verify_md5`, `verify_sha1`, `verify_sha256` check only the first argument of `command`; a mismatch makes the output ignored unless `skip_verification` is yes. Scheduling uses `day` (1-31), `wday` (sun-sat, incompatible with `day`) and `time` (hh:mm); `interval` takes s, m, h, d suffixes and must be a multiple of months with `day`, weeks with `wday`, or days/weeks with only `time`.

Logcollector `<localfile>`: `log_format` is `full_command` (single entry) or `command` (multiline), plus `command`, `alias` and `frequency` (seconds, default 360).

Alerting: the default decoder `ossec` has prematch `^ossec: `. Base rule 530 is level 0, so a custom rule needs `if_sid` 530 and a higher level.

Remote execution is disabled by default. Enable with `wazuh_command.remote_commands=1` (Command module) or `logcollector.remote_commands=1` in `local_internal_options.conf`, then restart the agent.

Gotchas: from 4.13.0 commands must be on local file systems (no UNC paths or mapped drives). `ossec.conf` is at `/var/ossec/etc/` (Linux), `/Library/Ossec/etc/` (macOS), `%ProgramFiles(x86)%\ossec-agent\` (Windows).

## Checked

2026-11-03. Confirmed against the Wazuh page "Command monitoring configuration": Command module option table (defaults for disabled, ignore_output, skip_verification, run_on_start, interval 2s), checksum tags verifying only the first argument, day/wday/time scheduling rules, Logcollector `full_command`/`command`, `alias`, `frequency` default 360, decoder `ossec` prematch, base rule 530 at level 0, remote_commands switches in local_internal_options.conf, the 4.13.0 local-path note, and the ossec.conf locations. Fixed: timeout default (the page lists N/A) and the `<WAZUH_AGENT_DIR>` placeholder.

Method: documentation only; no commands were run.
