---
id: computing-software.systems-network-administration.samba.winbind-on-ad-dc
name: winbind-on-ad-dc
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, winbind-on-ad-dc, libnss-winbind, dc-winbind, nsswitch, winbind]
level: advanced
status: docs-checked
description: "Use winbindd on a Samba AD DC for file serving: nsswitch.conf, libnss_winbind packages or links, template shell and homedir, and what not to set."
sources:
  - https://wiki.samba.org/index.php/Configuring_Winbindd_on_a_Samba_AD_DC
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# winbind on ad dc
Winbindd on a DC is started by the `samba` service; never start it manually. Check with `ps axf`.

`/etc/nsswitch.conf`:
```
passwd: files winbind
group:  files winbind
```
Keep `files` first. Do not add `winbind` to `shadow` (the page says this can make `wbinfo` fail). Do not use the same user names in local `/etc/passwd` as in the domain.

Libraries: on Debian install `libnss-winbind` and `libpam-winbind`. For source builds, symlink (do not copy) `libnss_winbind.so.2` from the Samba lib dir (`smbd -b | grep LIBDIR`) into the system lib directory for your platform (for example `/lib64/` on RHEL-based x86_64, `/lib/x86_64-linux-gnu/` on Debian), link `libnss_winbind.so` to it, and run `ldconfig`.

Only the winbind template mode is supported on a DC. Optional `[global]` settings:
```
template shell = /bin/bash
template homedir = <homes-root>/%U
```
Defaults are `/bin/false` for the shell and a home directory built from `%D/%U` under the system home root. The page's example override sets `/bin/bash` and a home directory ending in `%U`. Restart the `samba` service afterwards.

Do not set any `idmap config` lines on a DC; the wiki says this is unsupported and makes the `samba` service fail. Winbindd always reads uidNumber and gidNumber from AD (see rfc2307-attributes); objects without them get a locally generated ID stored in `idmap.ldb`. After you set an ID in AD, winbindd uses it only once its cache expires or you run `net cache flush`, and file ownerships must be reset manually.

## Checked
2026-11-04: nsswitch, library links, template defaults, service start and idmap notes compared with the Configuring Winbindd on a Samba AD DC wiki page. Nothing removed beyond the corrected home directory default.
Method: documentation only; no commands were run.
