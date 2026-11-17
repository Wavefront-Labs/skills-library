---
id: computing-software.cybersecurity-defensive.network-defence.downloadable-acl
name: downloadable-acl
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [downloadable-acl, dacl, dynamic-vlan, radius-authorization, cisco-ise, network-access-control, filter-id]
level: practitioner
status: docs-checked
description: "Enforce per-session access with RADIUS authorisation: dynamic VLAN assignment, Filter-Id, Cisco ISE downloadable ACLs and SGTs, and testing the results."
sources: ["https://www.cisco.com/c/en/us/td/docs/security/ise/3-3/admin_guide/b_ise_admin_3_3/b_ISE_admin_33_segmentation.html", "https://datatracker.ietf.org/doc/html/rfc3580"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Downloadable ACLs and dynamic VLANs

After 802.1X/MAB succeeds, the RADIUS Access-Accept tells the switch what the session may do.

## Options
| Mechanism | RADIUS attributes | Use |
|---|---|---|
| Dynamic VLAN | `Tunnel-Type=VLAN(13)`, `Tunnel-Medium-Type=802`, `Tunnel-Private-Group-ID=<vlan>` (RFC 3580) | Coarse segmentation (corp / IoT / quarantine) |
| Downloadable ACL (dACL) | Configured in Cisco ISE and referenced by an authorization profile (DACL Name) | Per-role filtering on the port without a VLAN change |
| Filter-Id | `Filter-Id=<acl-name>`; in ISE it names an ACL that already exists on the NAD | ACL predefined on the switch |
| SGT (TrustSec) | `cisco-av-pair=cts:security-group-tag` | Scalable group policy enforced elsewhere |

## Details from the sources
- RFC 3580: the VLAN ID is 12 bits (1 to 4094) and, because `Tunnel-Private-Group-ID` is a string, it is
  encoded as a string; the Tag field must be filled in as RFC 2868 describes.
- Cisco ISE 3.3: create dACLs under Policy > Policy Elements > Results > Downloadable ACLs, then reference
  them from an authorization profile under Policy > Policy Elements > Results > Authorization Profiles.
  "Check DACL Syntax" validates the entries. Default DACLs include PERMIT_ALL_IPV4_TRAFFIC,
  PERMIT_ALL_IPV6_TRAFFIC, DENY_ALL_IPV4_TRAFFIC and DENY_ALL_IPV6_TRAFFIC; defaults cannot be changed but can
  be duplicated.
- Once a dACL is used in a policy you cannot change its type or delete it; duplicate it to change the type,
  or remove it from policies first.
- If a dACL named in an authorization profile does not exist in ISE, authorization fails and ISE sends an
  Access-Reject (see the Live Log Details page and the AAA Diagnostics report). An empty dACL used in an IdP
  authorization policy also fails authorization.
- ACL (Filter-ID) in an ISE authorization profile specifies an ACL on the NAD; for Cisco devices ISE says to
  add the `.in` suffix when entering the text.

## Gotchas
- Dynamic VLAN changes after the client got a DHCP lease from the old VLAN need a port bounce or CoA reauth.
- Check your switch platform's documentation for dACL scale limits and any required device tracking.
- Version dACL names deliberately, since ISE will not let you edit the type of one in use.

## Verify
- [ ] The switch's session output shows the dACL or VLAN applied to the port (command names differ by platform).
- [ ] The downloaded ACL shows hit counters when you test allowed and denied traffic.

## Checked
Checked 2026-11-09 against RFC 3580 (VLAN assignment attributes and encoding) and the Cisco ISE 3.3
Administrator Guide segmentation chapter (dACL configuration, authorization profile, failure behaviour,
Filter-ID, cisco-av-pair security-group-tag). Removed: the Aruba role row (ClearPass page returned 403), the
`ACS:CiscoSecure-Defined-ACL` attribute string, the example ACE list, the IOS commands and TCAM and device
tracking claims, which these pages do not confirm.
Method: docs-checked 2026-11-09 against RFC 3580 and the Cisco ISE 3.3 segmentation chapter.
