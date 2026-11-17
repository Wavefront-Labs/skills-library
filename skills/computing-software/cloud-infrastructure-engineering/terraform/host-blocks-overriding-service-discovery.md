---
id: computing-software.cloud-infrastructure-engineering.terraform.host-blocks-overriding-service-discovery
name: host-blocks-overriding-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, host-block, service-discovery, cli-config, terraform-enterprise, private-registry]
level: practitioner
status: draft
description: "Use CLI config host blocks to override remote service discovery for a hostname, e.g. to point modules.v1 or login.v1 at internal endpoints during migrations and tests."
sources: ["https://developer.hashicorp.com/terraform/cli/config/config-file#host-blocks", "https://developer.hashicorp.com/terraform/internals/remote-service-discovery"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# `host` blocks in the CLI config

## Normal service discovery
For a hostname in a module/provider source (`tfe.example.com/org/vpc/aws`), Terraform
fetches `https://tfe.example.com/.well-known/terraform.json`:
```json
{ "modules.v1": "/api/registry/v1/modules/", "providers.v1": "/api/registry/v1/providers/",
  "login.v1": { "client": "terraform-cli", "authz": "/app/oauth/authorize", "token": "/oauth/token", "ports": [10000, 10010] },
  "tfe.v2": "/api/v2/" }
```

## Overriding it
A `host` block makes Terraform skip the well-known lookup for that hostname and use
the given services instead:
```hcl
# ~/.terraformrc
host "registry.corp.example" {
  services = {
    "modules.v1"   = "https://artifactory.corp.example/artifactory/api/terraform/tf-modules/v1/modules/",
    "providers.v1" = "https://artifactory.corp.example/artifactory/api/terraform/tf-providers/v1/providers/",
  }
}
```

## When it helps
- Keep module source addresses stable (`registry.corp.example/...`) while the backend
  moves between products (TFE, Artifactory, GitLab) by changing only the CLI config.
- Test a self-hosted registry implementation before publishing a well-known file.
- Networks where `/.well-known/` on the vanity hostname is blocked or served by a
  different web app.

## Gotchas
- Service URLs must be absolute HTTPS with trailing slashes as in the protocol.
- Credentials are still keyed by hostname (`credentials "registry.corp.example"` or
  `TF_TOKEN_registry_corp_example`).
- The override is per user/machine; CI runners need the same CLI config, or builds
  break with discovery errors. Ship it via `TF_CLI_CONFIG_FILE`.
- Marked as intended mainly for testing in the docs; prefer a real well-known file for
  production.

## Verify
- [ ] `terraform init` resolves a module from the overridden host with `TF_LOG=DEBUG` showing no `.well-known` request for it.
