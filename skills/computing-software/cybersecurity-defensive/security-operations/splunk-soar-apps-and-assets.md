---
id: computing-software.cybersecurity-defensive.security-operations.splunk-soar-apps-and-assets
name: splunk-soar-apps-and-assets
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [splunk-soar, splunk-soar-apps, soar-automation, phantom, assets, connectors, playbooks]
level: practitioner
status: draft
description: "Configure Splunk SOAR apps and assets: installing connectors, asset credentials and automation users, testing connectivity, action results and custom app development basics."
sources: ["https://docs.splunk.com/Documentation/SOAR/current/Admin/Apps", "https://docs.splunk.com/Documentation/SOAR/current/Admin/Assets", "https://docs.splunk.com/Documentation/SOARonprem/latest/DevelopApps/Overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Splunk SOAR apps and assets

## Concepts
- **App**: connector package exposing actions (e.g. `lookup ip`, `block ip`, `disable user`).
- **Asset**: a configured instance of an app (URL, credentials, proxy); playbooks call actions on
  assets. One app can have several assets (prod/test firewall).
- Actions return action results with data paths (`action_result.data.*.attribute`) used in later blocks.

## Setup
1. Apps > New Apps: install from Splunkbase (most connectors are on Splunkbase or bundled).
2. Asset Settings: name (playbooks reference it), product vendor/name, credentials. Use dedicated
   least-privilege service accounts per asset.
3. **Asset Settings > Approval Policy**: require approval for destructive actions (block, delete,
   disable) with approvers and SLA.
4. **Ingest settings** for polling assets (email, SIEM) with label and interval.
5. Test connectivity button; check result in the asset view.

## Automation user
Playbooks run as the `automation` user; restrict role permissions for which labels/containers
it can modify. Use separate assets for read vs write where vendor supports scoped credentials.

## Custom apps
App Wizard or SOAR App Editor generates connector skeleton (Python, `BaseConnector`, JSON app
metadata). Implement `handle_action`, return results via `ActionResult`. Package and install as
tarball. Test with `phenv` CLI and unit tests.

## Gotchas
- App upgrades can change action outputs; pin versions in production and test playbooks after upgrade.
- Credentials stored in assets are encrypted, but admins can export; restrict admin role.
- Proxy settings are per asset or global environment variables; mismatches cause intermittent failures.

## Verify
Each asset's test connectivity passes; a test playbook runs a read action on every asset and an
approval-gated write action in the test asset.
