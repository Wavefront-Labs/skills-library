---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-agent-auto-auth
name: vault-agent-auto-auth
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-agent, auto-auth, agent-template]
level: practitioner
status: docs-checked
description: "Run Vault Agent to authenticate, cache tokens and render secrets into files with templates so applications avoid the Vault API."
sources: ["https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent", "https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent/template", "https://developer.hashicorp.com/vault/docs/agent-and-proxy/autoauth/methods/approle", "https://developer.hashicorp.com/vault/docs/agent-and-proxy/autoauth/sinks/file"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vault Agent handles login, token renewal and secret rendering.

```hcl
auto_auth {
  method "approle" {
    config = { role_id_file_path = "/etc/vault/role-id", secret_id_file_path = "/etc/vault/secret-id", remove_secret_id_file_after_reading = true }
  }
  sink "file" {
    config = {
      path = "/run/vault/token"
      mode = 0640
    }
  }
}
template {
  source      = "/etc/vault/app.ctmpl"
  destination = "/run/app/config.env"
  command     = "systemctl reload app"
}
```

Run `vault agent -config=agent.hcl`.

Gotchas: sinks hold live tokens; the file sink docs advise writing to a ramdisk (ideally encrypted) with appropriate filesystem permissions (default mode 0640, overridable with `mode`). The AppRole method removes the secret ID file after reading it unless `remove_secret_id_file_after_reading = false`. Renewable secrets are renewed after 2/3 of the lease; non-renewable, non-leased secrets are fetched every 5 minutes by default (`static_secret_render_interval`, Vault 1.8+). The template `command` runs only when the rendered output changes and must return within 30s by default (`command_timeout`, deprecated in favour of `exec`). If auto-auth fails the agent backs off with some randomness and retries.

## Checked

2026-11-03. Confirmed on the Vault Agent, Agent template, auto-auth AppRole and file sink pages: `vault agent -config=`, the `auto_auth`/`sink "file"` structure and `mode`, AppRole `role_id_file_path`, `secret_id_file_path` and `remove_secret_id_file_after_reading` (default true), template `source`, `destination`, `command`, the renewal rules, the 5 minute fetch interval and the 30s command timeout, retry with back-off. Fixed the sink example to one attribute per line. Removed: root-user advice, the Kubernetes injector remark, stale-file monitoring advice and the invented Verify step.

Method: documentation only; no commands were run.
