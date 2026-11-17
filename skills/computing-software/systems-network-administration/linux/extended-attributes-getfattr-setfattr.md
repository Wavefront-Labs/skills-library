---
id: computing-software.systems-network-administration.linux.extended-attributes-getfattr-setfattr
name: extended-attributes-getfattr-setfattr
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, file-attributes, xattr, getfattr, setfattr, security-selinux, user-xattr, trusted-xattr, file-capabilities, rsync-x, lpic-2, sysadmin]
level: practitioner
status: verified
description: "Manage extended attributes: user, trusted, security and system namespaces, getfattr/setfattr, SELinux labels and capabilities, and preserving xattrs in copies."
sources:
  - https://man7.org/linux/man-pages/man7/xattr.7.html
  - https://man7.org/linux/man-pages/man1/getfattr.1.html
  - https://man7.org/linux/man-pages/man1/setfattr.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Extended attributes (xattrs)

**Goal:** know what metadata hides in xattrs (security labels, capabilities, ACLs, app data),
read/write them, and stop copies and backups from silently dropping them.

## 1. Namespaces
| Namespace | Who | Holds |
|---|---|---|
| `user.*` | access follows the file permission bits; regular files and directories only | arbitrary additional information such as MIME type or encoding |
| `trusted.*` | CAP_SYS_ADMIN only | user-space mechanisms, e.g. overlayfs (`trusted.overlay.*`) |
| `security.*` | policy of the security module; without one, root-only writes | `security.selinux` labels, `security.capability` (file caps), `security.ima`/`security.evm` |
| `system.*` | kernel, per-attribute policy | `system.posix_acl_access` / `system.posix_acl_default` (POSIX ACLs) |

## 2. Read and write
```bash
getfattr -d file                         # user.* only by default (-m default is "^user\.")
getfattr -d -m - file                    # -m - matches all attributes you may read
getfattr -n security.selinux file        # one attribute
getfattr -d -m - -e hex <file>            # hex: see raw bytes, e.g. security.capability
setfattr -n user.checksum -v "sha256:ab12…" file
setfattr -x user.checksum file           # remove
getfattr -R -d -m - /srv/data > xattrs.dump       # dump all readable attributes recursively
```
Higher-level tools are usually better for specific namespaces: `ls -Z`/`chcon`/`restorecon`
(SELinux), `getcap`/`setcap` (capabilities), `getfacl`/`setfacl` (ACLs).

## 3. Preserving them
- `cp --preserve=xattr` (or `-a`, which tries to preserve SELinux context and xattrs).
- `rsync -aX` (xattrs) `-A` (ACLs): by default `-X` copies only the `user.*` namespace for non-root users; see the `--xattrs` entry in rsync(1) for the root and filter behaviour.
- `tar --xattrs --acls --selinux` when creating and extracting; `--xattrs-include=PATTERN` selects which keys.
- `mv` always tries to copy xattrs when it has to copy (across filesystems).
Lost file capabilities after a copy can make a binary suddenly need root.

## 4. Support
Support and limits depend on the filesystem (xattr(7)); some filesystems such as ext2 and ext3 need the `user_xattr` mount option for `user.*`.

## Gotchas
- `user.*` isn't allowed on symlinks or device files.
- Limits: names up to 255 bytes and values up to 64 kB (VFS); on ext2/3/4 all of a file's xattrs must fit in one filesystem block; on Btrfs name, value and overhead are limited to the node size (16 kB by default); XFS has no practical count limit.
- Files restored without `security.selinux` get default labels → relabel with `restorecon -R`.

## Verify
- [ ] `getfattr -d -m - <file>` shows expected attributes on source and copy (diff the dumps).
- [ ] `getcap` on binaries that need capabilities still shows them after deployment.

## Checked
2026-10-27. Checked against man-pages xattr(7) (mirror, 2021 revision), the man7.org getfattr(1) and setfacl/getfacl pages (upstream commit dated 2026-06-29), the GNU coreutils manual source (cp -a, --preserve=xattr, mv), the rsync(1) manual source, Debian tar(1) 1.35 (trixie) and the Linux kernel overlayfs and EVM ABI documents. Confirmed: the four namespaces and their access rules; user.* only on regular files and directories; getfattr -d defaults to the user namespace with -m default ^user\. and -m - for all, -e hex, -R, -n; tar --xattrs, --acls, --selinux, --xattrs-include; rsync -X user namespace behaviour; xattr size limits. Removed: the setfattr --restore round-trip (not documented in getfattr(1)), tmpfs, NFSv4.2 and FAT support claims, the ea_inode and user_xattr-default-on-ext4 claims, GlusterFS and Samba attribute examples, and the exact cp version gate.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (attr 2.5.2, overlay filesystem): getfattr -d default (user.* only), -m -, -e hex, -n, -R; setfattr -n/-v/-x; system.posix_acl_access shown after setfacl; user.* refused on a symlink and on /dev/null; cp without options dropped the attribute while cp --preserve=xattr and cp -a kept it; rsync -a dropped it and rsync -aX kept it; tar --xattrs round trip; --xattrs-include and --selinux accepted; a 60000-byte value failed with ENOSPC (single-block limit), a 257-byte name failed with ERANGE. Not run: trusted.* and security.* writes (need capabilities the rootless container lacks), SELinux labels, Btrfs and XFS limits, mount option user_xattr.
