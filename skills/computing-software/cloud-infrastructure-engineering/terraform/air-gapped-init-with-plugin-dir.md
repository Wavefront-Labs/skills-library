---
id: computing-software.cloud-infrastructure-engineering.terraform.air-gapped-init-with-plugin-dir
name: air-gapped-init-with-plugin-dir
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, plugin-dir, air-gapped-init, terraform-init, offline-install, provider-installation]
level: practitioner
status: docs-checked
description: "Initialise Terraform on air-gapped or locked-down hosts with init -plugin-dir: directory layout, lock file hashes, and how it differs from filesystem_mirror."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/init#plugin-installation", "https://developer.hashicorp.com/terraform/cli/config/config-file#provider-installation", "https://developer.hashicorp.com/terraform/cli/commands/providers/mirror", "https://developer.hashicorp.com/terraform/language/files/dependency-lock", "https://developer.hashicorp.com/terraform/cli/commands/providers/lock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform init -plugin-dir`

## What it does
`-plugin-dir=PATH` forces plugin installation to read plugins only from the
specified directory, as if it had been configured as a `filesystem_mirror` in the CLI
configuration. The docs describe it as a one-time override for exceptional situations
(for example testing a local build of a provider); if you routinely use a filesystem
mirror, configure the installation methods globally instead.

```bash
terraform init -plugin-dir=/opt/terraform/providers -lockfile=readonly
```

`-lockfile=readonly` suppresses lock file changes but verifies checksums against the
information already recorded in the lock file.

## Directory layout (same as a filesystem mirror)
The two supported layouts are `HOSTNAME/NAMESPACE/TYPE/terraform-provider-TYPE_VERSION_TARGET.zip`
(packed, the distribution zip from the origin registry) and
`HOSTNAME/NAMESPACE/TYPE/VERSION/TARGET` (unpacked: a directory holding the extracted zip).
VERSION looks like `2.0.0`; TARGET looks like `linux_amd64`.
```
/opt/terraform/providers/registry.terraform.io/hashicorp/aws/terraform-provider-aws_5.70.0_linux_amd64.zip
/opt/terraform/providers/registry.terraform.io/hashicorp/aws/5.70.0/linux_amd64/
```
With the unpacked layout Terraform tries to symlink the mirror directory instead of copying;
the packed layout prevents that because the zip must be extracted.

Build the directory on a connected machine with `terraform providers mirror`, which
takes one required target directory, creates the filesystem-mirror path structure under
it and fills it with `.zip` files:
```bash
terraform providers mirror -platform=linux_amd64 /tmp/providers
```
`-platform=OS_ARCH` picks the target platform (default: the platform where you run the
command) and can be repeated. Re-running against an existing mirror directory adds
packages without removing earlier ones. The command also writes `.json` index files
(for the network mirror protocol); Terraform ignores them when the directory is used as a
filesystem mirror. Then copy the directory to the isolated host.

## Lock file interaction
- Installing from a mirror (rather than the origin registry) means Terraform cannot record
  checksums for platforms other than the one where `init` ran, so the lock file is not
  usable on other platforms. Pre-populate with `terraform providers lock`, using
  `-platform=` once per platform; `-fs-mirror=PATH` makes it read a filesystem mirror
  instead of the registry.
- Checksums recorded from a mirror are those the mirror reports, not the origin
  registry's signed checksums. To record the signed ones, run `providers lock` without
  `-fs-mirror`/`-net-mirror` on a connected machine.
- `zh:` is a SHA256 of the official `.zip`; the docs say it is not suitable for verifying
  mirrors that use the unpacked layout. `h1:` is computed from package contents, so it
  works for a zip, an unpacked directory, or a recompressed zip.

## -plugin-dir vs filesystem_mirror
| | `-plugin-dir` | `filesystem_mirror` in CLI config |
|---|---|---|
| Scope | one init run | per-user CLI configuration, all working directories |
| Registry | providers are read only from the given directory | falls back to the registry only if a `direct` method is kept; remove it (or `exclude` the providers) to use the mirror exclusively |
| Good for | exceptional one-off situations | routine, permanent use |

## Gotchas
- `-plugin-dir` covers providers only; `init` installs child modules from their `source`
  locations as a separate step (`-get=false` skips it).
- `-get-plugins=false` was removed in Terraform 0.15; do not use it.
- Check TARGET spelling (`linux_amd64`, `darwin_amd64`, `windows_amd64`) matches the host.

## Checked
Date: 2026-11-07

Read the fetched, tag-stripped text of five pages in full: `terraform init` (plugin installation, child module installation, `-lockfile`), CLI config file (provider installation, filesystem_mirror layouts, implied directories, plugin cache), `terraform providers mirror`, `terraform providers lock`, and the dependency lock file page. Code tabs and embedded snippets are not present in the stripped text, so none were opened.

Trimmed as unconfirmed: "repeatable" for `-plugin-dir`; "overrides the provider_installation block"; the packed/unpacked binary file name; the `tar` step; "init fails rather than silently picking another version"; "packed zips verify zh:, unpacked verify h1:"; "disables the implied local mirror dirs"; the "not found in any of the search locations" error text; both Verify steps. Added the `-lockfile=readonly` wording, the `providers lock` mirror behaviour and the removed `-get-plugins` note from the pages. Added the dependency-lock and `providers lock` pages to `sources`.

Method: documentation only; no commands were run.
