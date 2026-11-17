---
id: computing-software.systems-network-administration.linux.finding-documentation-with-man-and-info
name: finding-documentation-with-man-and-info
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, man, man-pages, documentation, info-pages, info, apropos, whatis, mandb, manpath, help, usr-share-doc, tldr, man-sections, less, pinfo, rhcsa, lfcs, sysadmin, help-builtin, type-command]
level: intro
status: docs-checked
description: "Find Linux documentation fast: man sections, apropos/whatis, mandb, info navigation, bash help, /usr/share/doc, and why a man page is missing."
sources:
  - https://man7.org/linux/man-pages/man1/man.1.html
  - https://man7.org/linux/man-pages/man7/man-pages.7.html
  - https://www.gnu.org/software/texinfo/manual/info-stnd/info-stnd.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Finding documentation with man and info — answer "what does this flag do" offline

**Goal:** locate authoritative documentation for a command, config file, syscall or
concept on the box in front of you, in the right section, without a search engine.

## 1. Man sections — the number is the whole trick
| Section | Contents | Example |
|---|---|---|
| 1 | User commands | `man 1 passwd` |
| 2 | System calls | `man 2 open` |
| 3 | Library functions | `man 3 printf` |
| 4 | Devices, special files | `man 4 null` |
| 5 | File formats and configs | `man 5 passwd`, `man 5 fstab`, `man 5 sshd_config` |
| 6 | Games | |
| 7 | Conventions, overviews | `man 7 signal`, `man 7 hier`, `man 7 regex` |
| 8 | Admin commands | `man 8 mount` |

`man passwd` returns section 1 (the command). The file format you wanted is
`man 5 passwd`. Same name, different section is common: `crontab(1)` vs `crontab(5)`,
`systemd.unit(5)` vs `systemd(1)`. List every section a name exists in:
```bash
man -f fstab           # same as whatis
man -k 'disk usage'    # same as apropos: search names + one-line descriptions
man -a mount           # show all sections in turn
man -w sshd_config     # path of the source file (useful for grep)
```
`apropos`/`whatis` read the index database that mandb(8) builds; if a search finds nothing, run `sudo mandb`.

Inside `man` (pager is `less`): `/pattern` search, `n`/`N` next/previous, `g`/`G` top/bottom,
`h` help, `q` quit. Jump straight to a term with `LESS='+/--color' man ls` (less `+cmd`).

## 2. Navigating a man page quickly
- `SYNOPSIS` shows argument grammar: `[ ]` optional, `...` repeatable, `|` alternatives.
- `SEE ALSO` is the fastest route to the config file (`sshd(8)` → `sshd_config(5)`).
- `ENVIRONMENT` and `FILES` sections explain why a command behaves differently for
  root vs a user or under cron.
- Print a page to plain text for grep or sharing: `man -P cat ls` or `man ls | col -b`.
- Read a page in another language or from another path: `man -L C ls`,
  `man -M /opt/app/share/man app`.

## 3. `info` — where GNU tools keep the full manual
GNU projects keep their full manual in Texinfo and the man page can be shorter.
`info sed`, `info coreutils 'ls invocation'`. Press `?` inside info for the key list.

## 4. Bash builtins and `--help`
Builtins such as `cd` are described in `bash(1)` and by the `help` builtin:
```bash
help cd
help -m read          # man-page-like layout
type -a time          # prints all places that contain a command of that name; -t gives alias, keyword, function, builtin or file
```
Many commands accept `--help` or `-h`; `systemctl --help`, `git help <sub>`, `docker <cmd> --help`
and `kubectl explain` are in-tool equivalents.

## 5. Package docs: `/usr/share/doc`
Examples, READMEs, changelogs, and often the *only* copy of a daemon's full
configuration reference:
```bash
ls /usr/share/doc/<package>/              # README.Debian, examples/, NEWS.gz
zless /usr/share/doc/<package>/changelog.Debian.gz
rpm -qd <package>                         # RHEL: list doc files in a package
dpkg -L <package> | grep -E 'man|doc'     # Debian: where did the docs go
```
On RHEL/Fedora documentation is often split into separate `-doc` subpackages.
Minimal images often strip docs; reinstall the package after removing the exclusion rule, or
install `man-db` (`apt install man-db manpages`; `dnf install man-db man-pages`).

## 6. When the page is missing or wrong
- `No manual entry for X`: the command exists but docs weren't installed (see 5), or
  `MANPATH` is wrong — `manpath` prints it; packages in `/opt` or `/usr/local` need
  their `share/man` added to `/etc/manpath.config` or `MANPATH`.
- The page is for a different version than the binary: `man --path`/`man -w` and
  compare with `which`/`command -v`. Locally built tools in `/usr/local/bin` with
  distro man pages in `/usr/share/man` are the usual cause.
- The kernel's own docs are online at `docs.kernel.org`; `man 7 cgroups` and `man 5 proc` are admin-facing pages.
- Community cheat-sheet tools such as `tldr` give examples, not authority;
  use them for syntax reminders, not for flags you will put in production.

## Verify
- [ ] `man 5 passwd` opens the file-format page, not the command.
- [ ] `apropos partition` returns results (if not, `sudo mandb` fixed it).
- [ ] `help -m cd` prints builtin docs; `info coreutils` opens the manual (if the info reader and manual are installed).
- [ ] `ls /usr/share/doc/<a package you use>` shows example configs.

## Checked
2026-10-27. Checked against Debian man(1) and mandb(8) (man-db, trixie), man-pages man-pages(7) for the section list, the less manual source, and the bash(1) manual for help -m and type -a/-t. Confirmed: man -f, -k, -a, -w/--path, -l, -L, -M, -P, --warnings, -E, -T devices including pdf; MANPATH, MANPAGER, MANWIDTH, MANOPT; sections 1 to 8; /etc/manpath.config is the man-db configuration file; mandb builds the index caches; the less +cmd and search keys. Removed: makewhatis, the Texinfo key list, pinfo, package and path specifics for Debian and RHEL images, the kernel-doc path and tldr package names. The GNU Info manual in sources is not readable from this environment, so no Info key bindings are stated beyond the ? help key.

Method: documentation only; no commands were run.
