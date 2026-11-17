---
id: computing-software.devops-ci-cd.nomad.identity-block
name: identity-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, workload-identity, identity-block, identity, nomad-token, jwt, aud, ttl, change-mode, consul-identity, consul-default, oidc, hcl]
level: advanced
status: docs-checked
description: "Expose Nomad workload identity JWTs to tasks with identity blocks using name, aud, ttl, env, file, filepath, change_mode, and configure consul_default identities for Consul auth."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/identity.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad identity block (workload-identity)

Nomad creates a **default** workload identity for every workload but does not expose it to the task. `identity` blocks (task, service, or task-level service) expose it, or define extra named identities for Vault, Consul or an external OIDC provider.

```hcl
task "api" {
  identity {
    env         = true
    file        = true
    filepath    = "local/example.jwt"
    change_mode = "restart"
  }
  identity {
    name          = "example"
    aud           = ["oidc.example.com"]
    file          = true
    ttl           = "1h"
    change_mode   = "signal"
    change_signal = "SIGHUP"
  }
}
```

## Parameters
- `name` (`"default"`) - unique per task; only one block may omit it.
- `aud` - audience list; always set it for non-default identities.
- `ttl` - lifetime, renewed at roughly half the TTL. Not allowed on the default identity; always set it on non-default ones.
- `env` (`false`) - put the token in `NOMAD_TOKEN`.
- `file` (`false`) - write it to `secrets/nomad_token`. Readable only by `task.user` if set, otherwise readable by all but guarded by parent directory permissions.
- `filepath` - with `file = true`, path relative to the task working directory instead of the secrets directory.
- `change_mode` (`"noop"`) - on token renewal: `noop` (task reloads when its token is rejected), `restart` (needed to pick up a changed env var), or `signal` (requires `change_signal`, for example `"SIGHUP"`).

Combine with the Task API so tasks can call the Nomad API.

## Consul
Add identity blocks to the task or service that talks to Consul. Servers can auto-add defaults via the `consul.service_identity` and `consul.task_identity` agent settings when a job has a `consul` block or Consul-provider services. **Jobs with `template` blocks get no default identities**, because Nomad cannot inspect template data; declare them. Task identity names must be `consul_<cluster name>`; in Community Edition that is `consul_default`. Service identities need no name. Enterprise: the name must match the task's `consul.cluster`.

```hcl
service {
  provider = "consul"
  identity { aud = ["consul.io"] ttl = "1h" }
}
task "httpd" {
  identity { name = "consul_default" aud = ["consul.io"] ttl = "1h" }
}
```

## Checked

2026-11-03. Confirmed against the identity job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
