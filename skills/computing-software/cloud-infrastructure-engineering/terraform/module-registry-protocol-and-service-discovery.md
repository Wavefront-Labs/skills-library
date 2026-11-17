---
id: computing-software.cloud-infrastructure-engineering.terraform.module-registry-protocol-and-service-discovery
name: module-registry-protocol-and-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, registry-protocol, service-discovery, well-known-terraform, gitlab-module-registry, private-registry, self-hosted-registry]
level: advanced
status: docs-checked
description: "Understand the module registry protocol and /.well-known/terraform.json service discovery, and use self-hosted or GitLab registries with credentials."
sources: ["https://developer.hashicorp.com/terraform/internals/module-registry-protocol", "https://developer.hashicorp.com/terraform/internals/remote-service-discovery", "https://docs.gitlab.com/user/packages/terraform_module_registry/", "https://developer.hashicorp.com/terraform/cli/config/config-file#credentials"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry protocol and service discovery

## Module addresses
`hostname/namespace/name/system`. The `hostname/` part is optional and defaults to
`registry.terraform.io/`, so `hashicorp/consul/aws` is shorthand for
`registry.terraform.io/hashicorp/consul/aws`. You only need to implement the protocol to
publish modules whose addresses use a different hostname that you control.

## Service discovery
For a source like `registry.acme.com/platform/vpc/aws`, Terraform forms
`https://registry.acme.com/.well-known/terraform.json` (HTTPS, fixed path) and sends a GET.
- A non-200 status, a media type other than `application/json`, or an unparseable body
  means discovery fails and the host is treated as supporting no Terraform-native services.
- Redirects are followed (at least one is guaranteed; nested redirects are not recommended).
- The JSON keys are service identifiers (type name, a period and a version). In use:
  `login.v1`, `modules.v1` and `providers.v1`. The value is the base URL, absolute or
  relative (relative values resolve against the final discovery URL).
```json
{ "modules.v1": "/terraform/modules/v1/" }
```
- Make the base URL end with a slash so the protocol's relative paths resolve correctly.
- Hostnames are normalised (including lower-casing). A non-standard port is allowed in the
  hostname for development, but providing discovery on port 443 is strongly recommended.
- Credentials for the hostname are included in the discovery request when available.

## Module registry protocol (modules.v1)
Paths below are relative to the `modules.v1` base URL.
- `GET :namespace/:name/:system/versions` returns JSON
  `{"modules":[{"versions":[{"version":"1.0.0"}, ...]}]}`. The first element of `modules` is
  the requested module and Terraform ignores other elements (third parties should return a
  single-element list). Terraform matches the versions against the `version` constraints in
  configuration. Return 404 if no such module exists.
- `GET :namespace/:name/:system/:version/download` returns `204 No Content` with an
  `X-Terraform-Get` header and no body. Its value accepts the same values as a module `source`
  argument, except that it cannot refer to another registry address. A relative URL
  (starting with `/`, `./` or `../`) is resolved against the download endpoint URL.
- Terraform assumes versions follow Semantic Versioning 2.0.

## Using GitLab as a private registry
GitLab project packages can act as a module registry. The source is
`<host>/<top-level-namespace>/<module-name>/<module-system>`:
```hcl
module "vpc" {
  source = "gitlab.acme.com/parent-group/vpc/aws"
}
```
Project and group names in the path must not include a dot (`.`), and versions should follow
SemVer. GitLab authenticates with a personal access token (at least `read_api`), a CI/CD
job token, or a deploy token with `read_package_registry` or `write_package_registry`.

Credentials in the CLI config (`~/.terraformrc`, or `terraform.rc` in `%APPDATA%` on Windows):
```hcl
credentials "gitlab.acme.com" {
  token = "<token>"
}
```
or an environment variable (Terraform 1.2.0 and later): `TF_TOKEN_` plus the hostname with
periods encoded as underscores, e.g. `TF_TOKEN_gitlab_acme_com`. Hyphens in hostnames may be
encoded as double underscores. The environment variable is preferred over CLI config
credentials, which are preferred over a credentials helper. The credentials hostname must
match the hostname in your module sources. GitLab's docs say environment variables are
preferred for enterprise setups and a `credentials` block suits local or temporary use.

## Debugging
```bash
curl -s https://registry.acme.com/.well-known/terraform.json
curl -s -H "Authorization: Bearer $TOKEN" https://registry.acme.com/terraform/modules/v1/platform/vpc/aws/versions
```
The second URL assumes the example discovery document above; use the base URL your registry advertises.

## Gotchas
- The registry only points at the code; the `X-Terraform-Get` value is installed like any
  other module source, so it must be fetchable with whatever access the CLI has.
- A third-party registry is supported only by Terraform CLI 0.11 and later.

## Checked
Date: 2026-11-07. Read in full: Module Registry Protocol Reference, Remote Service Discovery Protocol Reference, the GitLab Terraform Module Registry page, and the CLI config file page (Credentials, Environment Variable Credentials, priority order). Confirmed: address syntax and default host, discovery URL and failure rules, redirect and relative-URL rules, service identifiers, versions and download endpoints and the X-Terraform-Get rules, CLI 0.11 note, GitLab source format and token types, dot restriction, TF_TOKEN_ encoding and the 1.2.0 note, credential priority. Trims: replaced the login.v1 example (grant_types/authz fields are not on the pages) with the page's modules.v1 example, removed the list of registry products (Artifactory, Nexus, Terrareg, Boring Registry, citizen), the `TF_LOG=DEBUG ... grep` debugging step, the OpenTofu default-host claim and the Verify steps. HCP Terraform / Terraform Registry HTTP API extensions were not read.
Method: documentation only; no commands were run.
