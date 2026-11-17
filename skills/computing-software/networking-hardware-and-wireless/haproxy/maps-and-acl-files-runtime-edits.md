---
id: computing-software.networking-hardware-and-wireless.haproxy.maps-and-acl-files-runtime-edits
name: maps-and-acl-files-runtime-edits
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, map-file, add-map, set-map, acl-file, show-map, pattern-reference]
level: practitioner
status: docs-checked
description: "Use HAProxy map files and ACL pattern files, and edit them live with show, add, set and del map or acl, or swap them atomically by version."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# maps and acl files runtime edits
`/etc/haproxy/hosts.map` holds one key and value per line:
```
shop.example.com     be_shop
api.example.com      be_api
```
```
frontend fe_web
    use_backend %[req.hdr(host),lower,map(/etc/haproxy/hosts.map,be_default)]
    acl banned src -f /etc/haproxy/banned.lst
```
Map converters: `map(<map_name>[,<default>])` is an alias for `map_str`; the general form is `map_<match_type>[_<output_type>]`. Match types include `str`, `beg`, `sub`, `dir`, `dom`, `end`, `reg`, `regm` (string input), `int` and `ip`; output types are `str` (default), `int`, `ip` and `key`. If the key is not found the converter returns the default; without a default it fails as if no input could be fetched (so supply a default). The `key` output type returns the matched entry's key and does not accept a default. `map_regm` substitutes back references such as `\1` in the value.

- Keys that overlap: IP addresses and strings are stored in trees (the finest match wins); other key types are kept in lists (first match wins).
- File format: one key and value per line; empty lines and lines starting with `#` are ignored; leading blanks are stripped; the key is the first word and the value is the rest of the line without trailing blanks.
- ACL pattern files (`-f <file>`): each line is one pattern, with the same comment and blank rules; several `-f` can be given. `-M` loads the file as a two-column map so an ACL can check for a key's existence. A file is always identified by its name even if `-u <id>` forces an id.

Runtime commands (stats socket, see the runtime API skill), where `<map>` is the `#<id>` or name shown by `show map`:
```
show map /etc/haproxy/hosts.map
add map /etc/haproxy/hosts.map blog.example.com be_blog
set map /etc/haproxy/hosts.map shop.example.com be_shop2
del map /etc/haproxy/hosts.map blog.example.com
add acl /etc/haproxy/banned.lst 203.0.113.9
del acl /etc/haproxy/banned.lst 203.0.113.9
```
- `add map` and `add acl` do not check whether the entry already exists. `add map <map> <<` followed by lines accepts several key/value pairs in one payload.
- `show map` and `show acl` without an argument list all maps or ACLs. With a name, the first column of the dump is an entry identifier usable as `#<ref>` with `del map` and `set map`; the second is the pattern, the third the sample.
- `set map <map> [<key>|#<ref>] <value>` changes the value of the matching entries; `del map <map> [<key>|#<ref>]` deletes all entries with that key, or only the one reference.
- A name shared by a map and an ACL means entries are shared: deleting or clearing one affects the other, and `add acl` cannot be used on a name also used as a map (use `add map`).
- Atomic replacement: `prepare map <map>` allocates a new version (reported as `next_ver`); `add map @<ver> ...` fills it, where entries do not match until `commit map @<ver> <map>` swaps it in atomically. `clear map [@<ver>] <map>` empties one.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual (map converter text and file format, ACL `-f`/`-M`/`-u` flags) and management guide (`add map`, `add acl`, `set map`, `del map`, `del acl`, `show map`, `show acl`, `prepare map`, `commit map`, `clear map`). Removed: the `map_beg` redirect example, the `-M` claim about `_ip`/`_str` variants, the claim that runtime changes are lost on reload, the requirement of admin level, and the `curl` verify line. Read as sections of both documents only.
Method: documentation only; no commands were run.
