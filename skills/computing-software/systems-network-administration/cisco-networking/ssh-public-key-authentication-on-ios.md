---
id: computing-software.systems-network-administration.cisco-networking.ssh-public-key-authentication-on-ios
name: ssh-public-key-authentication-on-ios
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ssh, ssh-public-key, ip-ssh-pubkey-chain, key-based-authentication, device-access, automation-access]
level: practitioner
status: draft
description: "Log in to IOS/IOS XE with SSH keys: ip ssh pubkey-chain, key-hash vs key-string, RSA/ECDSA support by release, and pairing with AAA."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_ssh/configuration/xe-16/sec-usr-ssh-xe-16-book/sec-usr-ssh-sec-shell.html
  - https://www.cisco.com/c/en/us/support/docs/security-vpn/secure-shell-ssh/4145-ssh.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SSH public key authentication on IOS

## Prerequisites
SSH v2 working with password login first (hostname, domain name, RSA host key >= 2048 bits,
`ip ssh version 2`, VTY `transport input ssh`). See ssh-v2-setup-on-ios.

## Add a user key
```
ip ssh pubkey-chain
 username netadmin
  key-string
   AAAAB3NzaC1yc2EAAAADAQABAAABAQC... (paste the base64 body, split lines allowed)
  exit
 username automation
  key-hash ssh-rsa 8FB4F858DD7E5AFB372780EC653DB371      ! MD5 fingerprint form (older IOS)
```
`key-string` takes only the base64 blob (no `ssh-rsa` prefix, no comment); IOS stores it as a hash.
Generate with `ssh-keygen -t rsa -b 3072`; ECDSA (`ecdsa-sha2-nistp256`) and Ed25519 support
depends on the IOS XE release, so RSA is the safe common denominator.

## Authentication flow
- With `login local` / `aaa authentication login default local`, the user must exist in the
  pubkey-chain; a local `username` entry is still needed for authorization/privilege on many releases.
- With TACACS+/RADIUS, public key auth happens locally; authorization still goes to AAA (configure
  `aaa authorization exec default group TACACS local`).
- Disable password fallback for automation accounts only by giving them no password, or restrict
  methods per server:
```
ip ssh server algorithm authentication publickey keyboard password
```

## Client side
```
ssh -i ~/.ssh/id_rsa netadmin@<DEVICE>
# older IOS may need: -o PubkeyAcceptedAlgorithms=+ssh-rsa -o HostKeyAlgorithms=+ssh-rsa
```

## Verify
```
show ip ssh
show users
debug ip ssh                      ! "Publickey authentication succeeded"
```
- [ ] Key login works; wrong key falls back or fails as intended.
- [ ] Keys rotated/removed when staff leave (they are in the config: audit with `show run | section pubkey`).
