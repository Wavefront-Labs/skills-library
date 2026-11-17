---
id: computing-software.networking-hardware-and-wireless.powerdns.pdnsutil-backend-tools
name: pdnsutil-backend-tools
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pdnsutil, b2b-migrate, backend-lookup, bench-db, hash-password, test-schema, ipcipher]
level: advanced
status: docs-checked
description: "pdnsutil utility commands: b2b-migrate, backend-cmd, backend-lookup, bench-db, test-schema, hash-password, ipencrypt, ipdecrypt, create-bind-db."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdnsutil.1.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pdnsutil backend and utility tools

- `b2b-migrate OLD NEW`: migrate data between backends; needs `launch=OLD,NEW`.
- `backend-cmd BACKEND CMD [CMD]...`: send a raw command to a backend.
- `backend-lookup BACKEND NAME [TYPE [CLIENT_IP_SUBNET]]`: look records up in one backend.
- `bench-db [FILE]`: benchmark the database with zone names from FILE (default powerdns.com).
- `test-schema ZONE`: test the schema by creating ZONE.
- `create-bind-db FILENAME`: SQLite DNSSEC database for the BIND backend.
- `hash-password [WORK_FACTOR]`: read a password from stdin and print a salted hash; the scrypt work factor is a power of two, default 1024.
- `ipencrypt IP PASSPHRASE_OR_KEY [key]` and `ipdecrypt IP PASSPHRASE_OR_KEY [key]`: encrypt or decrypt an IP address per the ipcipher standard; add `key` when the passphrase is a base64 key.
- `list-algorithms [with-backend]`: supported DNSSEC algorithms, optionally with the crypto library.
- `raw-lua-from-content TYPE CONTENT`: format record content for dnsdist's SpoofRawAction.

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdnsutil.1.rst.

Method: documentation only; no commands were run.
