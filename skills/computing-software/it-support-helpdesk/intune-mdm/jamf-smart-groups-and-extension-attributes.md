---
id: computing-software.it-support-helpdesk.intune-mdm.jamf-smart-groups-and-extension-attributes
name: jamf-smart-groups-and-extension-attributes
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, jamf, jamf-pro, jamf-smart-groups, extension-attributes, static-groups, advanced-search, inventory-criteria, macos-management, jamf-recon]
level: practitioner
status: draft
description: "Target Macs with Jamf Pro smart groups and extension attributes: criteria logic, script EAs that report custom data, inventory timing, and avoiding slow or circular groups."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Smart_Groups.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Computer_Extension_Attributes.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Simple_Searches.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jamf-smart-groups-and-extension-attributes

Goal: groups that automatically contain exactly the Macs that need an
action ("needs Chrome update", "FileVault off"), driven by inventory.

## Smart group basics
Computers → Smart Computer Groups → New. Criteria rows joined with
**and/or**, with parentheses for grouping. Examples:
- `Application Title` `is` `Google Chrome.app` **and** `Application Version`
  `less than` `129.0` → patch target.
- `FileVault 2 Status` `is not` `All Partitions Encrypted` → remediation
  policy and alert.
- `Last Inventory Update` `more than x days ago` `30` → stale devices.
Membership is evaluated against the inventory Jamf already holds (on save
and whenever a computer submits inventory with `jamf recon`). If the Mac's
real state changed since its last inventory, the group is wrong until the
next recon. Use "Send email notification on membership change" for alerts.

## Static groups
Hand-picked members — for pilots/test rings. Don't use for anything that
should be attribute-driven.

## Extension attributes (EAs)
Settings → Computer Management → Extension Attributes → New. Input types:
text field, pop-up menu (manual), LDAP mapping, **Script**.
Script EA must print a `<result>` tag:
```bash
#!/bin/bash
# Report CrowdStrike sensor version
v=$(/Applications/Falcon.app/Contents/Resources/falconctl stats 2>/dev/null | awk '/version/{print $2; exit}')
echo "<result>${v:-Not Installed}</result>"
```
Script EAs run at **every inventory** on every Mac — keep them fast (<1 s),
no network calls, no `sudo` prompts. Use them as smart group criteria.

## Gotchas
- Nested smart groups ("member of" another smart group) chain inventory
  delays and can't be circular.
- "is"/"like" comparisons on versions are string compares — use the
  version-aware operators ("greater than" for Application Version) or
  normalise in the EA.
- Huge numbers of smart groups and script EAs slow the server and every
  recon.

## Verify
Group membership count matches an Advanced Computer Search with the same
criteria, and a test Mac moves in/out after `sudo jamf recon`.
