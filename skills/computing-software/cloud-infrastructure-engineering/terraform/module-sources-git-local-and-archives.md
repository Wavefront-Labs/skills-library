---
id: computing-software.cloud-infrastructure-engineering.terraform.module-sources-git-local-and-archives
name: module-sources-git-local-and-archives
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, module-sources, git-source, ref-subdir, local-module, local-path-source, archive-source, s3-module-source]
level: practitioner
status: docs-checked
description: "Reference modules from git (ref, //subdir, depth, SSH vs HTTPS auth), local paths, and S3/GCS/HTTP archives, and how installs and upgrades work."
sources: ["https://developer.hashicorp.com/terraform/language/block/module", "https://developer.hashicorp.com/terraform/language/modules/sources", "https://developer.hashicorp.com/terraform/cli/commands/init"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module sources: git, local, archives

`source` must be a literal string, or reference constant input variables (declared with
`const = true`) and locals. Run `terraform init` after changing `source`.

## Local paths
```hcl
module "network" {
  source = "./modules/network"       # must start with ./ or ../
}
```
- Paths beginning with `/` or a drive letter are absolute and are copied to the module cache as
  a package; HashiCorp does not recommend them because they couple the configuration to one machine's filesystem.
- The `version` argument applies only to modules from a registry. Local-path modules always share the caller's version.

## Git
```hcl
module "vpc" {
  source = "git::https://example.com/vpc.git//network/vpc?ref=v2.3.1"
}
module "vpc_ssh" {
  source = "git::ssh://git@example.com/vpc.git//network/vpc?ref=v2.3.1"
}
module "gh_short" {
  source = "github.com/hashicorp/example//modules/vpc?ref=v1.2.0"
}
```
- `//subdir` marks the rest of the path as a sub-directory of the package. Put query
  parameters such as `ref` after the sub-directory. Terraform extracts the entire package
  but reads the module from the sub-directory.
- `ref` takes a branch name, full or short SHA-1 hash, or tag name. Without it Terraform uses the
  default branch referenced by HEAD. Pin a tag or SHA; a branch can move.
- `depth` makes a shallow clone (supported for GitHub, generic Git and Bitbucket sources).
  With `depth`, `ref` is passed to `git clone --branch`, so it must be a named branch or tag,
  not a raw commit ID.
- Terraform runs `git clone` using your local Git configuration and credentials. SSH keys are
  used automatically and are the most common way to reach private repos from automation.
  For HTTP(S), see Git's own docs for credentials. In HCP Terraform you can only authenticate
  with SSH keys.
- `version =` applies only to registry modules; for Git the `ref` selects the version.

## Archives
```hcl
module "lambda" {
  source = "s3::https://s3-eu-west-1.amazonaws.com/examplecorp-terraform-modules/vpc.zip"
}
module "gcs" {
  source = "gcs::https://www.googleapis.com/storage/v1/modules/foomodule.zip"
}
module "http" {
  source = "https://example.com/network-module.zip//modules/vpc"
}
```
- Recognised archive extensions: `.zip`, `.bz2`/`.tar.bz2`/`.tar.tbz2`/`.tbz2`,
  `.gz`/`.tar.gz`/`.tgz`, `.xz`/`.tar.xz`/`.txz`. For another extension on an HTTPS URL, add
  the `archive` query parameter (for example `?archive=zip`).
- S3 credentials are looked up in order: `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`, the
  default profile in `.aws/credentials`, then the EC2 instance profile. Buckets in `us-east-1`
  must use the hostname `s3.amazonaws.com`.
- GCS credentials: `GOOGLE_OAUTH_ACCESS_TOKEN`, a service account key path in
  `GOOGLE_APPLICATION_CREDENTIALS`, default credentials on a GCE instance, or
  `gcloud auth application-default login`.
- A plain HTTP(S) URL gets a `terraform-get=1` query parameter; Terraform reads the module
  address from the `X-Terraform-Get` header or a `terraform-get` meta tag. HTTPS URLs that
  end in a known archive extension skip this and use the archive directly.
- Prefer immutable, versioned object names (practice advice).

## Installing and upgrading
- `terraform init` retrieves module sources into a hidden subdirectory of the working directory.
- Re-running init installs newly added modules but does not change already-installed ones.
  `-upgrade` overrides this and updates all modules to the latest available source code.
- Changing `source`, or the `version` of a registry module, requires re-running `terraform init`.

## Gotchas
- Because Terraform extracts the entire package, a module in a sub-directory can use a local
  path to reference another module in the same package.
- A branch ref without a pin can change under you; use a tag or SHA in production.

## Checked
Date: 2026-11-07. Read in full: the "module block reference" page (the Terraform sources page now redirects to the "Use modules in your configuration" page, also read in full) and the `terraform init` command page (Child Module Installation). Confirmed: literal-string/const rule, local paths and absolute-path note, `//` sub-directory and query ordering, `ref` values and default, `depth` semantics and the branch/tag-only restriction, SSH/credential behaviour, HCP SSH-only rule, archive extensions and `archive` parameter, `terraform-get=1`, S3 and GCS credential orders, us-east-1 hostname, init and `-upgrade` behaviour. Trims: removed the `git config ... insteadOf` command, the claim that local modules need no `init -upgrade`, `modules.json`, the "ref with slashes works", "every module call clones the whole repo" and "lock file does not cover modules" claims, and the grep-based Verify steps; example URLs changed to the page's own example hosts. The OpenTofu module sources page was not read, so it was dropped from sources.
Method: documentation only; no commands were run.
