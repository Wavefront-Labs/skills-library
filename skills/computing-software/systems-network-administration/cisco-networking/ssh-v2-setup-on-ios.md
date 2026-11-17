---
id: computing-software.systems-network-administration.cisco-networking.ssh-v2-setup-on-ios
name: ssh-v2-setup-on-ios
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ssh, ssh-setup, crypto-key-generate, ssh-version-2, vty, local-user, rsa-keys]
level: practitioner
status: draft
description: "Enable SSH v2 on IOS/IOS-XE: hostname and domain, RSA key generation, local users with scrypt secrets, vty transport input ssh, and verifying the session."
sources:
  - https://www.cisco.com/c/en/us/support/docs/security-vpn/secure-shell-ssh/4145-ssh.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_ssh/configuration/xe-16/sec-usr-ssh-xe-16-book/sec-usr-ssh-sec-shell.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SSH v2 setup on IOS

```
hostname SW-CORE-1
ip domain name corp.example.com            ! key label needs hostname + domain
crypto key generate rsa modulus 3072 label SSH-KEY
ip ssh rsa keypair-name SSH-KEY
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3
username netadmin privilege 15 algorithm-type scrypt secret <PASSWORD>
!
ip access-list standard MGMT-HOSTS
 permit 10.99.0.0 0.0.0.255
line vty 0 15
 access-class MGMT-HOSTS in
 login local
 transport input ssh
 exec-timeout 10 0
```
- Generate keys of at least 2048 bits; v2 requires >= 768, modern clients reject < 2048.
- `transport input ssh` disables telnet on those lines; do this only after testing SSH in a
  second session.
- `algorithm-type scrypt` (type 9) secrets; never `password` (type 7 is reversible).
- On IOS-XE 17.x, consider `ip ssh server algorithm` lists to remove weak ciphers/MACs
  (e.g. drop CBC and hmac-sha1) once all clients support modern ones.

## Old clients
Modern OpenSSH may refuse old IOS kex/hostkey algorithms. Client-side workaround:
`ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 -oHostKeyAlgorithms=+ssh-rsa netadmin@sw`.
Better fix: upgrade IOS or enable newer algorithms on the device.

## Verify
```
show ip ssh                  ! "SSH Enabled - version 2.0", modulus
show ssh                     ! active sessions, cipher, user
show crypto key mypubkey rsa
```
- [ ] SSH works from a management host; telnet refused; access-class blocks others.
