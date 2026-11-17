---
id: computing-software.cloud-infrastructure-engineering.terraform.vault-dynamic-cloud-and-database-credentials
name: vault-dynamic-cloud-and-database-credentials
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, vault-dynamic-secrets, vault, secrets-management, ephemeral-resource, aws-secrets-engine]
level: practitioner
status: docs-checked
description: "Use Vault dynamic secrets with Terraform: configure AWS and database secrets engines, and read short-lived credentials through ephemeral resources."
sources:
  - https://registry.terraform.io/providers/hashicorp/vault/latest/docs/ephemeral-resources/aws_access_credentials
  - https://registry.terraform.io/providers/hashicorp/vault/latest/docs/ephemeral-resources/database_secret
  - https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/aws_secret_backend
  - https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/aws_secret_backend_role
  - https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/database_secrets_mount
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault dynamic secrets with Terraform

Terraform has two roles here: **configuring** Vault secrets engines as code, and **consuming** short-lived credentials from them.

## Configure an AWS secrets engine
```hcl
resource "vault_aws_secret_backend" "aws" {
  path                      = "aws"
  region                    = "<REGION>"
  default_lease_ttl_seconds = 900
  max_lease_ttl_seconds     = 3600
  # Vault's own AWS credentials: access_key plus secret_key_wo (write-only)
  # or the standard AWS environment/shared-file/IAM role credentials on the Vault side
}
resource "vault_aws_secret_backend_role" "deploy" {
  backend         = vault_aws_secret_backend.aws.path
  name            = "deploy"
  credential_type = "assumed_role"
  role_arns       = ["arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>"]
}
```
- `credential_type` is one of `iam_user`, `assumed_role` or `federation_token`. `role_arns` is required for `assumed_role` and prohibited otherwise; `iam_user` and `federation_token` need at least one of `policy_document` or `policy_arns`.
- `default_sts_ttl` and `max_sts_ttl` (seconds) on the role apply only to `assumed_role` and `federation_token`.
- `secret_key_wo` plus `secret_key_wo_version` keep the secret key out of state and require Terraform 1.11+; incrementing the version triggers an update.

## Configure a database engine
```hcl
resource "vault_database_secrets_mount" "db" {
  path = "database"
  postgresql {
    name              = "payments"
    username          = "<ROOT_USER>"
    password_wo       = var.vault_admin_password
    password_wo_version = 1
    connection_url    = "postgresql://{{username}}:{{password}}@<DB_HOST>:5432/payments"
    verify_connection = true
    allowed_roles     = ["app"]
  }
}
resource "vault_database_secret_backend_role" "app" {
  backend = vault_database_secrets_mount.db.path
  db_name = vault_database_secrets_mount.db.postgresql[0].name
  creation_statements = [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";",
  ]
}
```
The provider docs list `password_wo_version` for each database block; see the provider's guide on write-only attributes for how updates work. The mount resource also has root-credential rotation settings (`root_rotation_statements`, and `rotation_schedule` / `rotation_window`; some options need Vault Enterprise 1.19+): check the resource page before relying on them.

## Consume: ephemeral resources
```hcl
ephemeral "vault_aws_access_credentials" "deploy" {
  mount    = vault_aws_secret_backend.aws.path
  role     = vault_aws_secret_backend_role.deploy.name
  type     = "sts"
  role_arn = "arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>"  # only needed if the role has several ARNs
}
provider "aws" {
  alias      = "workload"
  access_key = ephemeral.vault_aws_access_credentials.deploy.access_key
  secret_key = ephemeral.vault_aws_access_credentials.deploy.secret_key
  token      = ephemeral.vault_aws_access_credentials.deploy.security_token
}
```
- `type` is `creds` (IAM user credentials, the default) or `sts`; `security_token` is only present for `sts`; `ttl` applies only to `sts` (otherwise the role's `default_sts_ttl`).
- The provider docs state these credentials are not stored in Terraform state. Exported attributes also include `lease_id`, `lease_duration`, `lease_start_time` and `lease_renewable`.
- For databases, `ephemeral "vault_database_secret"` takes `mount`, `name` (the role) and `mount_id`.

## Verify
- [ ] State does not contain cloud or database credentials (inspect the state file for the secret key and password values).
- [ ] The Vault role TTLs are long enough for the longest apply.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the vault provider docs source in hashicorp/terraform-provider-vault (ephemeral `vault_aws_access_credentials`, ephemeral `vault_database_secret`, `vault_aws_secret_backend`, `vault_aws_secret_backend_role`, `vault_database_secrets_mount`) and the AWS provider docs (`access_key`, `secret_key`, `token`). Corrected: the ephemeral resource uses `mount` (not `backend`) and `type` is `creds` or `sts`. Removed as not confirmed: the Terraform 1.10+ version gate for ephemeral resources, the claim that the older data source writes credentials to state and that leases expire between plan and apply, the advice to run `vault write -f database/rotate-root/...` (the Vault API pages were not readable), IAM user propagation delays, the "audit log" check and the `state pull | grep` command. The Vault engine docs (developer.hashicorp.com/vault) could not be fetched in raw form, so engine behaviour beyond the provider pages is not claimed.
