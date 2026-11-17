---
id: computing-software.cloud-infrastructure-engineering.terraform.tflint-custom-rule-plugins
name: tflint-custom-rule-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, tflint-plugin, tflint, tflint-ruleset, custom-lint-rules, tflint-plugin-sdk, policy-linting]
level: practitioner
status: docs-checked
description: "Write and ship custom TFLint rule plugins with tflint-plugin-sdk: ruleset template, how plugins run, plugin block settings, signing, install location and GitHub rate limits."
sources:
  - https://github.com/terraform-linters/tflint-plugin-sdk
  - https://github.com/terraform-linters/tflint-ruleset-template
  - https://github.com/terraform-linters/tflint/blob/master/docs/user-guide/plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tflint custom rule plugins

Use when organisation rules aren't covered by built-in or provider rulesets: mandatory tags, naming conventions, banned resource types, module source pinning.

## How plugins work
- TFLint launches a plugin as a sub-process and talks to it over gRPC (go-plugin). The plugin is the server and TFLint the client sending inspection requests.
- Plugins are written in Go against `tflint-plugin-sdk`. Start from the `tflint-ruleset-template` repository, which has an example plugin using the SDK and example rules; copy its rule structure rather than writing one from memory, and read the SDK repository for the runner API.
- The binary must be named `tflint-ruleset-<name>` (`.exe` on Windows).

## Using a published plugin
```hcl
# .tflint.hcl
plugin "acme" {
  enabled = true
  version = "<VERSION>"
  source  = "github.com/<ORG>/tflint-ruleset-acme"
  # signing_key = <<-KEY ... KEY    # PGP public key, when the release is signed
}
```
```bash
tflint --init     # installs plugins declared with source and version
```
- `source` must be `github.com/org/repo`. `version` has no `v` prefix, cannot be omitted when `source` is set, and does not support constraints such as `>= 0.3`.
- Signature verification with a PGP `signing_key` is available (the docs list `pgp` as a verification mode).
- Installed plugins go to `~/.tflint.d/plugins` (or `./.tflint.d/plugins` if that already exists in the working directory), under `[plugin dir]/[source]/[version]/tflint-ruleset-[name]`.
- `tflint --init` calls the GitHub API; unauthenticated that is limited to 60 requests per hour per IP address. Set `GITHUB_TOKEN` to raise it (in GitHub Actions the built-in token works). For GitHub Enterprise Server use a host-specific `GITHUB_TOKEN_<host>` with `_` for `.` and `__` for `-`; it falls back to `GITHUB_TOKEN`.

## Local development
Omit `source` and `version`, and place the built binary named `tflint-ruleset-<name>` directly in the plugins folder (`~/.tflint.d/plugins/` on Unix-like systems). Manual installs also suit plugins not published on GitHub.

## Verify
- [ ] Unit tests for the rule cover pass, fail and unknown-value cases.
- [ ] CI runs `tflint --init` and fails on rule violations, with the plugin version pinned.

## Checked
2026-10-31. Confirmed against the tflint-plugin-sdk README (sub-process over gRPC, template
reference), the tflint-ruleset-template README, and the TFLint plugins user guide (`source`
format, `version` rules, `signing_key` / `pgp`, install directories and layout, GitHub
rate limit and `GITHUB_TOKEN` handling, manual install and naming). Removed: the Go rule and
test code (SDK function names and the `gh repo create` command could not be confirmed from
the fetched pages), GoReleaser and GPG signing workflow claims, the sample plugin
version, and the `tflint --recursive --format compact` invocation.
Method: documentation only; no commands were run.
