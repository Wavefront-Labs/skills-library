---
id: computing-software.systems-network-administration.cisco-networking.ssh-algorithm-hardening
name: ssh-algorithm-hardening
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, ssh, ssh-algorithms, ssh-hardening, kex, ciphers, vulnerability-scan]
level: practitioner
status: draft
description: "Harden SSH on IOS XE: restrict KEX, ciphers, MACs and host key algorithms, RSA key size, SSH v2 only, timeouts, and verifying with ssh -vv and ssh-audit."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_ssh/configuration/xe-17/sec-usr-ssh-xe-17-book/sec-usr-ssh-sec-shell.html
  - https://github.com/jtesta/ssh-audit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SSH algorithm hardening on IOS XE

Vulnerability scanners flag network devices for SHA-1 MACs, CBC ciphers, diffie-hellman-group1/14
SHA-1 KEX and small RSA keys. IOS XE 16.x/17.x lets you choose.

## Configuration
```
ip ssh version 2
crypto key generate rsa modulus 3072 label SSH-KEY
ip ssh rsa keypair-name SSH-KEY
ip ssh server algorithm kex ecdh-sha2-nistp256 ecdh-sha2-nistp384 diffie-hellman-group16-sha512
ip ssh server algorithm encryption aes256-gcm aes128-gcm aes256-ctr aes128-ctr
ip ssh server algorithm mac hmac-sha2-512 hmac-sha2-256
ip ssh server algorithm hostkey rsa-sha2-512 rsa-sha2-256
ip ssh time-out 60
ip ssh authentication-retries 3
ip ssh dh min size 2048
```
Exact algorithm names available vary by release; `ip ssh server algorithm encryption ?` lists
them. Newer releases add `curve25519-sha256` KEX and `ssh-ed25519` host keys.

Client side (when the router SSHes out, e.g. to SCP servers): `ip ssh client algorithm ...`.

## Verify
```
show ip ssh
!  SSH Enabled - version 2.0
!  Encryption Algorithms: aes256-gcm,aes128-gcm,aes256-ctr,aes128-ctr
!  MAC Algorithms: hmac-sha2-512,hmac-sha2-256
!  KEX Algorithms: ...
```
From a workstation:
```
ssh -vv admin@10.0.0.1 2>&1 | grep -E 'kex: algorithm|server->client cipher|host key algorithm'
ssh-audit 10.0.0.1          # grades each algorithm, flags weak ones
nmap --script ssh2-enum-algos -p 22 10.0.0.1
```

## Compatibility traps
- Old management tools (legacy NMS, old Paramiko/Netmiko, SecureCRT versions, RANCID with old
  OpenSSH) may only know CBC or SHA-1. Test every automation client before rolling out estate-wide.
- Very old OpenSSH clients cannot use rsa-sha2-*; modern OpenSSH (8.8+) refuses ssh-rsa (SHA-1)
  signatures by default, so hardening actually fixes "no matching host key type" errors from new
  clients.
- Regenerating the RSA key changes the host key fingerprint: update known_hosts in automation.

## Verify
- [ ] ssh-audit shows no weak (red/yellow) algorithms, and all automation tools still connect.
