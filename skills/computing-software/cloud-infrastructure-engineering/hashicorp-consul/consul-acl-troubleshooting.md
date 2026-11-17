---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-acl-troubleshooting
name: consul-acl-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, acl-troubleshooting, permission-denied, acl-not-found]
level: practitioner
status: docs-checked
description: "Diagnose Consul ACL problems with consul members, catalog nodes, and acl token and policy reads, and reset the ACL system if the management token is lost."
sources: ["https://developer.hashicorp.com/consul/docs/secure/acl/troubleshoot", "https://developer.hashicorp.com/consul/commands/acl/token/read", "https://developer.hashicorp.com/consul/docs/error-messages/consul"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The troubleshooting commands need a token with `write` on the ACL system (the initial management token works).

```sh
consul members                       # agents missing here lack the privileges to register
consul catalog nodes -detailed       # null TaggedAddresses means that agent's ACLs are wrong
consul acl token read -self          # which token am I actually using?
consul acl token read -id <accessor-id> -expanded   # expands the policies and roles
consul acl policy list
consul acl policy read -id <policy-id>
consul monitor -log-level=debug      # server logs
```

Over HTTP, `GET /v1/acl/token/self` with the `X-Consul-Token` header returns the token in use.

Order: run `consul acl token read` first when `consul members` or `consul catalog` give unexpected results.

Gotchas:
- `RPC error making call: ... ACL not found` means ACLs are on but a valid token was not passed. Check the token permissions and that an agent token is provided on each call.
- Only agents that can register themselves in the catalog appear in `consul members`.
- Tokens do not expire unless created with an expiry, so list tokens and delete unused ones.
- Lost the bootstrap token: reset on the leader. Find it with `/v1/status/leader`, run `consul acl bootstrap` to get the reset index from the 403 message, write the index to `acl-bootstrap-reset` in the data directory, and bootstrap again (see `consul-acl-bootstrap`).

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: secure/acl/troubleshoot, commands/acl/token/read (`-self`, `-expanded`), api-docs/acl/tokens (`/acl/token/self`), commands/monitor (`-log-level`), error-messages/consul (ACL not found). Removed: the "Permission denied vs ACL not found" definitions, the claim that agents cache token resolution for `acl.token_ttl` as a diagnosis step, the anonymous-token DNS remark, the AccessorID/SecretID remark, and the Verify step.
Method: documentation only; no commands were run.
