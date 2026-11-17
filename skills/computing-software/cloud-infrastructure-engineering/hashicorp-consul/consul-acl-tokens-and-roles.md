---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-acl-tokens-and-roles
name: consul-acl-tokens-and-roles
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, acl-tokens, acl-token, acl-role, service-identity]
level: practitioner
status: docs-checked
description: "Issue Consul tokens and roles with consul acl, use service and node identities, and use expiring tokens."
sources: ["https://developer.hashicorp.com/consul/commands/acl/token/create", "https://developer.hashicorp.com/consul/commands/acl/token/read", "https://developer.hashicorp.com/consul/commands/acl/role/create", "https://developer.hashicorp.com/consul/docs/secure/acl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tokens carry policies, roles and identities. A role is a collection of policies linked to tokens, so you can change a role's policies without touching the tokens. Service identities and node identities generate a policy for registering that service or node.

```sh
consul acl role create -name web-role -policy-name web-team
consul acl token create -description "web agent" -role-name web-role
consul acl token create -description "api svc" -service-identity "api:dc1"
consul acl token create -description "node web-01" -node-identity "web-01:dc1"
consul acl token list
consul acl token read -id 9861      # unique prefix of the AccessorID is accepted
consul acl token read -self         # the token in CONSUL_HTTP_TOKEN
consul acl token delete -id 9861
```

Formats: `-node-identity` is `NODENAME:DATACENTER`; `-service-identity` is `SERVICENAME` or `SERVICENAME:DC1,DC2,...`. `-role-name`, `-policy-name` and the identity flags may be repeated. `-name` is required for `role create`.

Gotchas:
- The anonymous token has AccessorID `00000000-0000-0000-0000-000000000002` and SecretID `anonymous`. It applies when a request carries no token (an agent with no `default` token uses it), so keep its policies minimal.
- `-expires-ttl=<duration>` makes a token expire, for example `-expires-ttl '15m'` on a temporary super-user token.
- The SecretID authorises operations, so treat it as a secret; the AccessorID is the identifier used by `read -id` and `delete -id`.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/acl/token/create, read, delete; commands/acl/role/create; secure/acl (roles and identities). Removed: a claim that secrets cannot be re-read, a claim about deleted roles taking effect immediately, a shell-history remark about `-token`, and the Verify step; all were unsupported by the pages.
Method: documentation only; no commands were run.
