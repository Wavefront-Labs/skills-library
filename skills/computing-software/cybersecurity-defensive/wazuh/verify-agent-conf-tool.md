---
id: computing-software.cybersecurity-defensive.wazuh.verify-agent-conf-tool
name: verify-agent-conf-tool
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [verify-agent-conf, validation, agent-conf, shared-folder]
level: intro
status: docs-checked
description: "Validate Wazuh centralized agent.conf files before distribution with verify-agent-conf, for every group folder or one file passed with -f."
sources:
  - https://documentation.wazuh.com/current/user-manual/reference/tools/verify-agent-conf.html
  - https://documentation.wazuh.com/current/user-manual/reference/centralized-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`verify-agent-conf` verifies the Wazuh `agent.conf` configuration.

Usage: `verify-agent-conf [-f <agent.conf file>]`, run as `/var/ossec/bin/verify-agent-conf`.

Default behaviour: with no option it searches `/var/ossec/etc/shared` for the folders belonging to groups and verifies the `agent.conf` file inside each, if it exists.

Option: `-f` verifies the file at the path you specify, which is how you test a temporary copy such as `agent.conf.tmp`.

Example output:

```
verify-agent-conf: Verifying [etc/shared/default/agent.conf]
verify-agent-conf: OK
```

Workflow (from the centralized configuration page): edit the group file under a temporary name such as `agent.conf.tmp` so the manager does not distribute an incomplete or invalid configuration, validate it with `verify-agent-conf -f <path to agent.conf.tmp>`, fix any issues, then rename it to `agent.conf`. The manager then detects the new configuration and distributes it to all agents in the group.

Failure mode: running it with no option only covers files that already live in group folders under `/var/ossec/etc/shared`; a file kept elsewhere needs `-f`.

## Checked

2026-11-08: confirmed against the verify-agent-conf reference page (read in full) and the temporary-file, validate and rename sequence on the Centralized configuration page (partial read: the section on creating and validating group configuration only). Removed the unsupported "syntax and structure errors" wording.
Method: documentation only; no commands were run.
