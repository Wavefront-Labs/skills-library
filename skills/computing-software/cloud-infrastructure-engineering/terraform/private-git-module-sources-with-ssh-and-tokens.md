---
id: computing-software.cloud-infrastructure-engineering.terraform.private-git-module-sources-with-ssh-and-tokens
name: private-git-module-sources-with-ssh-and-tokens
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, private-git-source, git-ssh-source, git-source, module-source, ci-cd]
level: practitioner
status: docs-checked
description: "Fetch modules from private Git repos: pin with ref, shallow clone with depth, rewrite URLs with git config insteadOf, and use HCP Terraform organization SSH keys."
sources: ["https://developer.hashicorp.com/terraform/language/modules/sources#generic-git-repository", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/ssh-keys", "https://git-scm.com/docs/git-config#Documentation/git-config.txt-urlltbasegtinsteadOf"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Private Git module sources

To access a private Git repository Terraform needs either login credentials (HTTPS) or an SSH key. Module installation
happens at `terraform init`, which clones the module source into a hidden subdirectory of the working directory.

## Pinning
```hcl
module "vpc" {
  source = "git::https://example.com/vpc.git?ref=v1.2.0"
}
```
Without `ref`, Terraform clones the default branch referenced by HEAD. The `ref` query parameter accepts any value the
`git checkout` command supports: a branch, a tag or a SHA-1 hash (use a full SHA for an immutable pin). Changing a
module's `source` requires re-running `terraform init`.

## Shallow clones
Add `depth` to the source URL to pass `--depth` to `git clone`. HashiCorp says `depth=1` suits most cases because
Terraform only uses the selected commit. Shallow clones are supported for GitHub, generic Git and Bitbucket sources.

## Credentials in CI
- Do not put tokens in the `source` string: it is committed with the configuration.
- Git's `url.<base>.insteadOf` setting rewrites any URL starting with the given value to start with `<base>` instead
  (the longest match wins). That lets you keep plain HTTPS or SSH module sources in code and inject the
  authenticated form in CI with `git config`; see your Git host's documentation for the token username and format.
```bash
git config --global url."https://<USER>:<TOKEN>@git.example.com/".insteadOf "https://git.example.com/"
```
- For SSH access, give the runner a key your Git host accepts (the key must not have a passphrase because Git runs
  non-interactively).

## HCP Terraform
- Upload keys in the organization: Settings, then SSH Keys (PEM-formatted private key, no passphrase). Keys can be
  added or deleted in organization settings and the text is never shown again.
- Assign a key to a workspace under Settings, then Integrations "SSH Key" (docs also describe a workspace
  "SSH Key" settings entry with an "Update SSH key" button). Each workspace can use only one key.
- Keys for cloning modules are used only during Terraform runs and are separate from keys used to bring VCS content
  into HCP Terraform.
- Before deleting a key, assign another one to workspaces using it, or their runs cannot clone private modules.
- If you upload an invalid key, upload the correct one and push a new commit for it to take effect.
- The docs call the private module registry an easier way to manage private modules, with no workspace SSH keys.

## Verify
- [ ] A clean CI runner can run `terraform init` with only the deploy key or token secret.
- [ ] No credentials appear in any `source` string or CI log.

## Checked
Confirmed 2026-11-08 against the Terraform module sources/usage page (ref, HEAD default, depth, supported hosts), the
HCP Terraform SSH keys page and the git-config `url.<base>.insteadOf` entry. Removed: the SSH URL example, GitHub
Actions ssh-agent step, ssh-keyscan advice, host-specific token usernames, double-download and Windows notes (not on
the cited pages).
Method: docs-only read of cited pages, 2026-11-08
