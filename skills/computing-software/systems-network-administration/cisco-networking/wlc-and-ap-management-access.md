---
id: computing-software.systems-network-administration.cisco-networking.wlc-and-ap-management-access
name: wlc-and-ap-management-access
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst-9800, wireless, wlc-management, ap-console, ap-ssh, management-user, ap-profile]
level: practitioner
status: draft
description: "Secure management access to Catalyst 9800 WLCs and APs: WebUI and SSH users, AP SSH/console credentials in the AP join profile, and recovering a stuck AP."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg.html
  - https://www.cisco.com/c/en/us/support/docs/wireless/catalyst-9800-series-wireless-controllers/215072-configure-ap-ssh-and-console-access.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WLC and AP management access

## The controller
9800 is IOS-XE: SSH, AAA, ACLs work like any IOS-XE box (see ssh-v2-setup and tacacs skills).
- WebUI on HTTPS: `ip http secure-server`, `ip http authentication aaa` (or local), and
  restrict with `ip http access-class ipv4 MGMT-HOSTS`.
- Use the dedicated service port (Gi0) in the Mgmt-intf VRF for out-of-band access on
  appliances.
- Management over wireless is disabled by default; leave it so.

## The APs (credentials pushed by the WLC)
APs use credentials from the **AP join profile**, not their own config:
```
ap profile default-ap-profile
 mgmtuser username apadmin password 0 <PW> secret 0 <ENABLE_SECRET>
 ssh                                   ! enable AP SSH (off by default)
```
WebUI: Configuration > Tags & Profiles > AP Join > Management > Device/User.
Without this, APs fall back to factory `Cisco/Cisco` until they join, then use the profile.

## AP console when it will not join
- Console cable (RJ-45 or micro-USB, 9600 8N1 by default on most Cisco APs).
- Default creds before join: `Cisco` / `Cisco`.
- Useful commands: `show capwap client rcb`, `show capwap ip config`,
  `capwap ap primary-base <WLC name> <WLC IP>`, `capwap ap erase all` (clear static config).
- Reset button held at boot = factory reset.

## Verify
```
show ap config general | include Username|SSH|Telnet
show ap summary
```
SSH to an AP with the profile user succeeds; telnet is disabled.
- [ ] AP SSH enabled only where needed, non-default AP creds pushed, WLC WebUI restricted to management hosts.
