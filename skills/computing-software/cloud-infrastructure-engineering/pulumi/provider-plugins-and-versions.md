---
id: computing-software.cloud-infrastructure-engineering.pulumi.provider-plugins-and-versions
name: provider-plugins-and-versions
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, plugin-install, provider-version, pulumi-plugin, plugin-ls]
level: practitioner
status: docs-checked
description: "Install Pulumi provider plugins ahead of time with pulumi plugin install and pin a provider version with the version resource option."
sources:
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_plugin_install/
  - https://www.pulumi.com/docs/iac/concepts/providers/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider plugins and versions

Providers are a kind of plugin (a resource plugin). The first `pulumi preview` or `pulumi up` installs any required providers missing from the plugin cache, so installing by hand is only needed to warm a CI cache or prepare a machine that will run without network access.

```bash
pulumi plugin install                                  # compute the set the current project needs (may download more than strictly necessary)
pulumi plugin install resource aws 6.50.0              # KIND NAME VERSION
pulumi plugin install resource aws 6.50.0 --exact      # exact version only (usually >= is accepted)
pulumi plugin install resource aws 6.50.0 --server <URL>   # download from another URL
pulumi plugin install resource aws 6.50.0 --file <path>    # from a binary, folder or tarball, no download
pulumi plugin install resource aws 6.50.0 --checksum <SHA256> --reinstall
```
`KIND` is one of `analyzer`, `language`, `resource`, `converter`, `tool`. `VERSION` must be a specific number, never a range; if omitted for a non-language plugin Pulumi looks up the latest version (not guaranteed). `--parallel` limits concurrent installs (default 4).

Pin per resource with the `version` resource option (custom resources only), which sets the provider plugin version used for that resource:

```typescript
new aws.s3.Bucket("b", {}, { version: "6.50.0" });
```

## Gotchas
- A `version` of a language plugin shipped with the CLI never needs installing; only third-party language plugins do.
- Pre-installing without a cache in CI means each run downloads the provider again; use the install command to warm the cache.
- Version ranges are rejected by `plugin install`; use an explicit number.

## Checked
2026-11-03. Confirmed on the `pulumi plugin install` CLI page (synopsis, kinds, flags, version rules), the Providers concept page (CLI installs missing providers on first preview/up) and the Resource options page (`version`, custom only). Removed: `plugin ls`/`plugin rm`, `PULUMI_HOME`, `~/.pulumi/plugins` path, `GITHUB_TOKEN`, size claim, `pulumi about` Verify paragraph, mixed-version claim, the `aws.Provider` version example.
Method: documentation only; no commands were run.
