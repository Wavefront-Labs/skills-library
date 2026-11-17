---
id: computing-software.cloud-infrastructure-engineering.pulumi.esc-environments
name: esc-environments
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-esc, esc-environment, esc-run, esc-open]
level: practitioner
status: docs-checked
description: "Define Pulumi ESC environments (values, fn::secret, dynamic providers, imports, outputs) and open them with pulumi env open, get and run."
sources:
  - https://www.pulumi.com/docs/esc/concepts/
  - https://www.pulumi.com/docs/esc/environments/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESC environments

An environment is the unit of organization in Pulumi ESC: a named, versioned YAML document of config and secrets. It combines static values, secrets, dynamic values from providers (clouds via OIDC) and values imported from other environments. Every definition has a top-level `values` key, optionally with `imports` to compose others. Every change creates a new immutable revision.

```yaml
values:
  environment: production                    # static
  stripeApiKey:
    fn::secret: sk_live_abc123               # encrypted on save
  aws:
    login:
      fn::open::aws-login:                   # dynamic, fetched at open time
        oidc:
          roleArn: arn:aws:iam::123456789012:role/esc-oidc
          sessionName: pulumi-esc
  environmentVariables:                      # reserved output: process env vars
    AWS_ACCESS_KEY_ID: ${aws.login.accessKeyId}
    AWS_SECRET_ACCESS_KEY: ${aws.login.secretAccessKey}
    AWS_SESSION_TOKEN: ${aws.login.sessionToken}
  pulumiConfig:                              # reserved output: Pulumi stack config
    environment: ${environment}
    stripeApiKey: ${stripeApiKey}
```
Other reserved outputs project values to temporary files and to policy packs (`policyConfig`).

**CLI (`pulumi env`).**
```bash
pulumi env open <org>/<project>/<env-name>                 # evaluate; secrets decrypted
pulumi env get  <org>/<project>/<env-name> database.password   # one value by property path
```
`pulumi env run` injects an environment's config and secrets into any command. The `pulumi env` subcommands cover initialize, list, get/set, edit, open, run, diff and tag versions, clone and delete. The console offers Open and a Show secrets toggle.

**Evaluation.** Opening resolves imports, runs providers for dynamic values, decrypts secrets for authorized users, evaluates interpolations and functions, and applies precedence. Dynamic values are never persisted; credentials are fresh on each open.

## Gotchas
- After save, `fn::secret` shows ciphertext when re-edited; plaintext is returned only to users with the open permission.
- Built-in environment permission sets: Environment Read, Open, Write, Admin. Open (decrypt/fetch credentials) is separate from Write (edit).
- A stack can only read environments from its own Pulumi organization; pin a revision or tag with `myapp/dev@prod`.
- One common layout is an environment per stage (`myapp/dev`, `myapp/staging`, `myapp/prod`) with shared values imported.

## Checked
2026-11-03. Confirmed on the ESC Concepts and Environments pages. Removed: the standalone `esc` binary commands (`esc env init/edit/get --value json --show-secrets`, `esc run`, `esc env version tag`), `DB_PASSWORD` example, import override ordering claim, `PULUMI_ACCESS_TOKEN` requirement and the grep Verify.
Method: documentation only; no commands were run.
