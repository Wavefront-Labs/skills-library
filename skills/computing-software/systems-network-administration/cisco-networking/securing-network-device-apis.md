---
id: computing-software.systems-network-administration.cisco-networking.securing-network-device-apis
name: securing-network-device-apis
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, api-authentication, restconf, netconf, gnmi, aaa, certificates, mtls, token-authentication, ios-xe, api-security]
level: practitioner
status: draft
description: "Secure device APIs (NETCONF, RESTCONF, gNMI) on IOS XE: AAA-backed users with least privilege, certificates and mTLS, ACLs, and protecting automation credentials."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1712/b_1712_programmability_cg/m_1712_prog_restconf.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1712/b_1712_programmability_cg/m_1712_prog_gnmi.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Securing device APIs

## Authentication per interface
| API | Transport | Auth on IOS XE |
|---|---|---|
| NETCONF | SSH port 830 | AAA (local/TACACS+/RADIUS) usernames; SSH keys possible |
| RESTCONF | HTTPS 443 | HTTP basic auth over TLS, checked via `ip http authentication aaa`/local |
| gNMI | gRPC over TLS (9339) | mutual TLS (client certificates) plus username/password metadata |

There is no OAuth/token on the device itself for RESTCONF; controllers (Catalyst Center, SD-WAN
Manager) use token auth on their own APIs (`X-Auth-Token`, JSESSIONID+XSRF token).

## Least privilege
- API users need privilege 15 for config on many releases. Use AAA command authorization or NACM
  (`ietf-netconf-acm`) rules to limit what they can read/write where supported.
- Separate accounts per tool (Ansible, monitoring, Terraform) so you can revoke one and audit actions.
- Accounting: `aaa accounting commands 15 default start-stop group TACACS` captures API-driven changes as commands.

## Transport hardening
```
ip http secure-server
ip http secure-trustpoint API-TP             ! CA-signed cert
no ip http server
ip http access-class ipv4 AUTOMATION-HOSTS
netconf-yang ssh ipv4 access-list name AUTOMATION-HOSTS    ! release-dependent syntax
gnxi
 gnxi secure-trustpoint GNMI-TP
 gnxi secure-client-auth                     ! require client certificates (mTLS)
 gnxi secure-server
```
Clients must verify the device certificate (no `verify=False` / `hostkey_verify=False` in production).

## Credentials in automation
- Store in a vault (HashiCorp Vault, Ansible Vault, CyberArk), inject at runtime; never in Git.
- Rotate service account passwords; prefer certificates/keys where the API supports them.
- Restrict source IPs to automation servers; log failed logins (`login on-failure log`).

## Verify
- [ ] API reachable only from automation subnets; plain HTTP closed.
- [ ] Each tool has its own account; TACACS+ accounting shows its changes.
- [ ] Clients validate certificates (test with a wrong cert: connection refused).
