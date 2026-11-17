---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.linux-package-integrity-verification
name: linux-package-integrity-verification
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [package-verification, rpm-verify, debsums, dpkg-verify, binary-tampering, linux-forensics, rootkit, dfir]
level: practitioner
status: docs-checked
description: "Check Linux files against package metadata with rpm -V, dpkg --verify and debsums to spot modified binaries and configs, and know their limits."
sources: ["https://rpm-software-management.github.io/rpm/man/rpm.8.html", "https://man7.org/linux/man-pages/man1/dpkg.1.html", "https://manpages.debian.org/debsums"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package integrity verification (rpm -V, dpkg --verify, debsums)

**Goal:** find modified binaries, configs and damaged files by comparing installed files with the package database. This shows files that differ from what the package manager recorded; it is not proof of a clean system.

## RPM (RHEL, Rocky, SUSE, Fedora)
```bash
rpm -V PACKAGE_NAME                      # verify one installed package
rpm -Va                                  # all installed packages
rpm --verify --noconfig openssh-server   # ignore configuration changes (example from the man page)
rpm -qf /usr/sbin/sshd                   # which package owns a file (-f, --file)
```
- Verify compares size, digest, permissions, type, owner and group of each file with the metadata in the rpm database; by default only files with discrepancies are shown (`--verbose` shows all).
- Output is 9 result characters then an attribute character and the filename. `.` passed, `?` could not be tested; `S` size, `M` mode (permissions and file type), `5` digest, `D` device numbers, `L` link path, `U` user, `G` group, `T` mtime, `P` capabilities differ. Attribute characters include `c` config file, `d` doc, `g` ghost, `l` licence, `m` missingok, `a` artifact.
- Verify-mode options can switch individual checks off (for example `--nodigest`, `--nofiles`, `--nomtime`), so confirm none are set in aliases when you read someone else's output.

## Debian / Ubuntu
```bash
dpkg --verify                  # all packages (-V, since dpkg 1.17.2)
dpkg --verify PACKAGE_NAME
debsums -c                     # changed files only
debsums -ca                    # changed files, including configuration files
debsums -l                     # packages with no checksum list
```
- `dpkg --verify` performs only an md5sum check of file contents against the stored value, and only where the database holds a digest. Its output defaults to the rpm-style format: `??5??????` means the digest check failed, a `c` marks a conffile, and a missing file prints `missing`. The man page says it is an integrity check and not a security verification.
- debsums verifies against `/var/lib/dpkg/info/*.md5sums`, can generate sums from `.deb` archives for packages without a list (`--generate`), and takes `--root=dir` to check another root directory (default `/`). Config files are excluded unless `-a`.
- debsums results: OK, FAILED, REPLACED (replaced by a file from a different package). Its man page warns it is of limited use as a security tool and points to aide, integrit, samhain or tripwire for integrity checking from safe media.

## Trust problems (practice; the pages do not cover forensic use)
- The checks are only as trustworthy as the database and tools. An attacker with root could alter the package database or the verification binaries. Run verification from your analysis system against the mounted image, using options that point at the image root (`--root` for dpkg and debsums; `rpm --root` appears in the rpm page's install example, and the rpm-common(8) page that documents it was not read, so confirm it for verify).
- The md5-based checks are weak against deliberate tampering; compare suspicious files against freshly downloaded packages for the same version.
- Files dropped into directories but not owned by any package are not flagged by verify. Check ownership with `rpm -qf` or `dpkg -S`.
- Expected changes: admin-edited configs, files changed by configuration management.

## High-value targets (practice)
`sshd`, `ssh`, `sudo`, `su`, `login`, `passwd`, PAM modules, `libc`, `ld.so`, `/etc/ld.so.preload` (should normally not exist), `ps`, `ls`, `netstat`, `ss`, `lsof`, `top`, `crond`.

## Self-check
Every non-config digest mismatch is explained, and suspicious binaries are hashed, compared with vendor packages and sent for analysis.

## Checked

2026-11-09. Read in full: rpm(8) man page on rpm.org (verify operation, output characters, attribute characters, verify options, examples), debsums(1) on manpages.debian.org (description, options, results, caveats) and the dpkg(1) man page on man7.org (the --verify, --verify-format, --root and --instdir text). Removed: `dpkg -l` and `rpm -qa --qf` commands as tamper checks, the `prelink -y` advice, `find -newer` workflow, "Debian .md5sums cover only shipped files" phrased as a fact beyond the pages, `dpkg --root` verify example and the `rpm --root -Va` offline example as stated syntax, and the claim "dpkg >= 1.17" for the `??5` format (now "since 1.17.2" for --verify). Trust section and target list are practice.

Method: documentation only; no commands were run.
