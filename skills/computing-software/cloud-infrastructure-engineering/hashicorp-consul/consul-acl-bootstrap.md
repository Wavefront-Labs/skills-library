---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-acl-bootstrap
name: consul-acl-bootstrap
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, acl-bootstrap, acl-bootstrap-token, default-policy-deny]
level: practitioner
status: docs-checked
description: "Enable ACLs with default deny, bootstrap the management token once, store it securely, and know the reset path for a lost token."
sources: ["https://developer.hashicorp.com/consul/commands/acl/bootstrap", "https://developer.hashicorp.com/consul/docs/secure/acl/bootstrap", "https://developer.hashicorp.com/consul/docs/secure/acl/reset"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable ACLs in the config of every server and client, then do a rolling restart, then bootstrap once on a server.

```hcl
acl {
  enabled                  = true
  default_policy           = "deny"
  enable_token_persistence = true
}
```

```sh
consul acl bootstrap -format=json > bootstrap.json   # keep out of git
export CONSUL_HTTP_TOKEN=$(jq -r .SecretID bootstrap.json)
```

`consul acl bootstrap` needs no ACL token. The bootstrap token gets the `global-management` policy (unrestricted), and the token can be created only once; afterwards bootstrapping is disabled. Optionally pass a file (or `-`) holding the Secret ID to use instead of a generated one. Give the management token to only a few ACL administrators, store it securely, and use it just to create tokens and policies for agents and services (the docs recommend Vault for storing them).

Gotchas:
- `default_policy = "deny"` is an allowlist: only explicitly allowed operations work. On an existing datacenter, enable ACLs first with `default_policy = "allow"`, create and apply the agent tokens, then switch to `deny` with another rolling restart.
- `enable_token_persistence` stores tokens set through the API or CLI on disk and reloads them after restart.
- Lost every `global-management` token: the reset runs on the current leader. Run `consul acl bootstrap` again; the 403 message gives the reset index ("ACL bootstrap no longer allowed (reset index: N)"). Write N into a file named `acl-bootstrap-reset` in the agent's data directory, then run `consul acl bootstrap` again to get a new management token. Existing tokens stay in place.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source (commands/acl/bootstrap, secure/acl/bootstrap, secure/acl/reset, reference/agent/configuration-file/acl): the HCL fields, `-format={pretty|json}`, required ACL `none`, one-time bootstrap, optional Secret ID file, reset index and `acl-bootstrap-reset` file, allow-then-deny rollout on an existing datacenter. Removed: the invented Verify step (anonymous `consul members` denied), the AccessorID-in-logs remark, and the "confirm details" hedge on the reset procedure.
Method: documentation only; no commands were run.
