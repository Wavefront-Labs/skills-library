---
id: computing-software.systems-network-administration.linux.posix-acl-mask-and-backup
name: posix-acl-mask-and-backup
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, acls, posix-acl, acl-mask, effective-rights, acl-backup, getfacl-r, setfacl-restore, default-acl, rhcsa, lpic-2, sysadmin]
level: practitioner
status: verified
description: "Understand the ACL mask and #effective rights, keep chmod from silently cutting ACL grants, and back up/restore tree ACLs with getfacl -R and setfacl --restore."
sources:
  - https://man7.org/linux/man-pages/man5/acl.5.html
  - https://man7.org/linux/man-pages/man1/setfacl.1.html
  - https://man7.org/linux/man-pages/man1/getfacl.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ACL mask, effective rights, and ACL backup

**Goal:** ACL grants that actually work, and ACLs that survive copies, migrations and restores.

## 1. The mask
Once a file has named user/group entries, the **mask** caps the rights of every named user,
named group and the owning group. The owner and "other" are not masked.
```bash
setfacl -m u:alice:rwx report.xlsx   # mask is recalculated to rwx
chmod 640 report.xlsx                # group bits are the mask: it becomes r--
getfacl report.xlsx
# user::rw-
# user:alice:rwx        #effective:r--     ← mask limits alice to r--
# group::r--
# mask::r--
# other::---
```
- `ls -l` shows a `+`, and the **group** permission bits displayed correspond to the **mask**, not the owning group.
- `chmod g-w file` on an ACL file changes the mask (group bits map to the mask) → removes write from every named entry's effective rights.
- `setfacl -m` recalculates the mask to the union of entries unless you pass `-n` (no mask recalc).
- Set it deliberately: `setfacl -m m::rwx file`.

## 2. Default ACLs (inheritance) and the mask
```bash
setfacl -m d:g:projects:rwX /srv/proj        # new files/dirs inherit
setfacl -R -m g:projects:rwX /srv/proj       # existing content
```
New files inherit the default ACL as their access ACL, but the mode passed by the creating process (e.g. `open()` with 0644)
removes permissions not in that mode — so a file created 0644 ends up with `mask::r--` and the named group can't write.
Apps that create files with 0600 defeat inheritance in the same way. Check with `getfacl` on a newly
created file, not just the directory.

## 3. Backup and restore
```bash
getfacl -R -p /srv/proj > $HOME/proj.acl             # -p/--absolute-names keeps leading slashes; by default they are stripped
setfacl --restore=$HOME/proj.acl                     # restore a backup made by getfacl -R
getfacl -R --skip-base proj > proj-only-acls.acl     # just files that actually have ACLs
```
Tools and ACLs:
- `cp -a`, `rsync -A` (and `-X` for xattrs) and `tar --acls --xattrs` (on create and extract) are the documented ways to carry them; archives and copies made without these options may drop them.

## Gotchas
- Restoring onto a system where users/groups have different UIDs/GIDs → wrong principals (getfacl stores names by default; `-n` stores numbers).
- Copying files to a filesystem without ACL support can lose them; check the target.
- Too many ACLs make permissions hard to audit; prefer groups + setgid directories where possible.

## Verify
- [ ] `getfacl` shows no `#effective` lower than intended for named entries.
- [ ] A file created by the real application (not `touch`) inherits the expected ACL and mask.
- [ ] Restore of the ACL dump onto a test copy produces identical `getfacl -R` output (`diff`).

## Checked
2026-10-27. Checked against the man7.org acl(5) (page dated 2026-06-05), setfacl(1) and getfacl(1) pages (upstream commit dated 2026-06-29), GNU coreutils and rsync(1) manual sources and Debian tar(1) 1.35. Confirmed: the mask limits named users, named groups and the owning group but not the owner or other; group permission bits correspond to the mask and chmod changes ACL entries; default ACL inheritance with the creation mode limiting inherited permissions; setfacl -m, -n, -R, --restore, d: prefix, X, m:: syntax; getfacl -R, -p, -n, --skip-base and the effective-rights comment; the copy and archive options. Removed: the claims about default filesystem ACL support, NFSv4 tooling, star and bsdtar, and the restore working-directory remark.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (acl 2.3.2, overlay filesystem): setfacl -m/-n/-R/--restore, getfacl -R/-p/-n/--skip-base, mask recalculation, chmod changing the mask, ls -l group bits showing the mask, default ACL inheritance (file created with mode 0644 got mask::r--, 0600 got mask::---, 0664 got mask::rw-), restore round trip identical, cp -a and rsync -aA and tar --acls keeping ACLs while plain cp, rsync -a and tar dropped them. Corrected the first example: right after setfacl -m the mask is rwx; the effective r-- appears after chmod 640. Not run: NFSv4 ACL tooling.
