---
id: computing-software.systems-network-administration.linux.preserve-acls-and-xattrs-in-copies
name: preserve-acls-and-xattrs-in-copies
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tar-acls, rsync-acls, acls, xattrs, selinux-context, backup, cp-preserve]
level: practitioner
status: docs-checked
description: "Keep POSIX ACLs, extended attributes and SELinux labels when copying or backing up: cp -a, rsync -aAX, tar --acls --xattrs --selinux, and verifying with getfacl/getfattr diffs."
sources:
  - https://manpages.debian.org/trixie/tar/tar.1.en.html
  - https://man7.org/linux/man-pages/man1/getfacl.1.html
  - https://man7.org/linux/man-pages/man1/setfacl.1.html
  - https://man7.org/linux/man-pages/man7/xattr.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preserving ACLs and xattrs

Most copy/archive tools drop ACLs and xattrs unless told otherwise — restores then "work" but permissions are wrong.

## Tools
```bash
cp -a src/ dst/                                   # -a tries to preserve SELinux context and xattrs (ACLs are stored as xattrs)
rsync -aHAX --numeric-ids src/ host:/dst/         # -A ACLs, -X xattrs, -H hardlinks; both ends need support
tar --acls --xattrs --xattrs-include='*' --selinux -cpf etc.tar /etc
tar --acls --xattrs --xattrs-include='*' --selinux -xpf etc.tar -C /restore    # same flags on extract
```
`--xattrs-include=PATTERN` selects which xattr keys tar handles (a globbing pattern); `--selinux` enables SELinux context support. Check the manual of your tar version for the default when `--xattrs` is omitted.

## Filesystem support
The target filesystem must support them; support and limits vary by filesystem (see xattr(7) and the filesystem's documentation). Check before relying on a copy.

## Verify by diff
```bash
(cd src && getfacl -R . ) > a.txt ; (cd dst && getfacl -R .) > b.txt ; diff a.txt b.txt
(cd src && getfattr -R -d -m - . ) > x1.txt ; (cd dst && getfattr -R -d -m - .) > x2.txt ; diff x1.txt x2.txt
```
Or save ACLs alongside data: `getfacl -R -p /srv/share > share.acl` and restore with `setfacl --restore=share.acl` (setfacl(1): restores a backup made by `getfacl -R`).

## Gotchas
- `--numeric-ids` makes rsync not map uid/gid values by user/group name; without it ownership is mapped by name, which can differ on hosts with different users.
- SELinux labels restored from another policy version may be wrong — `restorecon -R` after restoring system paths.

## Verify
- [ ] getfacl/getfattr diffs are empty after a test restore.

## Checked
2026-10-27. Checked against GNU coreutils manual source (cp -a and --preserve=xattr), rsync(1) manual source (-a excludes -A, -X and -H; --acls, --xattrs, --hard-links, --numeric-ids), Debian tar(1) 1.35 (trixie), man7.org getfacl(1) and setfacl(1) (upstream commit 2026-06-29). Confirmed: rsync -aHAX and its meanings, tar --acls --xattrs --selinux --xattrs-include=PATTERN, getfacl -R and -p, setfacl --restore, rsync --numeric-ids. Removed: the star command, the borg and restic default and flag claims, tar's default xattr behaviour claim, the per-filesystem support list and the --noacls claims, none of which the documents confirm. The GNU tar manual link in sources is not readable from this environment and was replaced by the Debian tar(1) page.

Method: documentation only; no commands were run.
