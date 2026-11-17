---
id: computing-software.systems-network-administration.linux.trace-path-permissions-with-namei
name: trace-path-permissions-with-namei
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, namei, permissions, path-traversal, directory-execute, permission-denied, util-linux]
level: intro
status: verified
description: "Find which directory in a path blocks access with namei -l (owners and modes of every component), follow symlinks, and pair it with sudo -u tests and SELinux checks."
sources:
  - https://github.com/util-linux/util-linux/blob/master/misc-utils/namei.1.adoc
  - https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# namei: trace permissions along a path

**Problem:** "Permission denied" on `/srv/www/site/index.html` even though the file is world-readable — a parent directory
lacks `x` for that user.

```bash
namei -l /srv/www/site/index.html
# f: /srv/www/site/index.html
# dr-xr-xr-x root  root  /
# drwxr-xr-x root  root  srv
# drwxr-x--- deploy deploy www        <- 'other' has no x: nginx can't traverse
# drwxr-xr-x deploy deploy site
# -rw-r--r-- deploy deploy index.html
namei -om /etc/ssl/private/key.pem    # -o owners, -m modes (-l is -m -o -v)
namei -x /var/lib/app/data            # mount point directories shown as D
namei -Z /srv/www/site/index.html     # security context, if namei was built with support
```
Symlinks are followed and shown (`l` lines), each target traced — great for chains like `/etc/alternatives`; `-n` stops following them.

## Then test as the real user
```bash
sudo -u nginx test -r /srv/www/site/index.html && echo readable
sudo -u nginx stat /srv/www/site/index.html
```
If modes look right but access still fails: ACLs on each directory, SELinux or AppArmor denials, mount options,
or systemd sandboxing (`ProtectHome=`, `ReadOnlyPaths=`) on the service.

## Fix minimally
Grant traverse only (execute on the directory) instead of opening reads: `chmod o+x /srv/www`, or an ACL entry for the service user.

## Verify
- [ ] `sudo -u <service-user> cat <file>` works and `namei -l` shows `x` for that user on every directory.

## Checked

2026-10-26. util-linux master (last commit 2026-10-26): namei options -l, -m, -o, -v, -x, -n, -Z, symlink following and the type characters. systemd.exec lists ProtectHome= and ReadOnlyPaths=. Removed the getfacl, setfacl, ls -Z and ausearch command details, which were not checked.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container: namei -l, -om, -x (D marks a mount point), -n (stops following symlinks), -Z (prints ? without a security context), symlink chains, and sudo -u test -r before and after chmod o+x on the blocking directory. Not run: SELinux/AppArmor and systemd sandboxing remarks (documentation only).
