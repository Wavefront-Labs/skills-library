---
id: computing-software.systems-network-administration.linux.filesystem-hierarchy-standard
name: filesystem-hierarchy-standard
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fhs, filesystem-hierarchy, directory-layout, usr-merge, var, etc, opt, srv, run, tmp, var-lib, var-log, usr-local, xdg, systemd-tmpfiles, separate-partitions, lpic-1, sysadmin]
level: intro
status: docs-checked
description: "Where things go on Linux (FHS 3.0, usr-merge, systemd conventions): which directory for binaries, config, state, logs, caches and third-party software, and what gets its own partition."
sources:
  - https://uapi-group.org/specifications/specs/linux_file_system_hierarchy/
  - https://systemd.io/MOUNT_REQUIREMENTS/
  - https://www.freedesktop.org/software/systemd/man/latest/tmpfiles.d.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filesystem Hierarchy Standard — putting files where the next admin will look

**Goal:** place binaries, configuration, state and data in the directory the FHS and
systemd expect, so packaging, backups, SELinux labels and read-only roots keep working.

## 1. The map
| Directory | Holds | Notes |
|---|---|---|
| `/bin`, `/sbin`, `/lib*` | symlinks to `/usr/*` on merged-usr systems | `/usr` must be available early (systemd Mount Requirements: initrd) |
| `/usr` | shareable, **read-only** vendor content: `/usr/bin`, `/usr/lib`, `/usr/share` | never hand-edit; package manager territory. `/usr/lib/<pkg>` for private vendor resources; `/etc` overrides vendor defaults |
| `/usr/local` | admin-installed software mirroring `/usr` layout (`bin`, `lib`, `etc`, `share`) | `make install` defaults here; survives distro upgrades |
| `/opt/<vendor-or-pkg>` | self-contained third-party packages (Chrome, Oracle, JetBrains) | config in `/etc/opt/<pkg>`, state in `/var/opt/<pkg>` |
| `/etc` | host-specific config, text, no binaries | `/etc/<x>.d/` drop-ins override `/usr/lib/<x>.d/`; mask vendor file with a same-named symlink to `/dev/null` |
| `/var/lib/<svc>` | persistent service state (databases, package DB, docker) | the thing you back up with the service |
| `/var/log` | logs; `/var/log/journal` for persistent journald | separate partition on anything that can be log-flooded |
| `/var/cache` | regenerable cache (apt/dnf packages, man index) | safe to delete |
| `/var/spool` | queued work (mail, cron, cups) | |
| `/var/tmp` | temp files preserved across reboot (default tmpfiles age 30 d) | |
| `/tmp` | temp, may be tmpfs; default tmpfiles age is 10 d | don't store anything large here |
| `/run` | runtime state since boot: PID files, sockets; flushed at boot | `/var/run` is a symlink to `../run` (systemd tmpfiles var.conf) |
| `/srv` | data served by this host (web roots, ftp, git) | FHS leaves layout to the admin; `/srv/www`, `/srv/nfs` are common |
| `/home`, `/root` | user homes; root's is separate so `/home` can be networked | |
| `/boot` | kernels and other assets used to bring up the system; may be the ESP | a separately mounted ESP goes at `/efi` (UAPI spec) |
| `/dev`, `/proc`, `/sys` | virtual: devices (devtmpfs+udev), process/kernel info, kernel objects | nothing persists here |
| `/mnt`, `/media` | temporary admin mounts / removable media | |

## 2. Rules that keep systems upgradable
- **Config you wrote belongs in `/etc` or `/usr/local/etc`, never in `/usr`.** Package
  upgrades overwrite `/usr`; `/etc` files are preserved (dpkg conffiles, rpm `%config(noreplace)` → `.rpmnew`/`.rpmsave`).
- Prefer drop-ins over editing vendor files: `/etc/systemd/system/foo.service.d/override.conf`,
  `/etc/sysctl.d/90-x.conf`, `/etc/ssh/sshd_config.d/10-x.conf` (works where sshd_config has an
  `Include`; for each sshd keyword the first obtained value wins — number low).
- Service state → `/var/lib/<svc>`, owned by the service user; systemd units can declare
  `StateDirectory=<svc>` to create it with the right ownership (and `LogsDirectory`,
  `CacheDirectory`, `RuntimeDirectory` for `/run/<svc>`).
- Runtime dirs under `/run` vanish at boot; create them with tmpfiles, not a one-off `mkdir`:
  `/etc/tmpfiles.d/myapp.conf` → `d /run/myapp 0755 myapp myapp -`, apply with
  `systemd-tmpfiles --create` (tmpfiles.d(5) type `d`).
- Custom scripts: `/usr/local/sbin` (admin-only) / `/usr/local/bin`; they precede
  `/usr/bin` in the default root `PATH`.
- SELinux labels follow paths: a web root outside the default location needs a `semanage fcontext` rule plus `restorecon -R` (see the SELinux skills).

## 3. Partition layout for servers
Separate at minimum: `/var/log` (floods), `/var` or `/var/lib` (databases, containers),
`/home` (users), `/tmp` as tmpfs or `nodev,nosuid,noexec`. CIS benchmarks ask for
`/var/tmp`, `/var/log/audit`, `/dev/shm` restrictions too (confirm in the benchmark text for your distribution). Keep `/usr` on the root
filesystem unless the initramfs mounts it (systemd Mount Requirements list `/usr` as needed in the initrd).

## 4. Finding what a package put where
```bash
rpm -ql <pkg>; dpkg -L <pkg>                    # file list
rpm -qc <pkg>; dpkg-query -W -f='${Conffiles}\n' <pkg>   # config files
rpm -qf /path; dpkg -S /path                    # which package owns a path
systemd-path                                     # systemd's resolved search paths
```

## Verify
- [ ] Nothing hand-written lives under `/usr` except `/usr/local` (`rpm -Va`/`debsums -c` quiet).
- [ ] Services create their `/run` dirs via tmpfiles or `RuntimeDirectory=` and survive a reboot.
- [ ] `df -h` shows `/var/log` (at least) separate from `/` on servers.

## Checked
2026-10-27. Checked against the UAPI.9 Linux File System Hierarchy specification and systemd Mount Requirements (current systemd docs), systemd tmpfiles.d(5), tmp.conf and var.conf, systemd.exec(5), systemd.unit(5) and sshd_config(5). Confirmed: /boot, /efi, /etc, /home, /opt roles; /etc overrides vendor defaults; /run is flushed at boot; tmpfiles ages of 10 d for /tmp and 30 d for /var/tmp; /var/run symlinked to ../run; StateDirectory, LogsDirectory, CacheDirectory, RuntimeDirectory; tmpfiles d lines; masking with a symlink to /dev/null; sshd_config Include and first-value-wins; /usr needed in the initrd. Removed: the usr-merge date, the 1 GiB boot size, udisks mount path, the /var/www label claim and the version gate on sshd_config.d. The file-hierarchy(7) link in sources now points to the UAPI specification that replaced it. CIS partition requirements are not readable here and are left to the benchmark text.

Method: documentation only; no commands were run.
