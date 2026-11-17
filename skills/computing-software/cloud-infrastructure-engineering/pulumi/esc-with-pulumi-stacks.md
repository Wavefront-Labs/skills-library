---
id: computing-software.cloud-infrastructure-engineering.pulumi.esc-with-pulumi-stacks
name: esc-with-pulumi-stacks
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, esc-environment-import, pulumi-environment, stack-environment, pulumi-config-esc]
level: practitioner
status: docs-checked
description: "Attach ESC environments to Pulumi stacks with the environment: block in Pulumi.<stack>.yaml and pulumiConfig; merge order, precedence, backend limit."
sources:
  - https://www.pulumi.com/docs/esc/integrations/infrastructure/pulumi-iac/
  - https://www.pulumi.com/docs/esc/environments/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESC with Pulumi IaC

Two pieces connect ESC to a Pulumi program.

1. The `environment` block in the stack config file lists imported environments; they are merged in order, later values overriding earlier ones:
```yaml
# Pulumi.dev.yaml
environment:
  - my-project/common
  - my-project/dev
```
2. The `pulumiConfig` block inside an environment declares what flows in as stack configuration, available through the standard Config API (`config.get()`, `config.require()` and secret variants):
```yaml
values:
  pulumiConfig:
    aws:region: us-west-2
    myApp:apiKey:
      fn::secret: super-secret-value
```
Values wrapped in `fn::secret` arrive as Pulumi secrets: masked in CLI output and encrypted in the state file, as if set with `pulumi config set --secret`. Values under `environmentVariables` are set as process environment variables during Pulumi CLI operations.

Other ways to attach: `pulumi config env add <project>/<environment>` (and `pulumi config env init` to create an environment from a stack's existing config), or `addEnvironments(...)` / `listEnvironments` / `removeEnvironment` in Automation API.

## Gotchas
- ESC requires the Pulumi Cloud backend: stacks in self-managed backends (S3, Azure Blob Storage, local filesystem) cannot reference environments.
- When a key is set both in an environment's `pulumiConfig` and explicitly in the stack config, the explicit stack value wins.
- A stack can only read environments from its own organization; pin a revision or tag by appending `@prod` or a revision number to the name.
- Other patterns: dynamic OIDC credentials, `fn::secret` and external stores, composed environments, and the `pulumi-stacks` provider (replaces `StackReference` outputs).

## Checked
2026-11-03. Confirmed on the ESC with Pulumi IaC page and the ESC Environments page. Removed: `pulumi config env ls`, the stack-file `config:` example, `pulumi config get` display claims, and the missing-environment-at-preview and Verify paragraphs.
Method: documentation only; no commands were run.
