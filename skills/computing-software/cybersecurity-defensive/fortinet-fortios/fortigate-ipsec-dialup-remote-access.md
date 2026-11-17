---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ipsec-dialup-remote-access
name: fortigate-ipsec-dialup-remote-access
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [ipsec-dialup, fortios, forticlient, mode-config, ike-v2-eap, xauth, remote-access-ipsec]
level: practitioner
status: draft
description: "Configure FortiGate dialup IPsec for FortiClient with mode-config addresses, xauth or EAP and user groups."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: IPsec remote access as the replacement for SSL VPN.

```
config vpn ipsec phase1-interface
    edit "dialup"
        set type dynamic
        set interface "port1"
        set ike-version 2
        set peertype any
        set net-device disable
        set mode-cfg enable
        set ipv4-start-ip 10.200.0.10
        set ipv4-end-ip 10.200.0.200
        set ipv4-netmask 255.255.255.0
        set dns-mode auto
        set eap enable
        set eap-identity send-request
        set authusrgrp "ENG"
        set proposal aes256-sha256
        set dhgrp 14
        set psksecret <PSK>
    next
end
config vpn ipsec phase2-interface
    edit "dialup"
        set phase1name "dialup"
        set proposal aes256-sha256
        set src-subnet 0.0.0.0 0.0.0.0
    next
end
```
Policy from `dialup` to the internal zone with source `10.200.0.0/24` and the group. FortiClient (VPN or EMS-deployed) selects the gateway and credentials.

Gotchas
- With IKEv1 use `xauthtype auto` and aggressive mode only with a certificate or strong PSK; IKEv2 EAP with certificates or SAML is preferred.
- Identical PSK for all users is weak; use certificates plus user auth.
- Pool must not overlap the LAN.

## Verify
```
diagnose vpn ike gateway list
diagnose vpn tunnel list
get vpn ipsec tunnel summary
```
Connect a client and verify the assigned address from the pool.
