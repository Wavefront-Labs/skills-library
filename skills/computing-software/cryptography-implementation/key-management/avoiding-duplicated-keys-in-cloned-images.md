---
id: computing-software.cryptography-implementation.key-management.avoiding-duplicated-keys-in-cloned-images
name: avoiding-duplicated-keys-in-cloned-images
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, cloned-image-keys, golden-image, ssh-host-keys, machine-id, cloud-init, sysprep, containers, key-generation, duplicate-keys]
level: practitioner
status: draft
description: "Prevent identical SSH host keys, TLS keys, machine IDs and RNG seeds across VM images and containers: image preparation, first-boot generation and detection."
sources: ["https://cloudinit.readthedocs.io/en/latest/reference/modules.html#ssh", "https://www.freedesktop.org/software/systemd/man/latest/machine-id.html", "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/sysprep--generalize--a-windows-installation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Avoiding duplicated keys in cloned images

Every VM or container built from an image that already contains private keys shares those keys. One compromise
exposes all instances, and SSH host-key pinning stops meaning anything.

## Image preparation (Linux)
```
rm -f /etc/ssh/ssh_host_*                     # host keys
truncate -s 0 /etc/machine-id; rm -f /var/lib/dbus/machine-id
rm -f /var/lib/systemd/random-seed            # RNG seed must be unique
rm -rf /etc/pki/tls/private/* /root/.ssh/id_*  # any service keys baked in by provisioning
cloud-init clean --logs --seed
```
Then let first boot regenerate: cloud-init `ssh_deletekeys: true` and `ssh_genkeytypes: [ed25519, ecdsa, rsa]`, or
`sshd-keygen` units on RHEL/Fedora, `ssh-keygen -A` in a first-boot script.

Windows: `sysprep /generalize` resets the machine SID and certificate-related state; avoid baking machine
certificates into images; enrol via auto-enrolment after join.

## Containers
- Never `COPY` private keys into images or build layers; even deleted in a later layer, they remain in history.
- Inject keys at runtime (mounted secrets, workload identity, cert-manager/SPIFFE).
- Scan images: `trivy image --scanners secret myimage:tag`, `docker history --no-trunc`.

## Detection across a fleet
- Collect host key fingerprints (`ssh-keyscan` across the inventory, or from config management facts) and look for
  duplicates.
- For TLS, compare SPKI hashes from scans; any duplicate across distinct hosts is a finding.
- For RSA, run a batch-GCD to catch shared primes from low entropy at first boot.

## Verify
- [ ] Two instances launched from the same image show different host key fingerprints.
- [ ] Image secret scan is clean in CI.
- [ ] Fleet duplicate-fingerprint report is empty.
