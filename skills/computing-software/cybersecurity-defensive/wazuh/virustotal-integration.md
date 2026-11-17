---
id: computing-software.cybersecurity-defensive.wazuh.virustotal-integration
name: virustotal-integration
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [virustotal, integration, integrator, api-key, rule-87105, syscheck-group]
level: practitioner
status: docs-checked
description: "Enrich FIM alerts with VirusTotal using the Wazuh integration block, rules 87101 to 87105, public API quota limits and data exposure."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/malware-detection/virus-total-integration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On the server `/var/ossec/etc/ossec.conf`, add the following (see the Wazuh External API integration page for the Integrator module):

```xml
<integration>
  <name>virustotal</name>
  <api_key>API_KEY</api_key>
  <group>syscheck</group>
  <alert_format>json</alert_format>
</integration>
```

Monitor folders with `<directories check_all="yes" realtime="yes">` in `<syscheck>`, then restart `wazuh-manager`.

Rules: 87101 public API rate limit reached (error 204); 87102 check credentials (error 403); 87104 file found, no positives; 87105 engines detected the file (level 12). A "no records" alert also exists.

Public API limits: 500 requests per day and 4 per minute. It is not for commercial products or business workflows that do not add new files, and using multiple accounts to bypass limits is prohibited. A premium private API has higher limits.

Gotchas:
- Only FIM alerts in the `syscheck` group trigger lookups, and only the file hash is sent.
- With many FIM events the daily quota runs out fast, producing 87101.
- Files unknown to VirusTotal give a "no records" alert, not a verdict.
- The API key is set directly in `ossec.conf` in the `<integration>` block.
- Alerts go to `/var/ossec/logs/alerts/alerts.log` and `alerts.json`. To also log integration activity in `/var/ossec/logs/integrations.log`, set `integrator.debug=1` in `/var/ossec/etc/local_internal_options.conf` and restart the manager.
- Use the EICAR test file only in a sandbox.

## Checked

2026-11-08. Read the whole VirusTotal integration page. Confirmed: integration block, syscheck directories attributes, manager restart, rule IDs and levels (87101 error 204, 87102 error 403, 87104, 87105 level 12), public API limits and terms, hash-only lookup, alert files, integrator.debug=1 for integrations.log. Removed: the plain-text key-storage claim (not on the page). The Integrator-module enabling steps are on the separate External API integration page, not read.
Method: documentation only; no commands were run.
