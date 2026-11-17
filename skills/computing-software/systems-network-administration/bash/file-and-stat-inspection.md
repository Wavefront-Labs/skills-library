---
id: computing-software.systems-network-administration.bash.file-and-stat-inspection
name: file-and-stat-inspection
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, file-command, stat, file-type, magic, mime-type, inode, timestamps, atime-mtime-ctime, birth-time, stat-format, hexdump, xxd, strings, file-management, lpic-1, sysadmin]
level: practitioner
status: gated
description: "Identify what a file is and what its inode says: file/MIME detection, stat -c format strings, the four timestamps, device/inode numbers, and quick content peeks with xxd/strings."
sources:
  - https://man7.org/linux/man-pages/man1/file.1.html
  - https://man7.org/linux/man-pages/man1/stat.1.html
  - https://man7.org/linux/man-pages/man7/inode.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# file and stat — what is this thing, and what does the inode know about it

**Goal:** classify unknown files reliably (extension lies), and read inode metadata in
script-friendly form.

## 1. file — content-based type detection
```bash
file suspicious.bin                     # "ELF 64-bit LSB pie executable, x86-64, dynamically linked, ..."
file -i upload.jpg                      # MIME: image/jpeg; charset=binary
file -b --mime-type *.pdf               # -b: no filename prefix (scripts)
file -L /usr/bin/python3                # follow symlink
file -s /dev/sda1                       # special files: read the block device (filesystem type)
file -z archive.tar.gz                  # look inside compressed files
file -k x                               # keep going: report all matches
```
- Uses magic numbers (`/usr/share/misc/magic.mgc`), then text heuristics. "data" means
  nothing matched — often encrypted, truncated or a raw custom format.
- Text outputs show encoding and line endings: `UTF-8 Unicode text, with CRLF line terminators`
  — the fastest way to spot Windows line endings breaking a script (`#!/bin/bash\r`).
- Shell scripts: `Bourne-Again shell script, ASCII text executable`; `file` does not check
  the executable bit, only the shebang.

## 2. stat — inode fields on demand
```bash
stat file                               # human report
stat -c '%n %s %U:%G %a %y' file        # name size owner mode mtime
stat -c '%i %h %d' file                 # inode, link count, device number
stat -c '%F' /dev/null                  # file type: "character special file"
stat -c '%A %a' /tmp                    # symbolic and octal mode (a sticky world-writable dir shows drwxrwxrwt 1777)
stat -f -c '%T %a/%b blocks free' /     # filesystem stats: type, free blocks
stat -L link                            # follow symlinks
stat --printf '%s\n' *                  # printf-style, no implicit newline
```
Useful format codes: `%s` size bytes, `%b %B` blocks/block size, `%u %g` uid gid,
`%X %Y %Z %W` atime/mtime/ctime/birth as epoch, `%x %y %z %w` same human-readable,
`%N` quoted name with symlink target, `%m` mount point.

## 3. The four timestamps
- **mtime**: content modified (what `ls -l` shows). Set by writes; `touch -d`.
- **ctime**: inode changed (writes, owner, group, link count, mode: inode(7)). `touch`/utime(2) sets only atime and mtime, so ctime is the harder one to forge, but root can still change the clock (gated: unconfirmed, source is paywalled or blocked).
- **atime**: last read; with `relatime` only updated if the previous atime is not later than mtime/ctime, or is more than a day old (mount(8)).
- **birth/crtime**: creation time (btime in inode(7)); not supported by most Linux filesystems per inode(7), and `stat %w` shows `-` when unavailable (gated: unconfirmed, source is paywalled or blocked).
`ls -lc` sorts/shows ctime, `ls -lu` atime.

## 4. Peeking at bytes
```bash
xxd file | head                  # hex + ASCII; xxd -r reverses
hexdump -C file | head           # canonical hex+ASCII (hexdump(1) (gated: unconfirmed, source is paywalled or blocked))
od -c file | head                # octal/char dump — shows \r \n explicitly
strings -n 8 binary | grep -i version   # -n: minimum length, default 4 (binutils (gated: unconfirmed, source is paywalled or blocked))
head -c 16 file | xxd            # magic bytes only
```

## 5. Scripting idioms
```bash
[[ $(file -b --mime-type "$f") == text/* ]] && echo "text file"
newer=$(stat -c %Y a) ; older=$(stat -c %Y b); (( newer > older )) && echo "a is newer"
size=$(stat -c %s "$f")      # portable alternative: wc -c < "$f"
```
macOS/BSD `stat` uses `-f` for format and different codes — guard with `uname` if
scripts must be portable.

## Failure modes
- `file` says "data" for a known type: the first bytes are corrupted/truncated — compare
  with `xxd | head -1` against the format's magic.
- Script "No such file or directory" despite existing: `file script.sh` reports CRLF, or the
  interpreter in the shebang is missing (`file` shows the shebang path).
- `stat` output differs between hosts: BSD vs GNU; use `stat --version` to detect.
- ctime appears "modified" after a backup: rsync/chown touched the inode; mtime unchanged.

## Verify
- [ ] `file -b --mime-type` on a renamed file (e.g. `.txt` that is a PNG) reports the true type.
- [ ] `stat -c %Z` increases after `chmod` while `%Y` stays the same (inode(7) (gated: unconfirmed, source is paywalled or blocked)).
