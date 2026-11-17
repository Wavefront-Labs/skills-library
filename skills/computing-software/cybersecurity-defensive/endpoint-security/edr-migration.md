---
id: computing-software.cybersecurity-defensive.endpoint-security.edr-migration
name: edr-migration
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [edr-migration, edr-replacement, coexistence, passive-mode, agent-rollout, detection-parity, edr-operations]
level: advanced
status: draft
description: "Migrate between EDR vendors: coexistence and passive modes, staged rollout, detection and response parity, exclusions transfer, uninstall of the old agent and rollback."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/switch-to-mde-overview", "https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility", "https://attack.mitre.org/resources/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EDR vendor migration

## Plan
1. **Inventory:** every device with the old agent (and those without - migrations surface gaps), OS versions, special groups (VDI, servers, OT-adjacent).
2. **Parity matrix:** detections (custom rules, IOAs), response actions (isolation, RTR scripts), integrations (SIEM, SOAR, ticketing), device control/firewall features, exclusions, reporting. Rebuild custom detections in the new platform's language.
3. **Coexistence:** run both briefly. Put one product in passive/detect-only mode and add mutual exclusions per both vendors' guidance (e.g. Defender Antivirus passive mode `ForceDefenderPassiveMode=1` on servers when a third-party AV is active). Never run two active AV engines with real-time blocking.
4. **Staged rollout:** pilot (IT/security) -> 10% -> 50% -> 100% per OS; deploy via existing tools (Intune, SCCM, Jamf, Ansible).
5. **Switch:** new agent to active/block mode, old agent removed with its uninstall token/passphrase (tamper protection!). Clean up leftovers (drivers, services).
6. **SOC readiness:** runbooks, training, alert routing, on-call; dashboards of coverage.

## Validation
- Atomic Red Team / vendor test detections per wave to confirm detection and blocking.
- Compare coverage counts daily: devices reporting to new console vs asset inventory.

## Rollback
Keep the old agent packages and tokens until 100% migration plus a stable period; documented rollback
per group.

## Gotchas
- Tamper protection on the old agent blocks scripted uninstall; collect maintenance tokens in bulk first (vendor APIs).
- Servers with fragile apps need per-app exclusions re-validated in the new product.
- Gaps during the switch: avoid any window where neither product is active.

## Verify
- [ ] Coverage = asset inventory (within agreed tolerance) on the new platform.
- [ ] Old agent absent from all devices; licences decommissioned.
