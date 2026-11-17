---
id: computing-software.cybersecurity-defensive.network-defence.host-intrusion-detection
name: host-intrusion-detection
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [host-intrusion-detection, hids, wazuh, ossec, rootcheck, log-analysis, active-response]
level: practitioner
status: draft
description: "Run host intrusion detection with Wazuh/OSSEC: agent deployment, log analysis rules and decoders, FIM, rootcheck/SCA, active response caution and SIEM integration."
sources: ["https://documentation.wazuh.com/current/index.html", "https://documentation.wazuh.com/current/user-manual/ruleset/index.html", "https://www.ossec.net/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Host intrusion detection (Wazuh / OSSEC)

## Components
- Agent on each host: collects logs (syslog, Windows event channels, app logs), file integrity monitoring (syscheck), rootcheck/policy monitoring, Security Configuration Assessment (SCA), inventory, vulnerability detection.
- Manager: decoders + rules engine, alerts (`alerts.json`), active response.

## Deploy
- Enrol agents with a password or certificate (`/var/ossec/etc/authd.pass`), group them (linux-web, windows-dc) and push group `agent.conf` from the manager (`/var/ossec/etc/shared/<group>/agent.conf`).
- Windows: collect `Security`, `System`, `Microsoft-Windows-Sysmon/Operational`, `Microsoft-Windows-PowerShell/Operational` via `<localfile><location>...</location><log_format>eventchannel</log_format>`.

## Rules
- Custom rules in `local_rules.xml` (IDs 100000+); child rules with `<if_sid>`, frequency correlation (`frequency`, `timeframe`, `same_source_ip`).
```xml
<group name="local,sshd,">
  <rule id="100100" level="10" frequency="8" timeframe="120">
    <if_matched_sid>5716</if_matched_sid>
    <same_source_ip />
    <description>SSH brute force from $(srcip)</description>
    <mitre><id>T1110</id></mitre>
  </rule>
</group>
```
- Test with `/var/ossec/bin/wazuh-logtest`.

## Active response
Blocking IPs automatically (firewall-drop) is easy to abuse (spoofed sources, locking out admins). Use
with allow-lists (`<white_list>`), short timeouts, and only for high-confidence rules.

## Integration
Forward `alerts.json` to the SIEM (Filebeat/Wazuh indexer, or syslog output); map rule level to severity.

## Gotchas
- Noisy default rules on busy servers; tune with level overrides in local rules, not by editing the stock ruleset (overwritten on upgrade).
- Agents running as root/SYSTEM are attractive targets; protect the manager like a SIEM.

## Verify
- [ ] Agent status all active (`agent_control -l`).
- [ ] `wazuh-logtest` confirms custom rules; test events produce alerts in the SIEM.
