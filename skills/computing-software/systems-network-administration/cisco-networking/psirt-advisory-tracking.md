---
id: computing-software.systems-network-administration.cisco-networking.psirt-advisory-tracking
name: psirt-advisory-tracking
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, psirt, security-advisories, cisco-software-checker, openvuln-api, cvss, kev, patch-management]
level: practitioner
status: draft
description: "Track Cisco PSIRT advisories against your estate: Software Checker, the openVuln API, mapping versions and enabled features, prioritising with CVSS and CISA KEV, and mitigation."
sources:
  - https://sec.cloudapps.cisco.com/security/center/publicationListing.x
  - https://developer.cisco.com/docs/psirt/
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracking PSIRT advisories

Network devices are prime targets (IOS XE web UI CVE-2023-20198 compromised tens of thousands of
devices within days). You need to know within hours which of your devices an advisory affects.

## Inventory first
Per device: platform, exact software version, and enabled features (web UI, Smart Install, SNMP,
IKE, VPN, NAT ALGs). Pull from your source of truth or `show version`/`show running-config` via
automation; feature exposure decides real impact.

## Cisco Software Checker
https://sec.cloudapps.cisco.com/security/center/softwarechecker.x : select platform type and
versions (or paste `show version`), get all advisories affecting them plus the first fixed release.
Bundled publications (March and September for IOS/IOS XE) arrive twice a year; out-of-cycle
critical advisories any time.

## Automate with the openVuln API
```
TOKEN=$(curl -s -X POST https://id.cisco.com/oauth2/default/v1/token \
  -d grant_type=client_credentials -d client_id=$ID -d client_secret=$SECRET | jq -r .access_token)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://apix.cisco.com/security/advisories/v2/OSType/iosxe?version=17.9.4" | jq '.advisories[] | {advisoryId, sir, cvssBaseScore, firstFixed}'
```
Run daily against each distinct version in the inventory; open tickets for new matches.

## Prioritise
1. In CISA KEV (actively exploited) or Cisco marks "exploited in the wild": emergency.
2. Critical/High SIR with the vulnerable feature enabled and reachable from untrusted networks.
3. Others: next maintenance cycle.
Read the advisory's "Vulnerable products" and "Determine the configuration" sections: many bugs
need a specific feature (e.g. `ip http server`).

## Mitigate when you cannot upgrade yet
Workarounds in the advisory: disable the feature (`no ip http server`, `no vstack`), restrict
access with ACLs/CoPP, management plane in a VRF reachable only from jump hosts. Check for
indicators of compromise listed in the advisory (implants, unknown local users).

## Verify
- [ ] Every device version is checked against advisories daily, and each critical finding has an
  upgrade or documented mitigation with a date.
