---
id: computing-software.networking-hardware-and-wireless.check-point.management-api-mgmt-cli
name: management-api-mgmt-cli
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, management-api, mgmt-cli, api-login]
level: practitioner
status: draft
description: "Automate Check Point management through the Management API with mgmt_cli, login sessions, and publish and install steps."
sources:
  - https://sc1.checkpoint.com/documents/latest/APIs/
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CommandLineInterfaceReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Management API with mgmt_cli and web services

```
api status
api start ; api restart
mgmt_cli login user admin password '...' domain "System Data" --format json > id.txt
mgmt_cli -s id.txt add host name "h1" ip-address "10.1.1.1"
mgmt_cli -s id.txt publish
mgmt_cli -s id.txt install-policy policy-package "Standard" access true targets.1 "gw1"
mgmt_cli -s id.txt logout
curl -k -H "Content-Type: application/json" -d '{"user":"admin","password":"..."}' https://mgmt/web_api/login
```
- Enable access to the API in SmartConsole: Manage & Settings > Blades > Management API > Advanced Settings > **Accessible from** (management only / all IPs / specific) and restart: `api restart`. Check `api status` for "API readiness test SUCCESSFUL".
- On the management server itself, `mgmt_cli -r true <command>` runs as the local superuser ("root login", no password) and also publishes automatically only when you call `publish`.
- Every command needs `publish` (or `discard`) to commit. Batch many `add` operations in one session, then publish once; unpublished sessions can remain locked until timeout.
- Use `--format json` and a JSON parser (`jq`) to read results; most `show` commands support `limit`, `offset`, and `details-level full`. The reference is in the online API documentation per version.
- Output "code": "generic_err_object_not_found" and "message" show the failing parameter. The API version may be pinned in the URL `/web_api/v1.9/` (confirm your version).
- Gotcha: API keys/passwords in scripts; use `login-as-root` or API keys (`api-key` login, R81+) stored in a secrets manager, not hard-coded.

Verify: `mgmt_cli -r true show hosts limit 5 --format json`; the change appears in SmartConsole's audit log under the API user.
