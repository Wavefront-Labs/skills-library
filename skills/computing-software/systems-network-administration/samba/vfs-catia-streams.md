---
id: computing-software.systems-network-administration.samba.vfs-catia-streams
name: vfs-catia-streams
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, vfs-catia-streams, catia, streams-xattr, vfs, character-mapping]
level: advanced
status: docs-checked
description: "Map illegal filename characters with vfs_catia and store NTFS alternate data streams in xattrs with vfs_streams_xattr: syntax, prefix default, example."
sources:
  - https://www.samba.org/samba/docs/current/man-html/vfs_catia.8.html
  - https://www.samba.org/samba/docs/current/man-html/vfs_streams_xattr.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vfs catia and streams xattr
catia: `catia:mappings` takes comma-separated `0xSERVER:0xCLIENT` hex pairs. A server-side character in a filename is shown to the client as the mapped one, and the reverse applies.
```
[CAD]
    path = /data/cad
    vfs objects = catia
    catia:mappings = 0x22:0xa8
```
A broader set: `0x22:0xa8,0x2a:0xa4,0x2f:0xf8,0x3a:0xf7,0x3c:0xab,0x3e:0xbb,0x3f:0xbf,0x5c:0xff,0x7c:0xa6`.

Caveat from the page: a mapping must work in both directions. Mapping colon (0x3a) to underscore (0x5f) fails because client-side underscores convert back to colons and lookups break. The page states no defaults.

streams_xattr stores alternate data streams in extended attributes:
- `streams_xattr:prefix`: default `user.DosStream.`; changing it also exposes the streams through the SMB EA interface.
- `streams_xattr:store_stream_type`: default `yes`; whether `$DATA` stream names carry the `:$DATA` suffix.
```
[share]
    vfs objects = streams_xattr
```
It is required for macOS metadata with fruit (see vfs-fruit-time-machine; order catia, fruit, streams_xattr). The shared filesystem must support xattrs, and most filesystems limit xattr size, so large streams may fail; `streams_xattr:max xattrs per stream` (2 to 16, default 1) spreads a stream over several xattrs.

## Checked
2026-11-04: catia mapping syntax, example and caveat, and streams_xattr prefix, store_stream_type, max xattrs per stream and the xattr requirement compared with the vfs_catia and vfs_streams_xattr man pages. Removed: a generic verify line; reworded the xattr requirement to match the page.
Method: documentation only; no commands were run.
