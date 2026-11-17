---
id: computing-software.cloud-infrastructure-engineering.terraform.setup-opentofu-in-ci
name: setup-opentofu-in-ci
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, setup-opentofu, opentofu, github-actions, tofu-wrapper, ci-pipeline, version-pinning]
level: practitioner
status: docs-checked
description: "Install and pin OpenTofu in CI with opentofu/setup-opentofu: version inputs, the output wrapper, the install script, the OCI image and tenv."
sources:
  - https://github.com/opentofu/setup-opentofu
  - https://opentofu.org/docs/intro/install/
  - https://get.opentofu.org/install-opentofu.sh
  - https://github.com/tofuutils/tenv
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# setup-opentofu in CI

## GitHub Actions
```yaml
jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: opentofu/setup-opentofu@v2
        with:
          tofu_version: 1.8.5          # pin exactly; or tofu_version_file: .opentofu-version
          tofu_wrapper: false          # see below
      - run: tofu init -input=false
      - run: tofu plan -input=false -out=tfplan
```
- `tofu_version` accepts an exact version or a constraint (for example `~1.6.0`); with no version it defaults to latest.
- `tofu_version_file` points at a file such as `.opentofu-version`; if both inputs are given, the file's version takes precedence.
- `tofu_wrapper` (default `true`) wraps the binary to expose `stdout`, `stderr` and `exitcode` as step outputs. If exit codes or output formats misbehave, set it to `false`.
- `cli_config_credentials_token` and `cli_config_credentials_hostname` write credentials into the CLI config for a Terraform Cloud/Enterprise-style host (hostname defaults to `app.terraform.io`).

## Other ways
- Official installer script: `curl -fsSL https://get.opentofu.org/install-opentofu.sh | sh -s -- --install-method standalone --opentofu-version <version>`. `--install-method` is required; values include auto, deb, rpm, apk, snap, brew and standalone. Read the script before piping it to a shell.
- OpenTofu publishes an OCI container image on the GitHub Container Registry for container-based CI; see the install page for the current image name and tags.
- tenv (tofuutils/tenv) is a version manager for OpenTofu, Terraform, Terragrunt, Terramate and Atmos, for runners and laptops that juggle versions.

## Pitfalls
- Mixing tools on one state: switch a root module completely, and test a plan with the other tool before committing.
- Version constraints written for Terraform in `required_version` may not match OpenTofu's version numbers; check them against `tofu version`.

## Verify
- [ ] CI logs print `tofu version` equal to the pinned version on every job.
- [ ] Plans run without the wrapper interfering with JSON parsing.

## Checked
2026-10-28. Confirmed against the setup-opentofu README (inputs `tofu_version`, `tofu_version_file`, `tofu_wrapper`, `cli_config_credentials_*`, precedence, wrapper outputs), the OpenTofu install script (`--install-method`, values, `--opentofu-version`), the OpenTofu install page (OCI image, standalone method), and the tenv README (what it manages).
Corrected: the action version (`opentofu/setup-opentofu@v1` in the skill; the README uses `@v2`).
Removed: the provider plugin cache section (the fetched pages document `TF_PLUGIN_CACHE_DIR` for Terraform only), the GitLab OpenTofu component details (the component page returned only a stub), the Atlantis `TF_BINARY` / `--tf-distribution` setting and its version, `.tofu-version` with tenv, `tenv tofu install` syntax, the exact `ghcr.io` image tag, registry hostname in the lock file, and the state-compatibility claim about Terraform versions above 1.6 (none confirmed in the fetched pages).
Method: documentation only; no commands were run.
