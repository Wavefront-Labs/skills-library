---
id: computing-software.cybersecurity-defensive.system-hardening.junos-hardening
name: junos-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [junos-hardening, juniper, network-device-hardening, loopback-filter, routing-engine-protection, junos]
level: practitioner
status: draft
description: "Harden Juniper Junos devices: root and login classes, SSH-only management, loopback firewall filter protecting the routing engine, AAA, NTP, logging and unused services."
sources: ["https://www.juniper.net/documentation/us/en/software/junos/overview/topics/concept/junos-security-hardening.html", "https://www.juniper.net/documentation/us/en/software/junos/routing-policy/topics/example/firewall-filter-stateless-example-trusted-source-protecting-routing-engine.html", "https://www.cisecurity.org/benchmark/juniper", "https://public.cyber.mil/stigs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Junos hardening

## Accounts and AAA
```
set system root-authentication encrypted-password "<hash>"
set system login class NOC permissions [ view view-configuration ]
set system login user netops class super-user authentication encrypted-password "<hash>"
set system authentication-order [ tacplus password ]
set system tacplus-server 10.0.10.5 secret "<key>" source-address 10.0.0.1
set system login retry-options tries-before-disconnect 3 backoff-threshold 1 lockout-period 15
set system login message "Authorised access only"
set system login password minimum-length 14
```
Keep one local emergency account; disable root SSH login.

## Management plane services
```
set system services ssh root-login deny
set system services ssh protocol-version v2
set system services ssh connection-limit 10 rate-limit 4
set system services ssh ciphers [ aes256-gcm@openssh.com aes128-gcm@openssh.com ]
delete system services telnet
delete system services ftp
delete system services web-management http
set system services netconf ssh          # only if automation needs it
set system no-redirects
set system internet-options no-source-quench
```
Disable unused J-Web; if used, HTTPS only on the management interface.

## Protect the Routing Engine (lo0 filter)
A stateless firewall filter on `lo0` controls everything destined to the device itself:
```
set policy-options prefix-list MGMT-HOSTS 10.0.10.0/24
set firewall family inet filter PROTECT-RE term ssh from source-prefix-list MGMT-HOSTS protocol tcp destination-port ssh
set firewall family inet filter PROTECT-RE term ssh then accept
set firewall family inet filter PROTECT-RE term bgp from source-prefix-list BGP-PEERS protocol tcp port bgp
set firewall family inet filter PROTECT-RE term bgp then accept
set firewall family inet filter PROTECT-RE term ospf from protocol ospf
set firewall family inet filter PROTECT-RE term ospf then accept
set firewall family inet filter PROTECT-RE term icmp from protocol icmp
set firewall family inet filter PROTECT-RE term icmp then policer ICMP-1M accept
set firewall family inet filter PROTECT-RE term snmp ... ntp ... dns ...
set firewall family inet filter PROTECT-RE term default then count DENIED discard
set interfaces lo0 unit 0 family inet filter input PROTECT-RE
```
Do the same for `family inet6`. Apply with `commit confirmed 5` so a mistake rolls back automatically.

## Other settings
- NTP with authentication; `set system time-zone UTC`.
- SNMPv3 only with authPriv, or no SNMP; restrict clients.
- Syslog to central servers with `any notice; authorization info; interactive-commands any`;
  `set system syslog time-format millisecond year`.
- `set system ports console log-out-on-disconnect`; `set system ports auxiliary disable`.
- Routing protocol authentication (BGP TCP-AO/MD5, OSPF/IS-IS keys).
- Junos OS version on a supported, recommended release (JTAC recommended releases page).

## Verify
`show configuration system services` lists only SSH/NETCONF; from an unauthorised subnet SSH times out and
`show firewall filter PROTECT-RE` counts the drops; `show system login` shows no shared accounts; a CIS or STIG
scan passes.
