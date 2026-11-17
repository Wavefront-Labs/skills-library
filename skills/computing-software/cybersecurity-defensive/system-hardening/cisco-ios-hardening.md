---
id: computing-software.cybersecurity-defensive.system-hardening.cisco-ios-hardening
name: cisco-ios-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [network-device-hardening, cisco-ios-hardening, ios-xe, aaa, ssh, service-hardening, cisco-guide-to-harden-ios]
level: advanced
status: docs-checked
description: "Harden Cisco IOS and IOS XE devices: AAA with TACACS+, SSH v2 only, disable legacy services, secure passwords, logging, NTP and interface protections per Cisco's guide."
sources: ["https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cisco IOS / IOS XE hardening

**Goal:** a standard secure configuration applied to every router and switch, with auditable admin access. The
reference is Cisco's "Cisco Guide to Harden Cisco IOS Devices"; command availability varies by release, so confirm
each command on your platform.

## Baseline snippets
```
ip domain-name <DOMAIN>
crypto key generate rsa modulus 2048
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3
enable secret <strong>
username breakglass privilege 15 algorithm-type scrypt secret <strong>
!
aaa new-model
aaa authentication login default group tacacs+ enable
aaa authorization exec default group tacacs none
aaa authorization commands 15 default group tacacs none
aaa accounting commands 15 default start-stop group tacacs
tacacs-server host <TACACS_IP>
tacacs-server key <key>
!
no ip http server
no ip http secure-server          ! unless needed
no service pad
no ip finger
no cdp run                         ! or disable per untrusted interface: no cdp enable
no service tcp-small-servers
no service udp-small-servers
no ip bootp server
!
line vty 0 15
 transport input ssh
 access-class MGMT-ONLY in
 exec-timeout 10 0
line con 0
 exec-timeout 10 0
!
logging host <SYSLOG_IP>
logging buffered <size> 6
service timestamps log datetime msec localtime show-timezone
ntp server <NTP_IP>
```
Notes from the Cisco guide:
- Use `enable secret`, not `enable password`. `service password-encryption` and Type 7 passwords are only a
  Vigenere-style obfuscation; treat configs that contain them like cleartext. Use type 9 (scrypt) for local users
  where supported.
- Fallback: with `aaa authentication login default group tacacs+ enable`, the `enable` secret is used only if all
  TACACS+ servers are unavailable. The guide's authorization examples end in `none`; decide deliberately whether
  `none`, `local` or `enable` is acceptable for your lockout risk.
- `no service tcp-small-servers` / `no service udp-small-servers` matter only on old releases; small services are
  disabled by default from Cisco IOS 12.0.
- NTP: configure a trusted time source and use NTP authentication (`ntp authenticate`).

## Interfaces
`no ip redirects`, `no ip unreachables` and `no ip proxy-arp` on external interfaces; unicast reverse path
forwarding (`ip verify unicast source reachable-via <mode>`) at the edges.

## Smart Install
The guide covers disabling Smart Install (`no vstack`); do so unless you use it.

## Verify
- [ ] The running config shows `ip ssh version 2` and `transport input ssh` on every vty line.
- [ ] A config audit (golden config diff or your compliance scanner) has no failures.
- [ ] The software release is a Cisco-recommended, supported version with no open critical security advisories.

## Checked
2026-10-31. Checked each command against "Cisco Guide to Harden Cisco IOS Devices" (SSH, AAA/TACACS+, method lists
and fallback, command authorization and accounting, small services, HTTP server, CDP, vty settings, logging, NTP,
`no vstack`, interface commands, uRPF, type 7/type 9 notes). Removed: `login block-for`, `security passwords
min-length`, `login on-failure/on-success log`, `enable algorithm-type`, 3072-bit RSA, "type 8", the CVE reference
and "heavily exploited" claim, named audit tools, and the CIS XE and NSA guide sources (not read).
Method: documentation only; no commands were run.
