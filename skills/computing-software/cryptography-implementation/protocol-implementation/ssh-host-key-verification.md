---
id: computing-software.cryptography-implementation.protocol-implementation.ssh-host-key-verification
name: ssh-host-key-verification
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, ssh, openssh, known-hosts, host-key-verification, stricthostkeychecking, sshfp, updatehostkeys, tofu, ci-ssh]
level: practitioner
status: docs-checked
description: "Verify SSH host keys instead of TOFU: pre-seeded known_hosts, SSHFP with DNSSEC, StrictHostKeyChecking in CI, UpdateHostKeys, changed-key warnings."
sources: ["https://man.openbsd.org/ssh_config", "https://datatracker.ietf.org/doc/html/rfc4255", "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH host key verification

SSH authenticates the server by its host key. The default trust model is TOFU
(trust on first use): the first connection asks for confirmation and stores the
key in `known_hosts`. In automation that prompt is usually "fixed" with
`StrictHostKeyChecking=no`, which makes ssh add new host keys automatically and
(per `ssh_config(5)`) allow connections to hosts whose key has changed, so
server authentication is effectively gone.

## Get the real key out of band

```bash
ssh-keyscan -t ed25519 git.example.com > keys.txt   # fetches over the network: NOT verification by itself
ssh-keygen -l -f keys.txt                           # compare fingerprint with a trusted source
```

Trusted sources: the provider's published fingerprints (GitHub publishes
its), your provisioning system, an SSH host CA, or SSHFP records under DNSSEC.

## CI and automation

```bash
# commit the known_hosts entries (or inject from a secret/config)
echo "github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl" >> ~/.ssh/known_hosts
ssh -o StrictHostKeyChecking=yes git@github.com
```

(That Ed25519 entry matches GitHub's published list; recheck it on GitHub's
SSH key fingerprints page before use, as keys can change.)

- `StrictHostKeyChecking=yes`: unknown or changed keys fail.
- `accept-new`: adds new host keys to `known_hosts` automatically but refuses
  hosts whose key has changed. Use it for ephemeral fleets only with another
  trust anchor.
- Never `no` outside throwaway labs.

## SSHFP

Publish host key fingerprints in DNS (`ssh-keygen -r hostname` prints
records), sign the zone with DNSSEC, and set `VerifyHostKeyDNS yes` (default
`no`; with `yes` the client implicitly trusts keys matching a secure
fingerprint, and insecure fingerprints are handled as `ask`). RFC 4255 says
clients that validate DNSSEC signatures themselves SHOULD use standard
procedures; without DNSSEC validation the records are just more
unauthenticated network data.

## Rotation and changed keys

- `UpdateHostKeys` lets servers announce additional host keys so clients learn
  new ones before the old is retired. It is on by default if you have not
  overridden `UserKnownHostsFile` and have not enabled `VerifyHostKeyDNS`;
  otherwise it is off.
- A changed-host-key warning means stop and confirm through another channel
  (rebuild? key rotation?). Then remove the old entry with `ssh-keygen -R hostname`.
- At scale, host CA keys in `known_hosts` with the `@cert-authority` marker
  remove the per-host problem.

## Verify

- [ ] No `StrictHostKeyChecking no` in scripts or CI configs.
- [ ] Pinned known_hosts entries match fingerprints from a trusted source.
- [ ] Host key rotation procedure documented (UpdateHostKeys or host CA).

## Checked

2026-11-01. Confirmed against ssh_config(5) (StrictHostKeyChecking
`accept-new` and `no` behaviour, VerifyHostKeyDNS default and meaning,
UpdateHostKeys default conditions), ssh-keygen(1) (`-l`, `-r hostname`,
`-R hostname`), ssh-keyscan(1) (`-t`), sshd(8) (`@cert-authority` marker in
known_hosts), RFC 4255 (SSHFP, DNSSEC) and GitHub's fingerprints page (the
Ed25519 known_hosts line). Removed: OpenSSH version numbers for
`accept-new` and `UpdateHostKeys`, the GitHub 2023 RSA rotation remark, and
the `UserKnownHostsFile=/dev/null` example (not in the sources).
Method: documentation only; no commands were run.
