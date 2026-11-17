---
id: computing-software.systems-network-administration.linux.ssh-known-hosts-and-host-key-verification
name: ssh-known-hosts-and-host-key-verification
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ssh, openssh, known-hosts, host-key-verification, ssh-keyscan, hashknownhosts, sshfp, host-certificates, remote-host-identification-changed, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Handle SSH host keys safely: verify fingerprints, fix 'REMOTE HOST IDENTIFICATION HAS CHANGED' properly, pre-seed known_hosts, and use host certificates or SSHFP."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/sshd.8
  - https://github.com/openssh/openssh-portable/blob/master/ssh_config.5
  - https://github.com/openssh/openssh-portable/blob/master/ssh-keygen.1
  - https://github.com/openssh/openssh-portable/blob/master/ssh-keyscan.1
  - https://datatracker.ietf.org/doc/html/rfc4255
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# known_hosts and host key verification

**Goal:** never blindly trust a new or changed host key, and avoid training people to type
"yes" by managing keys centrally.

## 1. First connection
On first contact ssh shows the server's host key fingerprint and asks for confirmation. Compare it with the
fingerprint obtained out-of-band:
```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub     # on the server console / provisioning output
```

## 2. Changed host key warning
The warning means the key differs from what you recorded: reinstall/rebuild, IP reused by another host,
load balancer with different backends — or a MITM. Verify the new fingerprint, then remove the
old entry precisely:
```bash
ssh-keygen -R web01; ssh-keygen -R 10.0.1.5        # removes all keys for the name (also from hashed files)
ssh-keygen -F web01                                # find entries
```
Don't delete the whole `known_hosts` or set `StrictHostKeyChecking no`.

## 3. Files and options
- `~/.ssh/known_hosts` (user), `/etc/ssh/ssh_known_hosts` (system-wide, managed by config mgmt).
- `HashKnownHosts yes` hashes host names and addresses added to `~/.ssh/known_hosts` (default `no`).
- `StrictHostKeyChecking accept-new`: add unknown keys automatically but still refuse changed ones — sane for automation; `yes` for high security.
- `UpdateHostKeys yes`: accept the server's additional host keys sent after authentication and add them to the user known_hosts.
- `VerifyHostKeyDNS yes` with DNSSEC-signed SSHFP records (`ssh-keygen -r web01.example.com` prints them).

## 4. Pre-seeding
```bash
ssh-keyscan -t ed25519 web01 web02 >> /etc/ssh/ssh_known_hosts    # only from a trusted network path!
```
ssh-keyscan itself does no verification — it's TOFU in bulk. Better: publish keys from the
provisioning system (it knows them) into the system known_hosts file.

## 5. Host certificates (at scale)
```bash
ssh-keygen -s host_ca -I web01 -h -n web01,web01.example.com,10.0.1.5 -V +52w /etc/ssh/ssh_host_ed25519_key.pub
# sshd_config: HostCertificate /etc/ssh/ssh_host_ed25519_key-cert.pub
# clients' known_hosts:
@cert-authority *.example.com ssh-ed25519 AAAA…host_ca_pub…
```
Rebuilt hosts get a new signed cert; clients never see a prompt or a changed-key warning.

## Gotchas
- Golden images with baked host keys: every clone has the same key — remove the host keys and regenerate them on first boot (`ssh-keygen -A` creates missing default-type host keys).
- Load balancers in front of SSH must present the same host key (or certs) on all backends.
- `-o UserKnownHostsFile=/dev/null` in scripts hides real MITM warnings.

## Verify
- [ ] `ssh-keygen -F <host>` returns exactly one entry with the verified key.
- [ ] Connecting to a rebuilt host either works silently (cert) or warns — never auto-accepts a changed key.

## Checked
Checked 2026-10-25 against OpenSSH portable master manual sources (ssh.1, ssh_config.5, sshd.8, sshd_config.5, ssh-keygen.1, ssh-add.1, scp.1, sftp.1) and ssh-keyscan.1.
Confirmed: known_hosts format including the `@cert-authority` and `@revoked` markers and hashed names, `ssh-keygen -R`, `-F`, `-H`, `-r`, `-A`, host certificate signing with `-s ... -h -n -V`, `StrictHostKeyChecking accept-new`, `HashKnownHosts` (default no), `UpdateHostKeys`, `VerifyHostKeyDNS` with SSHFP, `HostCertificate`, and ssh-keyscan `-t`.
Removed as unconfirmed: the Debian default for hashing, the AWS console-output command, and the exact first-connection prompt text.

Method: documentation only; no commands were run.
