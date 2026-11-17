---
id: computing-software.systems-network-administration.linux.userdel-and-account-offboarding
name: userdel-and-account-offboarding
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, users-groups, userdel, user-removal, account-lock, offboarding, orphaned-files, usermod-lock, crontab-removal, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Remove or disable a departing user properly: lock first, kill sessions, archive and delete home, find orphaned files, remove cron/at jobs, keys and sudo rules, then userdel."
sources:
  - https://github.com/shadow-maint/shadow/blob/master/man/userdel.8.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/usermod.8.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/shadow.5.xml
  - https://github.com/systemd/systemd/blob/main/man/loginctl.xml
  - https://github.com/SSSD/sssd/blob/master/src/man/sss_cache.8.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# userdel and account offboarding

**Goal:** a leaver loses access immediately, their data is kept as policy requires, and no
orphaned files, jobs or keys remain to be re-used by a future account with the same UID.

## 1. Disable now (reversible)
```bash
usermod -L -e 1 alice              # lock the password AND set account expiry to 1 (usermod(8) advice for locking the account)
chage -E 1 alice                   # expiry only (shadow(5): do not use 0 as the expiry date)
usermod -s /sbin/nologin alice
loginctl terminate-user alice      # end sessions;   or: pkill -KILL -u alice
```
`usermod -L` locks only the password; to lock the account itself also set the expiry date to 1 (usermod(8)). Whether key-based SSH logins are then refused depends on the PAM account stack, so test it.
Also remove keys: `mv ~alice/.ssh/authorized_keys{,.disabled}`; check `AuthorizedKeysFile`
locations outside home and central key systems (LDAP/IPA, SSH CA certs — revoke/KRL).

## 2. Inventory what they own
```bash
crontab -l -u alice; atq
grep -r alice /etc/sudoers /etc/sudoers.d/
find / -xdev \( -user alice -o -group alice \) -not -path "$(getent passwd alice | cut -d: -f6)/*" -ls 2>/dev/null   # files outside home
loginctl disable-linger alice      # lingering keeps a user manager running after logout
ps -u alice
```

## 3. Archive and remove
```bash
tar -czf /archive/alice-$(date +%F).tgz -C /home alice
crontab -r -u alice
userdel -r alice                   # remove account, home and mail spool (files on other file systems stay)
userdel -r -f alice                # force: skips safety checks, may leave the system inconsistent (careful)
```
Then reassign leftover files found in step 2: `find / -xdev -nouser -exec chown newowner {} +`.

## 4. Why orphans matter
UIDs get reused: a new user created with the old UID instantly owns every orphaned file.
Either reassign/delete orphans, or never reuse UIDs (track in central identity). Find all orphans periodically: `find / -xdev \( -nouser -o -nogroup \) -ls`.

## Gotchas
- `userdel` refuses if processes run as the user (exit 8) — kill sessions first, or use `-f`.
- With `USERGROUPS_ENAB yes` userdel also removes the same-named group, unless it is another user's primary group (then it only warns).
- `USERDEL_CMD` in login.defs names a script run on removal that should clear cron, at and print jobs; its exit status is ignored.
- Central accounts (sssd/LDAP): disable in the directory; local `userdel` doesn't apply, and cached credentials may allow offline login until cache expires (`sss_cache -u alice`).
- Shared service passwords the user knew must be rotated separately.

## Verify
- [ ] `ssh alice@host` fails (password and key); `chage -l alice` shows account expired.
- [ ] `getent passwd alice` empty after userdel; `find / -xdev -nouser` has nothing from the old UID.
- [ ] No cron/at jobs or sudo rules remain and lingering is disabled.

## Checked

2026-10-26. shadow-maint/shadow master (last commit 2026-10-20, release 4.20.3): userdel -r and -f, exit status 8 when the user has processes, USERGROUPS_ENAB group removal, USERDEL_CMD, usermod -L note about expiry date 1, shadow(5) warning against expiry 0 (the earlier chage -E 0 example was replaced). systemd loginctl man page: terminate-user and enable/disable-linger. sss_cache man page: -u invalidates one user. Removed the unconfirmed PAM-phase explanation and the linger directory path.

Method: documentation only; no commands were run.
