---
id: computing-software.systems-network-administration.patch-management.network-device-golden-image-versions
name: network-device-golden-image-versions
category: computing-software
field: systems-network-administration
product: patch-management
tags: [golden-image-version, recommended-release, network-device-upgrade, software-standard, cisco-suggested-release, network-compliance]
level: practitioner
status: draft
description: "Set and enforce golden (standard) software versions per network platform: choosing vendor-recommended releases, version compliance reporting, and planned upgrade waves."
sources:
  - https://www.cisco.com/c/en/us/support/docs/field-notices/
  - https://supportportal.juniper.net/s/article/Junos-Software-Versions-Suggested-Releases-to-Consider-and-Evaluate
  - https://sec.cloudapps.cisco.com/security/center/softwarechecker.x
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Golden image versions for network devices

**Goal:** every switch, router and firewall model runs one approved release, chosen for stability and security, so upgrades are planned rather than reactive.

## Choosing the release
- Start from the vendor's recommendation: Cisco "suggested release" (gold star on software download), Juniper JTAC recommended releases KB, Arista/Palo Alto/Fortinet recommended-release notes.
- Check it against security advisories (Cisco Software Checker, vendor PSIRT) and field notices.
- Prefer long-lived maintenance trains (e.g. extended maintenance releases) over feature releases.
- Test in a lab or on a few low-risk devices for a defined soak period.

## Document the standard
| Platform | Golden release | Approved alternates | Image hash | Review date |
|---|---|---|---|---|
| C9300 | 17.12.x | 17.9.x (until date) | SHA512 | quarterly |

## Compliance reporting
Collect versions automatically:
```yaml
- name: Gather IOS facts
  cisco.ios.ios_facts:
    gather_subset: min
- debug: msg="{{ inventory_hostname }} {{ ansible_net_version }}"
```
Or pull from NetBox/Nautobot plus NAPALM `get_facts`, or the vendor controller (DNA Center/Catalyst Center SWIM, Junos Space). Report devices off-standard by age.

## Upgrade waves
Lab -> non-critical access -> distribution -> core/edge, each with rollback plan and a window. Emergency PSIRT fixes may jump straight to a patched release with a shorter soak.

## Gotchas
- The golden release can itself become vulnerable; re-review on every critical advisory, not just quarterly.
- Hardware EOL models may not support the new standard; track them as exceptions with replacement dates.

## Verify
Compliance report shows >95% of devices on golden or approved alternates, with dated plans for the rest.
