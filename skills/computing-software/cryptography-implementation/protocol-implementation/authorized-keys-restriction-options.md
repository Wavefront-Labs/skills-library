---
id: computing-software.cryptography-implementation.protocol-implementation.authorized-keys-restriction-options
name: authorized-keys-restriction-options
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, authorized-keys-options, ssh, openssh, forced-command, restrict, deploy-keys]
level: practitioner
status: docs-checked
description: "Restrict SSH keys in authorized_keys: command=, from=, restrict, permitopen, no-pty and expiry-time options, plus forced commands for backup and deploy keys."
sources: ["https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT", "https://man.openbsd.org/sshd_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authorized_keys restriction options

## Syntax
Options go before the key type, comma-separated, no spaces outside quotes:
```
restrict,command="/usr/local/bin/backup-receive",from="10.0.5.0/24" ssh-ed25519 AAAA... backup@host
restrict,port-forwarding,permitopen="db.internal:5432" ssh-ed25519 AAAA... tunnel@ci
expiry-time="20261231",restrict,pty ssh-ed25519 AAAA... contractor
```

## Key options
- `restrict`: disables port, agent and X11 forwarding, PTY allocation and `~/.ssh/rc`, and any restrictions added in future. Re-enable selectively (`pty`,
  `port-forwarding`, `agent-forwarding`). Use it as the default for every non-interactive key.
- `command="..."`: forced command; the client's requested command is in `$SSH_ORIGINAL_COMMAND` for wrapper
  scripts to validate (e.g. allow only `rsync --server ...`).
- `from="pattern-list"`: the remote canonical host name or IP must match the list; CIDR notation is supported. It adds to key authentication, so a stolen key is harder to use from elsewhere; name-based patterns depend on name servers, so prefer IPs.
- `permitopen="host:port"` limits `-L` forwards (literal hosts, no pattern matching); `permitlisten="[host:]port"` limits `-R` listens.
- `expiry-time="timespec"`: `YYYYMMDD[Z]` or `YYYYMMDDHHMM[SS][Z]`; system time zone unless suffixed with Z (UTC).
- `principals="..."` on `cert-authority` lines restricts accepted certificate principals.
- `no-touch-required`/`verify-required` apply to FIDO (`ecdsa-sk`, `ed25519-sk`) keys.
- A `ForceCommand` in sshd_config can supersede `command=`; the option applies to shell, command and subsystem execution.

## Practices
- Validate `$SSH_ORIGINAL_COMMAND` in forced-command wrappers with an allow list; never `eval` it.
- Manage via `AuthorizedKeysCommand` or SSH certificates at scale instead of hand-edited files.

## Verify
- [ ] `ssh -i key host` gets the forced command only; `ssh -L` beyond permitopen fails.

## Checked
2026-11-01. Confirmed against the sshd(8) AUTHORIZED_KEYS FILE FORMAT section: restrict contents, command and SSH_ORIGINAL_COMMAND, from, permitopen, permitlisten, expiry-time format, principals, FIDO options. Removed: OpenSSH 7.7 version claim and rrsync advice.
Method: documentation only; no commands were run.
