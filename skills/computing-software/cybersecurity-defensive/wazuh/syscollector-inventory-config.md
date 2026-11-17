---
id: computing-software.cybersecurity-defensive.wazuh.syscollector-inventory-config
name: syscollector-inventory-config
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [syscollector, system-inventory, inventory-harvester, max-eps, scan-on-start]
level: practitioner
status: docs-checked
description: "Configure Wazuh system inventory: Syscollector agent defaults and toggles, centralized override, and the manager indexer block."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/system-inventory/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Agent side: Syscollector is enabled by default. Local config paths: `/var/ossec/etc/ossec.conf` (Linux), `ossec.conf` in the agent install directory (`ossec-agent` under Program Files (x86) by default, Windows), `/Library/Ossec/etc/ossec.conf` (macOS). Centralized config (for the default group, `/var/ossec/etc/shared/default/agent.conf` on the server) takes precedence over local settings.

Defaults: `disabled` no; `interval` 1h (s, m, h, d); `scan_on_start` yes; `max_eps` 10 events per second (integer 0 to 1000000). `ports` defaults to yes; the shipped agent `ossec.conf` sets `all="yes"` (all ports), while omitting the attribute scans listening ports only. Other toggles defaulting to yes: `hardware`, `os`, `network`, `packages`, `processes`, `users`, `groups`, `services`, `browser_extensions`. Windows systems can also use `<hotfixes>` (details are on a separate docs page, not checked here).

Restart the agent after local changes; with centralized configuration no manual restart is required because the agent reloads automatically.

Manager side: the Wazuh Inventory Harvester forwards data through the `<indexer>` block, enabled by default (it can be missing on old configs or if vulnerability detection was disabled at install). Settings: `<enabled>yes</enabled>`, `<hosts>` and `<ssl>` with `certificate_authorities`, `certificate`, `key` under `/etc/filebeat/certs/`. With several indexer nodes the first host is preferred and the next is used on failure.

Store credentials by piping each value into `/var/ossec/bin/wazuh-keystore -f indexer -k username` and `-k password`. Test the connection from the server with curl against `https://<INDEXER_IP_ADDRESS>:9200/_cluster/health`; a failure means the server cannot send inventory data to the indexer, and `-k` can be used to check whether the problem is certificates. Apply with `systemctl restart wazuh-manager`.

## Checked

2026-11-08: confirmed against the Wazuh docs page System inventory: Configuration (read in full): config paths, centralized precedence, every Syscollector default and range, the manager indexer block, failover, keystore commands, the curl health check and restart. Corrected the ports default (shipped config sets all=yes; omitting the attribute scans listening ports only) and the macOS path. The hotfixes option is only pointed to, not verified here.
Method: documentation only; no commands were run.
