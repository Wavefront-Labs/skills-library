---
id: computing-software.systems-network-administration.samba.idmap-backend-choice
name: idmap-backend-choice
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, idmap-backend-choice, idmap, id-mapping, winbind, domain-member]
level: practitioner
status: docs-checked
description: "Choose a winbind idmap backend for a Samba domain member: ad versus rid versus autorid, the default star domain, range planning and overlap rules."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_a_Domain_Member
  - https://www.samba.org/samba/docs/current/man-html/idmap_rid.8.html
  - https://www.samba.org/samba/docs/current/man-html/idmap_ad.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# idmap backend choice
- `ad`: reads RFC2307 `uidNumber`/`gidNumber`, which you add in AD yourself. Use when IDs must match everywhere or shells/homes live in AD.
- `rid`: computes IDs from the RID; nothing is added to AD and RFC2307 data is ignored. Identical `[global]` on every member gives identical IDs.
- `autorid`: allocates a range per domain; the wiki says using `*` for everything fits only this backend.

Rules:
- Each domain using `rid` or `ad` needs its own `idmap config DOMAIN : ...` entries with disjoint ranges.
- `rid` and `ad` cannot be the default; a writable `*` backend (`tdb` or `ldap`) is required for BUILTIN SIDs, other domains and group mappings, with a range not overlapping the others.
- The `range` is a filter that stops local and remote IDs colliding.

Wiki-suggested ranges for `ad`: `*` 3000-7999, `DOMAIN` 10000-999999, `TRUSTED` 1000000-9999999.

Winbind templates (when AD does not supply them): `template shell` default `/bin/false`; `template homedir` default is a `%D/%U` path under the home root. Set in `[global]`.

Never add `idmap config` on an AD DC.

## Checked
2026-11-04: backend guidance, rules, suggested ranges and template defaults compared with the Setting up Samba as a Domain Member wiki page and the idmap_rid and idmap_ad man pages. Nothing removed.
Method: documentation only; no commands were run.
