---
id: computing-software.messaging-and-integration.prosody.storage-per-store-config
name: storage-per-store-config
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, storage, default-storage, stores, sql]
level: practitioner
status: docs-checked
description: "Mixing Prosody storage backends per store with the storage table and default_storage, plus the common store names such as accounts, roster, archive and pep."
sources:
  - https://prosody.im/doc/storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-store storage configuration

Roster in SQL, everything else on the default:

```lua
storage = {
    roster = "sql";
}
```

Everything in SQL except accounts:

```lua
default_storage = "sql"
storage = {
    accounts = "internal";
}
```

Usually a store has the same name as the module using it; community modules may use additional stores. Examples from the page's table: `accounts` (mod_auth_internal_plain, mod_auth_internal_hashed), `roster` (mod_roster, rostermanager), `vcard` (mod_vcard), `archive` (mod_mam), `muc_log` (mod_muc_mam), `offline` (mod_offline), `pep` and `pep_data` (mod_pep).

## Checked

2026-11-04: confirmed against prosody.im/doc/storage (both examples and the common stores table). Removed a generic verify line.
Method: documentation only; no commands were run.
