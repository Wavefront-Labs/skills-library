---
id: computing-software.cloud-infrastructure-engineering.terraform.building-a-local-mirror-with-providers-mirror
name: building-a-local-mirror-with-providers-mirror
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, providers-mirror-command, provider-mirror, filesystem-mirror, network-mirror, air-gapped]
level: practitioner
status: docs-checked
description: "Build a provider mirror with terraform providers mirror: platforms, lock-file use, merging configurations, filesystem or HTTPS network mirror use, and exclusive use via direct."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/providers/mirror", "https://developer.hashicorp.com/terraform/internals/provider-network-mirror-protocol", "https://developer.hashicorp.com/terraform/cli/config/config-file"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform providers mirror`

## Build
`terraform providers mirror [options] <target-dir>` downloads the providers required by the current configuration and copies them into the target directory (available in Terraform v0.13 or later). Terraform creates the path structure expected by filesystem mirrors and fills it with `.zip` files containing the plugins.
```bash
terraform providers mirror \
  -platform=linux_amd64 -platform=darwin_arm64 -platform=windows_amd64 \
  /path/to/tf-mirror
```
Options documented on the command page:
- `-platform=OS_ARCH`: target platform; by default only the platform where you run the command. Repeat the flag for several platforms (for example `linux_amd64`).
- `-lock-file=true`: set to `false` to ignore the provider lock file. By default the command uses the version info in the lock file if the directory was previously initialised.
- `-var 'NAME=VALUE'` and `-var-file=FILENAME`: set root-module input variables, as for other commands.

Re-running the command on an existing mirror directory updates it: for example adding a new `-platform` places those packages without removing packages already downloaded, and the JSON index files are merged. To build one mirror for several configurations, run it in each configuration in turn with the same output directory; Terraform merges the requirements into one set of JSON indices.

## Use it as a filesystem mirror
Packed layout used by the command: `HOSTNAME/NAMESPACE/TYPE/terraform-provider-TYPE_VERSION_TARGET.zip`. Terraform ignores the generated JSON index files when the directory is used as a filesystem mirror.
```hcl
# CLI config: ~/.terraformrc (terraform.rc in %APPDATA% on Windows)
provider_installation {
  filesystem_mirror {
    path    = "/path/to/tf-mirror"
    include = ["registry.terraform.io/*/*"]
  }
  direct {
    exclude = ["registry.terraform.io/*/*"]
  }
}
```
Terraform tries every installation method whose `include`/`exclude` patterns match and picks the newest version across them. To use a mirror exclusively, remove `direct` or exclude those providers from it. If both `include` and `exclude` are set, exclusion wins.

## Serve it as a network mirror
The command also generates `.json` index files that are suitable responses for the network mirror protocol when the directory is uploaded to a static website host. The host must serve `.json` files as `application/json`.
```hcl
provider_installation {
  network_mirror {
    url = "https://mirror.example.com/providers/"
  }
}
```
- The URL must use `https:` and should end with a trailing slash.
- Protocol paths under the base URL: `:hostname/:namespace/:type/index.json` (versions) and `:hostname/:namespace/:type/:version.json` (archives per platform, with optional `hashes`). A 404 means the mirror lacks that provider.
- A network mirror can serve providers from any registry hostname; the hostname in the address is then only an identifier.
- If the CLI configuration has credentials for the mirror's hostname, Terraform sends them on index requests but not when downloading the archives. For a non-443 port, the credentials hostname must include the port.
- Only configure network mirrors you trust: a mirror with a valid TLS certificate can still serve modified providers.

## Gotchas
- A network mirror may host only a subset of platforms; if the response includes `hashes`, Terraform verifies the download, and if it has none, it installs the archive with no verification.
- In the explicit `provider_installation` block you must write the `direct` exclusions yourself; the automatic exclusion applies only to the implied configuration.

## Checked
Date: 2026-11-07. Read in full: the `terraform providers mirror` command page, the provider network mirror protocol page (all operations, authentication, static-website section), and the whole CLI configuration file page (Provider Installation, Implied Local Mirror Directories). Removed as unsupported by those pages: the invented `5.70.0.json` file listing, the nightly "mirror manifest" job, the self-signed certificate and `SSL_CERT_FILE` advice, the `providers lock` advice and the OpenTofu hostname remark, and both Verify items. Code blocks on the pages were read from the text extract; no linked example files exist on these pages.
Method: documentation only; no commands were run.
