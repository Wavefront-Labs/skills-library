---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortimanager-policy-packages-and-install
name: fortimanager-policy-packages-and-install
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [policy-package, fortimanager, installation-targets, install-preview, adom-revision, policy-and-objects, jsonrpc]
level: practitioner
status: draft
description: "Create FortiManager policy packages, assign installation targets, preview and install, and automate with the JSON-RPC API."
sources: ["https://docs.fortinet.com/document/fortimanager/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: reviewed, repeatable policy rollout to many FortiGates.

Workflow
1. Policy & Objects > Policy Packages: create a package in the ADOM (global header/footer policies from the Global ADOM optionally).
2. Add policies and objects. Use Normalize (per-device mappings) for interfaces and VIPs that differ by site.
3. Set Installation Targets (devices and VDOMs).
4. Install Preview shows the CLI diff for each target; then Install Policy Package & Device Settings.
5. Use ADOM Revisions to snapshot before major changes and Revision History per device to roll back.

JSON-RPC example (read policies in a package):
```
curl --cacert ca.pem -H "Content-Type: application/json" https://fmg.example.com/jsonrpc -d '{"method":"get","params":[{"url":"/pm/config/adom/root/pkg/corp/firewall/policy"}],"session":"<SESSION>","id":1}'
```
Log in first with `{"method":"exec","params":[{"url":"/sys/login/user","data":{"user":"api","passwd":"<PASSWORD>"}}]}`, or use an API token header.

Gotchas
- Out-of-sync device config (changed locally) is overwritten on install; retrieve first (Device Manager > Retrieve Config) if local changes should be kept.
- Install failures usually come from missing mapped interfaces or dependent objects.
- Workspace mode locks ADOMs per admin; remember to save and unlock.

## Verify
After install, the device shows Policy Package Status Synchronised and `show firewall policy` on the FortiGate lists the new rules.
