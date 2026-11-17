---
id: computing-software.cybersecurity-defensive.nessus.linking-scanners-to-tenable-platforms
name: linking-scanners-to-tenable-platforms
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-deployment, scanner-linking, tenable-vulnerability-management, tenable-sc, linking-key, scanner-groups, managed-scanner]
level: practitioner
status: docs-checked
description: "Link Nessus scanners to Tenable Vulnerability Management or Security Center, organise scanner groups and confirm scans route through the right scanner."
sources: ["https://docs.tenable.com/nessus/Content/LinkToTenableVulnerabilityManagement.htm", "https://docs.tenable.com/nessus/Content/LinkToTenableSecurityCenter.htm", "https://docs.tenable.com/nessus/Content/NessusCLI.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linking scanners to Tenable platforms

**Goal:** scanners in every network segment are managed centrally, so scans can be run from a scanner that can reach the targets.

## Tenable Vulnerability Management (cloud)
1. In Tenable Vulnerability Management open Settings > Sensors > Linked Scanners > Add Nessus Scanner and copy the linking key.
2. In the Nessus setup wizard choose "Link Nessus to another Tenable product", set *Managed by* to Tenable One Vulnerability Management, paste the key and create the local administrator account. Or use the CLI:
   `nessuscli managed link --key=<linking-key> --cloud` (use `--fedcloud` for a FedRAMP instance, which must be linked from the command line).
3. If the scanner was registered or linked before, unlink it or run `nessuscli fix --reset-all` first. `--reset-all` removes users, data, settings and configuration; export scan data and back up first. A CLI link creates no web UI user; add one with `nessuscli adduser <username>`.
4. Firewalls: Tenable recommends allowing `*.cloud.tenable.com` (with the wildcard), which covers `sensor.cloud.tenable.com`. Scanners in mainland China connect through `sensor.cloud.tenablecloud.cn`.

## Tenable Security Center (on-prem)
1. In the setup wizard choose "Link Nessus to another Tenable product" and set *Managed by* to Tenable.sc, then create the local administrator account.
2. Add the scanner in Tenable Security Center as described in "Add a Nessus Scanner" in the Security Center user guide.
3. Security Center does not send plugins to linked Nessus Managers; a Nessus Manager pulls plugins from Tenable's plugin sites, so it needs internet access or a manual offline update.

## CLI options and status
`nessuscli managed link --key=<key> --host=<host> --port=<port>` accepts optional `--name`, `--ca-path`, `--groups` (existing scanner groups, case-sensitive, comma-separated), `--scan-zones` (existing Security Center scan zones, case-sensitive), `--profile-uuid` and proxy options (`--proxy-host`, `--proxy-port`, `--proxy-username`, `--proxy-password`, `--proxy-agent`). A scanner that is already registered cannot be linked through the CLI without a reset. `nessuscli managed status` shows status; `nessuscli managed unlink` unlinks.

## Gotchas
- Once linked, a scanner stays linked until you unlink it.
- Linking to a different manager requires unlinking (or `fix --reset-all`) first.

## Verify
- [ ] Scanner shows online in the managing platform.
- [ ] A test scan targeted at the scanner or its group runs from it (check scan details).

## Checked
2026-11-02. Confirmed from Tenable Nessus 10.12 pages "Link to Tenable One Vulnerability Management", "Link to Tenable Security Center" and the Nessus CLI page (Managed Scanner Commands). Removed (not stated there): "outbound HTTPS 443 only, no inbound rules", scanner-group-per-zone advice, scan-zone routing and overlap behaviour, "Security Center pushes plugins and policies to scanners", IPS/stateful-firewall placement advice, proxy-before-link behaviour.

Method: documentation only; no commands were run.
