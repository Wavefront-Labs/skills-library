---
id: computing-software.systems-network-administration.network-design.byod-onboarding-and-segmentation
name: byod-onboarding-and-segmentation
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, segmentation, byod, nac, mdm, device-onboarding, guest-network]
level: practitioner
status: docs-checked
description: "Let personal devices onto the network safely: separate SSID/VLAN or NAC roles, onboarding with certificates or MDM, internet-only access and app access via ZTNA."
sources:
  - https://csrc.nist.gov/pubs/sp/800/46/r2/final
  - https://www.ncsc.gov.uk/collection/device-security-guidance/bring-your-own-device
  - https://www.cisco.com/c/en/us/td/docs/security/ise/3-2/admin_guide/b_ise_admin_3_2/b_ISE_admin_32_byod.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BYOD onboarding and segmentation

## Principles
- Treat personal devices as untrusted; give access to services, not to the internal network.
- Protect corporate data at the app level (MAM, conditional access) rather than owning the device.

## Network patterns
| Pattern | Access | Effort |
|---|---|---|
| Guest-style BYOD SSID / VLAN | internet only; corporate apps via SaaS or ZTNA | low |
| NAC-onboarded (for example Cisco ISE) | user registers device, gets a certificate (EAP-TLS) and a BYOD role with limited internal access | medium |
| MDM-enrolled | compliance check gates access; Wi-Fi profile pushed | medium |

## Onboarding flow (NAC example)
1. User joins an onboarding SSID or web portal with corporate credentials.
2. NAC provisions a device certificate and Wi-Fi profile (native supplicant provisioning).
3. Device reconnects to the secure SSID with EAP-TLS; RADIUS returns the BYOD authorisation result (for example a VLAN or ACL).
4. Device registered with owner; limit devices per user; lost-device portal for revocation.

## Policy for the BYOD segment
- Client isolation; internet allowed; DNS filtering.
- Internal: only published apps via reverse proxy/ZTNA; no SMB/RDP into server VLANs.
- Bandwidth/QoS limits as needed.
- Logging tying IP to user (RADIUS accounting to the firewall's user identity).

## Verify
- [ ] Onboarded BYOD device lands in the BYOD role, reaches only allowed apps; revoking its certificate blocks it immediately.

## Checked

2026-10-28: Confirmed in the Cisco ISE 3.2 BYOD guide: native supplicant provisioning, a device certificate used for EAP-TLS with a Wi-Fi profile enforcing EAP-TLS, an employee limit on registered devices, and certificate revocation when a device is reported lost or stolen. The NIST SP 800-46 and NCSC pages gave only abstracts or no matching text, so the attribution of the principles to them was removed. Removed: ClearPass, Intune and Jamf, and the SGT/dACL authorisation names.
Method: documentation only; no commands were run.
