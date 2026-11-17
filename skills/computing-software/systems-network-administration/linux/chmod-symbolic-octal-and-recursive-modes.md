---
id: computing-software.systems-network-administration.linux.chmod-symbolic-octal-and-recursive-modes
name: chmod-symbolic-octal-and-recursive-modes
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, permissions, chmod, symbolic-mode, octal-mode, chmod-recursive, capital-x, umask, directory-execute, executable-bit, rhcsa, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Set permissions precisely: octal vs symbolic chmod, the capital X trick for recursive changes, what r/w/x mean on directories vs files, and fixing trees with find."
sources:
  - https://man7.org/linux/man-pages/man1/chmod.1.html
  - https://man7.org/linux/man-pages/man7/path_resolution.7.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# chmod: symbolic, octal, recursive; directory bits

**Goal:** apply exactly the permissions you mean, recursively without making every file
executable, and understand why "permission denied" happens on a directory.

## 1. Octal vs symbolic
Octal: each digit = r(4)+w(2)+x(1) for user, group, other; optional leading digit for
setuid(4)/setgid(2)/sticky(1). `chmod 640 f`, `chmod 2775 dir`.
Symbolic: `[ugoa][+-=][rwxXst]` — changes only what you name:
```bash
chmod u+x script.sh            # add execute for owner only
chmod go-w file                # remove write from group and others
chmod g=rX,o= dir              # set group exactly to r + X, others nothing
chmod a+r,u+w file
chmod --reference=good.conf bad.conf
```
Prefer symbolic when you want to change one bit without knowing the rest; octal when you want
an exact final state.

## 2. Directory permissions mean something different
| Bit | On a file | On a directory |
|---|---|---|
| r | read contents | list names (`ls`) |
| w | modify | create, delete, rename entries (**regardless of the files' own permissions**) |
| x | execute | **traverse**: access entries by name, `cd` into it |
- `r` without `x`: `ls` shows names but `ls -l`/open fail ("Permission denied").
- `x` without `r`: you can open `dir/known-name` but can't list — a "drop box" pattern.
- Every parent directory needs `x` for the path to resolve: `namei -l /srv/app/data/file`
  shows where the chain breaks.
- Deleting someone else's file needs only `w`+`x` on the directory — unless the **sticky bit**
  (`chmod +t`, `/tmp`) restricts it to the file owner.

## 3. Recursive the right way
```bash
chmod -R u=rwX,g=rX,o= /srv/share     # X: execute only on directories (and files already executable by someone)
find /srv/share -type d -exec chmod 2750 {} +    # explicit: dirs
find /srv/share -type f -exec chmod 0640 {} +    # files
find /srv/share -type f -perm /o+w -exec chmod o-w {} +   # fix only offenders
```
`chmod -R 755` makes every file executable; `chmod -R 777` is never the fix — find which
directory in the chain lacks `x` or which user/group the process actually runs as.

## 4. Defaults: umask
`umask 027` → new files 640, dirs 750. Set it per user in the shell startup files; check the documentation of your init system and login stack for service-wide defaults.

## Gotchas
- GNU `chmod` ignores symlinks found during a recursive traversal; for a symlink named on the command line it changes the pointed-to file (`-H` is the default, `-L` and `-P` change this). Avoid running it on paths you do not control.
- `chmod` never changes the permissions of a symbolic link itself.
- ACLs (`+` in `ls -l`) can grant more than the mode bits show; read `getfacl` output before concluding.

## Verify
- [ ] `stat -c '%A %a %U:%G %n'` on samples shows intended modes; no regular files gained `x`.
- [ ] `namei -l <path>` shows traverse rights on every parent for the service user (`sudo -u svc test -r <path>`).

## Checked

Documentation check. Checked 2026-10-27 against the man-pages project chmod(1) page (GNU coreutils version, man7.org): the symbolic-mode letters and the X meaning (execute/search only if a directory or already executable by someone), `--reference=RFILE`, `-R` with `-H` default and `-L`/`-P`, and that symlinks met during recursion are ignored while command-line symlinks affect the target. Removed the unconfirmed umask pointers (`UMask=`, login.defs, pam_umask) and the ACL-mask remark.
Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container: symbolic and octal modes, capital X with -R, --reference, find -type d/-type f/-perm /o+w fixes, directory r-without-x and x-without-r behaviour, sticky bit blocking deletion by another user, chmod on a command-line symlink changing its target, umask 027 giving 640/750. Not run: -H/-L/-P variants and ACL interplay (documentation only).
