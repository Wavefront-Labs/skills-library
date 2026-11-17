---
id: computing-software.systems-network-administration.bash.find-printf
name: find-printf
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, find-printf, find-printf-format, shell-scripting]
level: advanced
status: draft
description: "Format find output with GNU -printf for sizes, times, permissions and NUL-delimited records instead of parsing ls."
sources:
  - https://www.gnu.org/software/findutils/manual/html_mono/find.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# find -printf output formats
**Goal:** structured file listings.
```bash
find . -type f -printf '%s\t%p\n' | sort -n | tail     # size then path
find . -type f -printf '%TY-%Tm-%Td %TH:%TM %p\n'       # modification time
find /etc -type f -printf '%m %u:%g %p\n'               # mode, owner:group
find . -type f -printf '%P\0' | xargs -0 ...            # path relative to start, NUL-terminated
find . -printf '%y %p\n'                                 # file type letter
find . -type f -printf '%i %n %p\n'                      # inode, link count
```
- Directives: `%p` path, `%f` name, `%h` dir, `%s` bytes, `%m` octal perms, `%u/%g` owner, `%T@` mtime epoch, `%A/%C` atime/ctime.
- GNU only; BSD/macOS find has `-print0` and `-exec stat` instead. Version unconfirmed for busybox.
- `\n` and `\0` need escaping in the format string; `-printf` does not add a newline.
- Self-check: sizes in the first column sort numerically.
