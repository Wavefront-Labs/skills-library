---
id: computing-software.cloud-infrastructure-engineering.terraform.vault-provider-auth-login-methods
name: vault-provider-auth-login-methods
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, vault-auth-login, vault-provider, provider-authentication, oidc, jwt-auth]
level: practitioner
status: docs-checked
description: "Authenticate the Vault provider without static tokens using auth_login blocks: JWT from CI, AWS, AppRole, and HCP Terraform Vault-backed dynamic credentials."
sources: ["https://raw.githubusercontent.com/hashicorp/terraform-provider-vault/main/website/docs/index.html.markdown", "https://developer.hashicorp.com/vault/docs/auth/jwt", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/dynamic-provider-credentials/vault-configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault provider `auth_login_*`

By default the Vault provider creates a short-lived intermediate (child) token for Terraform to use. Instead of `VAULT_TOKEN`, use
an `auth_login*` block.

## JWT/OIDC from CI (GitHub Actions)
```hcl
provider "vault" {
  address = "https://vault.example.com:8200"
  auth_login_jwt {
    mount = "jwt-github"             # default: jwt
    role  = "terraform-payments"
    jwt   = var.ci_id_token          # or env TERRAFORM_VAULT_AUTH_JWT
  }
}
```
Vault side: `vault write auth/jwt-github/role/terraform-payments role_type=jwt
bound_audiences=https://github.com/corp bound_claims='{"repository":"corp/payments-infra"}'
user_claim=sub policies=terraform-payments ttl=30m`.

## AWS IAM (runner on AWS)
```hcl
auth_login_aws {
  role = "terraform"
  # mount defaults to "aws"; credentials come from arguments or AWS_* env vars
}
```

## AppRole and other mounts without a dedicated block
There is no dedicated block for every method (the provider docs list userpass, aws,
cert, gcp, kerberos, radius, oci, oidc, jwt, azure and token_file); use the generic
`auth_login` block with the mount's login `path`.
```hcl
auth_login {
  path = "auth/approle/login"
  parameters = {
    role_id   = var.role_id
    secret_id = var.secret_id
  }
}
```

## HCP Terraform
Vault-backed dynamic credentials: set `TFC_VAULT_PROVIDER_AUTH=true`,
`TFC_VAULT_ADDR`, `TFC_VAULT_RUN_ROLE` on the workspace; HCP injects a token via its
workload identity JWT. No auth block needed. On the Vault side the JWT role uses
`role_type`, `bound_audiences`, `bound_claims`, `user_claim`, `token_ttl` and
`policies` (see the HCP Terraform Vault configuration page).

## Gotchas
- The intermediate token TTL is `max_lease_ttl_seconds` (default 20 minutes, env
  `TERRAFORM_VAULT_MAX_TTL`). Data sources are read at plan time and the result is
  stored in the plan, so an `apply` run after the token expires will likely fail.
- `skip_child_token = true` is strongly discouraged: it raises the chance of a renewable
  token being exposed, and makes `token_name` and `max_lease_ttl_seconds` be ignored. Use
  it only when the token cannot create child tokens.
- Secrets read by Vault data sources are written into the state and plan.

## Verify
- [ ] No `VAULT_TOKEN` stored in CI; Vault audit log shows logins via the chosen method.

## Checked
2026-10-31. Confirmed against the terraform-provider-vault index docs (raw GitHub, because the registry page renders as a stub), the Vault JWT auth page and the HCP Terraform Vault dynamic-credentials page: `auth_login_jwt`/`auth_login_aws`/generic `auth_login` blocks and their defaults, `TERRAFORM_VAULT_AUTH_JWT`, `max_lease_ttl_seconds` default 20 minutes, `skip_child_token` behaviour, `TFC_VAULT_PROVIDER_AUTH`/`TFC_VAULT_ADDR`/`TFC_VAULT_RUN_ROLE`, JWT role fields. Removed: the `auth_login_kubernetes` block (not in the provider docs), the sts:GetCallerIdentity comment and the TF 1.10 ephemeral-resource claim.
Method: documentation only; no commands were run.
