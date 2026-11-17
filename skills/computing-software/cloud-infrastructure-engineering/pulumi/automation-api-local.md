---
id: computing-software.cloud-infrastructure-engineering.pulumi.automation-api-local
name: automation-api-local
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, automation-api, localworkspace, create-or-select-stack, local-source]
level: practitioner
status: docs-checked
description: "Drive Pulumi from code using the Automation API with a local workspace: select stack, set config, up and destroy from a project directory."
sources:
  - https://www.pulumi.com/docs/iac/automation-api/
  - https://www.pulumi.com/docs/iac/automation-api/getting-started-automation-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automation API with a local program

Automation API exposes the CLI operations (`up`, `preview`, `refresh`, `destroy`, stack init) as a typed SDK so your code can drive the Pulumi engine. Uses include CI/CD, integration testing, multi-stage deployments and custom CLIs over Pulumi.

A local program is a traditional CLI-driven program with its own directory, a `Pulumi.yaml` and a program file. `LocalWorkspace` is the default workspace; it reads and writes `Pulumi.yaml` and `Pulumi.<stack>.yaml` exactly as the CLI does, so setting config on a stack modifies the stack's yaml file.

```python
from pulumi import automation as auto
stack = auto.create_or_select_stack(stack_name="dev", work_dir="./infra")
stack.set_config("aws:region", auto.ConfigValue(value="us-west-2"))
res = stack.up(on_output=print)
```
```go
stack, err := auto.UpsertStackLocalSource(ctx, stackName, workDir)
```
In TypeScript use `LocalWorkspace.createOrSelectStack(args)` and `stack.setConfig("aws:region", { value: "us-west-2" })`, then `stack.up({ onOutput: console.info })`.

## Gotchas
- The Pulumi CLI must be available at runtime, preinstalled on `PATH` or installed programmatically (`PulumiCommand.install()` in TypeScript, `auto.PulumiCommand.install()` in Python, downloading into the `~/.pulumi/versions/<version>` directory by default; the Java SDK cannot do this).
- Missing Registry provider plugins are downloaded automatically before an operation.
- Resource import through `Stack` needs Pulumi CLI v3.127.0 or later.

## Verify
The result of `up` contains the stack outputs and a summary of changes.

## Checked

Method: docs-checked 2026-11-09 against the Pulumi Automation API overview and Using Automation API pages. Removed unconfirmed claims: secret config flag, envVars advice, update-in-progress lock behaviour, passphrase variable, and the TypeScript workDir example.
