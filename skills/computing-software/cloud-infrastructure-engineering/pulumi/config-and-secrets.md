---
id: computing-software.cloud-infrastructure-engineering.pulumi.config-and-secrets
name: config-and-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-config, config-secret, requiresecret, pulumi-config-set]
level: practitioner
status: docs-checked
description: "Set and read Pulumi stack configuration and secrets with pulumi config, typed getters, namespaces and --secret, in TypeScript and Python."
sources:
  - https://www.pulumi.com/docs/iac/concepts/config/
  - https://www.pulumi.com/docs/iac/concepts/secrets/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration and secrets

```bash
pulumi config set instanceCount 3
pulumi config set aws:region eu-west-1          # provider namespace
pulumi config set dbPassword hunter2 --secret   # encrypted in Pulumi.<stack>.yaml
pulumi config set --path 'tags.team' platform   # structured config
pulumi config get instanceCount
pulumi config                                    # secrets shown as [secret]
pulumi config --show-secrets
pulumi config rm instanceCount
```
```typescript
const cfg = new pulumi.Config();
const n = cfg.getNumber("instanceCount");
const pw = cfg.requireSecret("dbPassword");   // Output<string>, marked secret
const tags = cfg.getObject<{team: string}>("tags");
```
```python
cfg = pulumi.Config()
n = cfg.get_int("instanceCount")
pw = cfg.require_secret("dbPassword")
```

## Gotchas
- Read secrets with `requireSecret` / `getSecret` (`require_secret` / `get_secret` in Python) so the value is marked secret in the program.
- Keys without a namespace belong to the project name; a key like `aws:region` has an explicit namespace and is not tied to the project name.
- `getObject` / `requireObject` return a plain object, not a `Config`; reach into it with ordinary property access.
- Structured values are set with `--path`; combine with `--secret` for an encrypted nested value (`pulumi config set --path --secret 'endpoints[0].token' <value>`).

## Verify
`Pulumi.<stack>.yaml` holds `secure:` ciphertext for each secret; `pulumi config --show-secrets` lists the plaintext values.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Configuration page (`--path`, namespaced keys, `getNumber`, `get_int`, `getObject`/`requireObject`, `requireSecret`/`require_secret`), the Secrets page (`getSecret`, `--secret`, `[secret]`, `secure:` in the stack file, `--path --secret`), the `pulumi config` CLI reference (`--show-secrets`, `rm`) and the stack settings file page. Removed: `requireNumber`/`require_int`/`requireBoolean` (not on the pages read), the claims about `require` losing secretness, derived values staying secret, `pulumi.unsecret`, string-only values, and `pulumi config get ... --show-secrets` (the `config get` page lists only `--path`).
Method: documentation only; no commands were run.
