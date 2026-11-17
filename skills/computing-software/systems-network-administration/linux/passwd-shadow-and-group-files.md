---
id: computing-software.systems-network-administration.linux.passwd-shadow-and-group-files
name: passwd-shadow-and-group-files
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, users-groups, etc-passwd, etc-shadow, shadow-file, etc-group, gshadow, vipw, pwck, grpck, password-hashes, rhcsa, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Read and safely edit the account databases: /etc/passwd, /etc/shadow (hash formats, aging fields, lock markers), /etc/group and gshadow; vipw/vigr, pwck/grpck consistency checks."
sources:
  - https://github.com/shadow-maint/shadow/blob/master/man/shadow.5.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/passwd.5.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/vipw.8.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/pwck.8.xml
  - https://github.com/besser82/libxcrypt/blob/develop/doc/crypt.5
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# /etc/passwd, /etc/shadow, /etc/group

**Goal:** interpret every field, spot locked/expired/passwordless accounts, and edit the files
without corrupting them when the usual commands won't do.

## 1. /etc/passwd (world-readable, 644)
`name:x:UID:GID:GECOS:home:shell` — `x` = hash is in shadow. UID 0 = root privileges regardless
of name. The shell field selects the login program; a nologin-style shell is the usual way to block interactive login.

## 2. /etc/shadow (must not be readable by regular users)
`name:hash:lastchg:min:max:warn:inactive:expire:reserved`
- hash prefixes (crypt(5)): `$y$` yescrypt, `$6$` SHA-512, `$5$` SHA-256, `$1$` MD5 (weak — rehash), `$2b$` bcrypt.
  The default method differs per distribution; check the PAM configuration.
- a leading `!` = locked (`passwd -l`/`usermod -L`); `*` = no password login possible (system accounts);
  **empty = no password needed** (audit!).
- `lastchg`, `expire` are days since 1970-01-01; `lastchg` 0 = must change at next login; empty `lastchg` disables aging.
- the `min` field is deprecated and ignored; `warn` is days of warning before `max`; `inactive` is days after expiry during which login still works (password change required); `expire` 0 should not be used.
```bash
awk -F: '($2==""){print "EMPTY:",$1}' /etc/shadow
awk -F: '($3==0){print "UID0:",$1}' /etc/passwd
chage -l alice                                                                           # aging dates in readable form
```

## 3. /etc/group and /etc/gshadow
`group:x:GID:member1,member2` — lists **supplementary** members only; users whose primary GID
matches are members without being listed. gshadow holds group passwords (rare) and group
admins (`gpasswd -A`).

## 4. Editing safely
Prefer `useradd/usermod/chage/gpasswd`. When you must edit by hand:
```bash
vipw            # locks passwd and opens $VISUAL, $EDITOR or vi; vipw -s edits shadow
vigr; vigr -s   # group, gshadow
pwck -r; grpck -r   # read-only consistency checks (duplicate names, bad homes, missing shadow entries)
pwconv; grpconv     # create or sync shadow/gshadow from passwd/group
```
Never edit with a plain editor while useradd might run — vipw/vigr set the locks that prevent
concurrent damage. `/etc/shadow-` is the backup file written by the shadow tools.

## Gotchas
- Wrong permissions on shadow (world-readable) expose hashes to offline cracking.
- A malformed line (e.g. missing field) can break logins for everyone; test with `pwck` and keep a root shell open.
- `getent passwd` shows local + NSS sources (LDAP/sssd); the files show only local accounts.

## Verify
- [ ] `pwck -r` and `grpck -r` report no errors (a stock Debian 13 container exits 2 from `pwck -r` because system accounts have missing home directories, so read the output rather than relying on the exit code).
- [ ] `stat -c '%a %U:%G' /etc/shadow` shows no access for ordinary users; no empty hashes, only root has UID 0.

## Checked

2026-10-26. shadow-maint/shadow master (last commit 2026-10-20, release 4.20.3): shadow(5) nine fields, ! and * meaning, empty hash, last-change 0, deprecated minimum age, inactivity and expiry semantics; vipw/vigr -s and editor lookup; pwck -r. libxcrypt crypt(5) hash prefixes $y$, $6$, $5$, $1$, $2b$. Removed distribution-specific defaults, file modes, the !! RHEL meaning and the lock-file name, which no source confirmed.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container: field layout of passwd and shadow, $y$ hashes by default on Debian 13, ! prefix after passwd -l, empty hash after passwd -d found by the awk audit, usermod -U refusing to unlock a passwordless account, chage -d 0 giving last change 0, file modes (passwd 644, shadow 640 root:shadow), vipw/vigr/pwconv/grpconv present and vipw -s, pwck -r and grpck -r (including a malformed line), /etc/shadow- backup file, supplementary-only group lists. Not run: other hash prefixes, gshadow admin entries.
