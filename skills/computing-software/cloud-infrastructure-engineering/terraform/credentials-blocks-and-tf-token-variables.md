---
id: computing-software.cloud-infrastructure-engineering.terraform.credentials-blocks-and-tf-token-variables
name: credentials-blocks-and-tf-token-variables
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tf-token, credentials-block, cli-config, terraform-login, private-registry]
level: practitioner
status: docs-checked
description: "Authenticate the CLI to HCP Terraform and private registries with credentials blocks, TF_TOKEN_host variables, terraform login or a credentials helper, and know the priority."
sources: ["https://developer.hashicorp.com/terraform/cli/config/config-file", "https://developer.hashicorp.com/terraform/cli/commands/login"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `credentials` blocks and `TF_TOKEN_*`

## Priority order
Credentials from an environment variable for a host win over those in the CLI config (including ones saved by `terraform login`). If neither is set, a configured credentials helper is consulted. (Before Terraform 1.2 the CLI config was preferred over `TF_TOKEN_*` variables.) A helper is consulted only for hosts without an explicit `credentials` block, so a `credentials` block overrides the helper for that host.

## Environment variable credentials (Terraform 1.2.0 and later)
Variable name = `TF_TOKEN_` + the hostname with periods encoded as underscores. Its value is used as a bearer authorization token for requests to that host.
```bash
export TF_TOKEN_app_terraform_io="$HCP_TOKEN"     # app.terraform.io
export TF_TOKEN_tfe_example_com="$TFE_TOKEN"      # tfe.example.com
```
- Non-ASCII hostnames must be converted to punycode with the ACE prefix: `例えば.com` becomes `TF_TOKEN_xn--r8j3dr99h_com`.
- Hyphens in hostnames may be encoded as double underscores. The page's example for `café.fr` accepts `TF_TOKEN_xn--caf-dma.fr`, `TF_TOKEN_xn--caf-dma_fr` or `TF_TOKEN_xn____caf__dma_fr`. If several variables evaluate to the same hostname, Terraform uses the one defined last in the OS variable table.

## CLI config file
Location: `terraform.rc` in `%APPDATA%` on Windows; `.terraformrc` in the home directory elsewhere; or the path in `TF_CLI_CONFIG_FILE` (should follow the pattern `*.tfrc`).
```hcl
credentials "app.terraform.io" {
  token = "REPLACE_WITH_TOKEN"
}
```
- You can have several `credentials` blocks, one per host.
- The token must be a user token or a team token; organization tokens cannot be used for command-line Terraform actions.
- The credentials hostname must match the hostname in your module sources and/or backend configuration. If a Terraform Enterprise instance answers on several hostnames, use one consistently. HCP Terraform also answers at `atlas.hashicorp.com`.

## `terraform login`
`terraform login [hostname]` gets a token by launching a web browser on the same host, so it is interactive only; for unattended automation, configure credentials manually. With no hostname it logs in to `app.terraform.io`. By default the token is saved in plain text in `credentials.tfrc.json` and the command tells you where before saving, giving you a chance to cancel. It works with any server supporting the login protocol.

## Credentials helper
```hcl
credentials_helper "example" {
  args = []
}
```
At most one block; the label is the helper's name and `args` is optional. Terraform ships no helpers; write your own to integrate with an existing secrets system.

## Checked
Date: 2026-11-07. Read in full: the CLI configuration file page (Locations, Available Settings, Credentials, Environment Variable Credentials, Credentials Helpers, Priority order) and the `terraform login` page. Removed as unsupported: the "which token type" table (only user and team tokens versus organization tokens is stated), the claimed error strings (`401 Unauthorized`, `Required token could not be found`), the Git-module and OpenTofu remarks, the container-image advice, and both Verify items; the three-way precedence list was rewritten to the page's actual order (environment variable, CLI config, helper). The HCP Europe `app.terraform.io/eu` login note was not carried over.
Method: documentation only; no commands were run.
