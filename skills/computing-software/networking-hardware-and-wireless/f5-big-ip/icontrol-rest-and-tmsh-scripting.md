---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.icontrol-rest-and-tmsh-scripting
name: icontrol-rest-and-tmsh-scripting
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, icontrol-rest, tmsh, bigip-automation]
level: practitioner
status: draft
description: "Automate BIG-IP with iControl REST (token auth, transactions) and tmsh cli scripts with save and sync discipline."
sources:
  - https://clouddocs.f5.com/api/icontrol-rest/
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iControl REST and tmsh scripting

```
curl -sk -X POST https://bigip/mgmt/shared/authn/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"'$PW'","loginProviderName":"tmos"}'
curl -sk -H "X-F5-Auth-Token: $TOK" https://bigip/mgmt/tm/ltm/pool?%24select=name,monitor
curl -sk -H "X-F5-Auth-Token: $TOK" -H 'Content-Type: application/json' -X POST https://bigip/mgmt/tm/ltm/pool -d '{"name":"p1","monitor":"http"}'
curl -sk -H "X-F5-Auth-Token: $TOK" -X POST https://bigip/mgmt/tm/transaction -d '{}'
curl -sk -H "X-F5-Auth-Token: $TOK" -H 'Content-Type: application/json' -X POST https://bigip/mgmt/tm/util/bash -d '{"command":"run","utilCmdArgs":"-c \"tmsh show sys version\""}'
```
- Auth: HTTP basic or a token (valid for 20 min by default; extend through `/mgmt/shared/authz/tokens/<token>` PATCH `timeout`). Token auth avoids sending the password on every call.
- Objects have `fullPath` URLs where `/` becomes `~` (e.g. `~Common~pool_web`). Subcollections like pool members live at `.../members`.
- Transactions (`X-F5-REST-Coordination-Id` header) group multiple changes atomically; either all apply or none.
- REST changes do not save the config. Run `tmsh save sys config` (REST: `POST /mgmt/tm/sys/config {"command":"save"}`), and sync if it is a device group member.
- tmsh: `tmsh -c "cd /Common; list ltm pool"` for scripting, `tmsh load sys config merge file x.scf`, and `tmsh list ltm virtual one-line` for diffable output. Use `modify ... replace-all-with` for lists to avoid accumulation.
- Gotcha: commands in tmsh/`list` output vary per version; compare the prefilled GUI via the `?options=all-properties`.

Verify: `GET /mgmt/tm/ltm/pool/~Common~p1` returns the object; `tmsh show cm sync-status` after changes in HA.
