---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.ssh-authorized-keys-and-ssh-artefacts
name: ssh-authorized-keys-and-ssh-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [authorized-keys, linux-forensics, linux-persistence, ssh-forensics, dfir]
level: practitioner
status: docs-checked
description: "Investigate SSH persistence and lateral movement on Linux: authorized_keys entries and options, known_hosts, sshd_config key sources, certificate CAs and key timelines."
sources: ["https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT", "https://man.openbsd.org/sshd_config", "https://attack.mitre.org/techniques/T1098/004/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH authorized_keys and SSH artefacts

**Goal:** adding a public key to `authorized_keys` (ATT&CK T1098.004, persistence and privilege escalation) is a common Linux
persistence technique (the page lists Skidmap, TeamTNT and others). SSH artefacts also map lateral movement between servers.

## Where keys can come from (sshd_config)
- `AuthorizedKeysFile`: default `.ssh/authorized_keys .ssh/authorized_keys2`, relative to the user's home unless absolute; several
  files may be listed, tokens `%h`, `%U`, `%u` are accepted, and `none` skips file keys. Changed values are a finding.
- `AuthorizedKeysCommand` (default none): runs after the files, only if no match was found there, and its output is in
  authorized_keys format; `AuthorizedKeysCommandUser` must be set or sshd refuses to start.
- `TrustedUserCAKeys`: a file of CA public keys; a certificate signed by a listed CA is accepted for any user in the certificate's
  principals list. Check for rogue CAs. `AuthorizedPrincipalsFile` / `AuthorizedPrincipalsCommand` restrict accepted principals.
- `Include` pulls in further configuration files, expanded in lexical order, so inspect included files too.
- Check every account's files, including root and service accounts. sshd ignores an authorized_keys file whose file, `.ssh`
  directory or home directory is writable by others unless `StrictModes` is `no`.

## authorized_keys line format
Fields: options (optional), key type, base64 key, comment. Option examples shown in sshd(8): `restrict`, `command="..."` (forced
command: it can hide a backdoor), `permitopen`, `permitlisten`, `tunnel`, `no-touch-required`, `verify-required`,
`cert-authority` with `principals=`. Review each key's options and comment, and compare the key against the organisation's
key inventory.

## Other SSH artefacts
| Artefact | Use |
|---|---|
| `~/.ssh/known_hosts`, `/etc/ssh/ssh_known_hosts` | Hosts the account has connected to. Fields: optional marker, hostnames, key type, key, comment. Hostnames starting with `|` are hashed; hashed entries cannot be read back, only tested against a candidate name with ssh-keygen |
| `~/.ssh/environment`, `~/.ssh/rc` | Per-user login-time code or environment; the environment file is processed only when `PermitUserEnvironment` is enabled |
| `/etc/ssh/sshrc`, `~/.hushlogin`, `/etc/nologin` | Other sshd login-time files described in the FILES section |
| `sshd_config` changes | Review `PermitRootLogin`, `PasswordAuthentication`, `Port` and the key-source options above |
| Authentication logs | Tie logins to a key; log locations vary by distribution and are outside the cited pages |

## Gotchas
- Attackers may append to an existing line or insert keys in the middle of long files: compare full content against a baseline.
- File times of `authorized_keys` and `.ssh/` help date the change; key comments often name the creating host but can be forged.

## Verify
Every key and every trusted CA is attributed to a known owner, and every key-based login maps to an attributed key.

## Checked
Date: 2026-11-08.
Confirmed in sshd(8): authorized_keys option examples, known_hosts field layout, hashed host names starting with `|`, FILES section
entries, StrictModes behaviour. Confirmed in sshd_config(5): AuthorizedKeysFile default and tokens, AuthorizedKeysCommand and
its User option, TrustedUserCAKeys, AuthorizedPrincipalsFile, Include. Confirmed in T1098.004: persistence and privilege
escalation tactics and the example groups.
Removed (not in the cited pages): ssh-keygen invocations, debugfs/stat crtime advice, sample auth.log text, agent-socket path,
bash_history, osquery and Velociraptor artefact names, `sshd_config.d`, and the claim that this is "the most common" Linux
persistence.
Method: docs-only read of cited pages, 2026-11-08
