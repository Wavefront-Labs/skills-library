---
id: computing-software.cloud-infrastructure-engineering.terraform.cli-configuration-credentials-and-provider-mirrors
name: cli-configuration-credentials-and-provider-mirrors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, cli-config, terraformrc, provider-mirror, network-mirror, filesystem-mirror, terraform-login, credentials, plugin-cache, providers-mirror, air-gapped, dev-overrides, tf-cli-config-file]
level: practitioner
status: docs-checked
description: "Configure .terraformrc/terraform.rc: registry credentials, plugin_cache_dir, filesystem and network provider mirrors for air-gapped CI, and dev_overrides for local builds."
sources: ["https://developer.hashicorp.com/terraform/cli/config/config-file", "https://developer.hashicorp.com/terraform/cli/commands/providers/mirror", "https://developer.hashicorp.com/terraform/internals/provider-network-mirror-protocol", "https://developer.hashicorp.com/terraform/cli/commands/login"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CLI configuration, credentials and provider mirrors

**Goal:** control where Terraform fetches providers and how it authenticates to
registries, so CI does not hammer registry.terraform.io, air-gapped runners still
`init`, and a locally built provider can be tested without publishing.

## 1. Where the CLI config lives
- Unix: `~/.terraformrc`; Windows: `%APPDATA%\terraform.rc`.
- On Windows the file must be named `terraform.rc` (not `terraform.rc.txt`; Explorer can hide
  the extension) in the user's `%APPDATA%` directory.
- Override with `TF_CLI_CONFIG_FILE=/path/to/file.tfrc` (useful in CI); such a file should
  follow the `*.tfrc` naming pattern.
- `terraform login` saves its token in plain text in a local CLI configuration file called
  `credentials.tfrc.json`.
- It is per-user CLI behaviour, separate from your infrastructure configuration.

## 2. Credentials
```hcl
credentials "app.terraform.io" {
  token = "<TOKEN>"
}
```
Prefer the env var form, which needs no file: `TF_TOKEN_app_terraform_io=<TOKEN>`
(hostname with periods → underscores; hyphens may be encoded as double underscores). The
variable supplies the bearer token when the CLI makes service requests to that host.
`terraform login [hostname]` is interactive only (it opens a web browser) and defaults to
app.terraform.io; for unattended automation configure credentials manually. A
`credentials_helper "name" {}` block (at most once) delegates storage to an external
helper program; it is consulted only for hosts not configured in a `credentials` block.
Terraform ships no credentials helpers.

## 3. Plugin cache (fast, still online)
```hcl
plugin_cache_dir = "$HOME/.terraform.d/plugin-cache"
```
or `TF_PLUGIN_CACHE_DIR`. The directory must already exist. `init` still uses the
installation methods to find metadata, then reuses a cached copy and, when possible, symlinks
it. The cache is not guaranteed to be concurrency safe, must not also be a filesystem mirror
directory, and Terraform never deletes old plugins from it. By default Terraform uses a cached
package only if it matches a checksum in the dependency lock file; the setting
`plugin_cache_may_break_dependency_lock_file = true` changes that, and HashiCorp recommends
leaving it unset (commit the lock file instead).

## 4. Filesystem mirror (air-gapped)
Build the mirror on a connected machine from a directory containing your configs:
```bash
terraform providers mirror -platform=linux_amd64 -platform=darwin_arm64 ./mirror
```
`terraform providers mirror` (Terraform 0.13 or later) creates the structure filesystem
mirrors expect, populated with `.zip` files, plus `.json` index files for the network
mirror protocol. By default it uses the lock file's versions if the directory was already
initialised (`-lock-file=true`); re-run it with another `-platform` to add platforms.
Copy `./mirror` to the runner and configure:
```hcl
provider_installation {
  filesystem_mirror {
    path    = "/opt/terraform/mirror"
    include = ["registry.terraform.io/*/*"]
  }
  direct {
    exclude = ["registry.terraform.io/*/*"]
  }
}
```
`init` then does not fetch those providers from the origin registry. Keep
`.terraform.lock.hcl` committed so the mirror is built for the versions you pin. If both
`include` and `exclude` match, `exclude` wins.

## 5. Network mirror (Artifactory, Nexus, internal HTTPS)
```hcl
provider_installation {
  network_mirror {
    url     = "https://artifactory.example.com/artifactory/api/terraform/terraform-remote/providers/"
    include = ["registry.terraform.io/*/*"]
  }
  direct { exclude = ["registry.terraform.io/*/*"] }
}
```
The URL must use `https:` and end with a trailing slash, and the server must implement
the provider network mirror protocol (`:hostname/:namespace/:type/index.json` and
`:hostname/:namespace/:type/:version.json`). The directory `terraform providers mirror`
writes can be uploaded to a static website host that serves `.json` as `application/json`.
Only configure network mirrors you trust: a mirror can serve modified providers.

## 6. dev_overrides (testing a locally built provider)
```hcl
provider_installation {
  dev_overrides {
    "example.com/me/myprovider" = "<GOPATH>/bin"
  }
  direct {}
}
```
`dev_overrides` must appear first in `provider_installation`. `terraform init` still
selects a published version for the lock file, but other commands use the override
directory instead (it should hold an executable named like `terraform-provider-<type>`).
HashiCorp recommends using it only temporarily during provider development, for example
with a separate `dev.tfrc` selected through `TF_CLI_CONFIG_FILE`; see
`computing-software.cloud-infrastructure-engineering.terraform.provider-development-with-the-plugin-framework`.

## 7. Other settings
- `disable_checkpoint = true` disables the upgrade and security bulletin checks that reach
  HashiCorp network services.
- `TF_REGISTRY_CLIENT_TIMEOUT` (default 10s) for slow proxies.
- `TF_IN_AUTOMATION` (any non-empty value) only adjusts human-readable output; purely cosmetic.

## Gotchas
- To use a local mirror exclusively, remove the `direct` method or exclude the providers in
  it; a `provider_installation` block with only `filesystem_mirror` means every matching
  provider must come from the mirror, including ones you forgot to mirror.
- With no `provider_installation` block Terraform uses implied local mirror directories
  (such as `terraform.d/plugins` in the working directory) before `direct`.
- Windows: `terraform.rc` must be in `%APPDATA%` and named exactly that.

## Verify
- [ ] On the air-gapped runner, `terraform init` completes with network disabled.
- [ ] The mirror directory contains a `.zip` for every platform your runners use (`-platform=OS_ARCH`).
- [ ] No `credentials` token is committed; CI uses `TF_TOKEN_<host>`.

## Checked
- 2026-10-28. Confirmed against the Terraform CLI configuration file page (file names and locations, `TF_CLI_CONFIG_FILE` and `*.tfrc`, `TF_TOKEN_*`, `credentials_helper`, `provider_installation` methods and include/exclude, network mirror URL rules and warning, implied mirrors, `plugin_cache_dir` behaviour and lock-file setting, `dev_overrides`, `disable_checkpoint`), the `terraform providers mirror`, `terraform login` and provider network mirror protocol pages, and the CLI environment-variables page.
- Removed: OpenTofu `.tofurc`, the "since 1.4" claim, `CHECKPOINT_DISABLE`, Artifactory and Nexus native support, `host` service-discovery blocks, the error message text, case-sensitivity and token-expiry claims, and the `terraform providers lock` check (not in the fetched pages).
Method: documentation only; no commands were run.
