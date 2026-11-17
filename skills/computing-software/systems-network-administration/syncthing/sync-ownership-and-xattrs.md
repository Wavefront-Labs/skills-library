---
id: computing-software.systems-network-administration.syncthing.sync-ownership-and-xattrs
name: sync-ownership-and-xattrs
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, syncownership, syncxattrs, extended-attributes]
level: advanced
status: docs-checked
description: "Synchronise file ownership and extended attributes in Syncthing and grant the capabilities required on Linux."
sources: ["https://docs.syncthing.net/advanced/folder-sync-ownership.html", "https://docs.syncthing.net/advanced/folder-send-ownership.html", "https://docs.syncthing.net/advanced/folder-sync-xattrs.html", "https://docs.syncthing.net/advanced/folder-xattr-filter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ownership and extended attributes

## Options
- `syncOwnership` (since 1.21.0) applies ownership from peers. `sendOwnership` (1.22.0) records and sends it. A peer needs one of the two for data to exist.
- `syncXattrs` and `sendXattrs` (since 1.22.0) do the same for extended attributes.

Unix UID and GID travel with user and group names. The receiver looks up the name first and falls back to the number. Windows ownership uses account names. Ownership does not cross between POSIX and Windows, but foreign data is passed along. Xattrs are per operating system, and moving a file on Linux can lose macOS xattrs. Supported for xattrs as of 1.22.0: Linux, macOS, FreeBSD, NetBSD. Scanning ownership on Windows has a fairly significant performance impact, and scanning xattrs may too.

## Privileges
A normal user cannot change ownership. Options: run as root (for example in a container), or grant capabilities:

```sh
sudo setcap CAP_CHOWN,CAP_FOWNER=pe /path/to/syncthing
```
The binary must be root-owned and not user-writable. Automatic upgrades would undo this, and with systemd you can set capabilities in the unit instead.

## xattr filter
The filter field appears after enabling Sync Extended Attributes. Rules are first-match. With no rules everything is permitted, but once one exists the default flips to deny, so add a final `*` permit rule if needed.

## Checked

2026-11-09. Confirmed against the Syncthing syncOwnership, sendOwnership, syncXattrs, sendXattrs and xattrFilter pages (advanced/folder-*, raw rst from syncthing/docs): version gates, peer requirement, UID/GID name lookup order, POSIX/Windows separation, xattr per-OS rule and move caveat, supported OS list, CHOWN and FOWNER capabilities and setcap line, root-owned binary, upgrade caveat, systemd alternative, filter default and first-match rules. Removed: the blanket "both features cost performance" (the pages say Windows ownership scans are significantly slower and xattr scans may be).

Method: documentation only; no commands were run.
