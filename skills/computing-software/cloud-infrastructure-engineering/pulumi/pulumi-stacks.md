---
id: computing-software.cloud-infrastructure-engineering.pulumi.pulumi-stacks
name: pulumi-stacks
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, stack-config, pulumi-stack, stack-init, pulumi.dev.yaml]
level: practitioner
status: docs-checked
description: "Create, select, configure, rename and remove Pulumi stacks, and where per-stack config lives in Pulumi.<stack>.yaml."
sources:
  - https://www.pulumi.com/docs/iac/concepts/stacks/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_stack/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_stack_remove/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stacks

A stack is an isolated instance of a project (dev, staging, prod) with its own config and state.

```bash
pulumi stack init dev                 # create and select
pulumi stack init myorg/webapp/prod   # fully qualified: org/project/stack
pulumi stack ls                       # list stacks
pulumi stack select prod
pulumi stack output                   # all outputs; add --show-secrets to reveal
pulumi stack output vpcId --json
pulumi stack rename prod-eu           # or a fully qualified name
pulumi stack export --file state.json # checkpoint; restore with pulumi stack import --file state.json
pulumi stack rm dev --force           # --force leaves the stack's resources behind
```

Per-stack config is stored in `Pulumi.<stack>.yaml` next to `Pulumi.yaml`; secrets in it are encrypted values, and the Secrets page says it is safe and good practice to check these files into source control.

## Gotchas
- `pulumi stack rm` removes the stack and its configuration; use `pulumi destroy` to remove its resources first. `--force` removes the stack and leaves any resources it managed behind, still running in the cloud.
- Stack names can be `stack`, `org/stack` or `org/project/stack`. On a DIY backend the org part is always the constant `organization`.
- Renaming a stack changes the value `pulumi.getStack()` / `pulumi.get_stack()` returns, so resources named from it are replaced on the next `pulumi up`; review the preview first.
- Renaming into a different project also requires updating `name` in `Pulumi.yaml` and renaming the project-prefixed keys in `Pulumi.<stack>.yaml`; `aws:region`-style namespaced keys are unaffected.
- Choose the stack explicitly in CI (`--stack` or `pulumi stack select`) so a previously selected stack is not updated by accident.

## Verify
`pulumi stack ls` lists the stack; `pulumi stack --show-urns` lists its resources with their URNs.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Stacks page (name forms, DIY `organization`, select, rename effects and cross-project steps, outputs and `--show-secrets`), the `pulumi stack rm`, `export`, `import` and `output` CLI references, and the Secrets page (checking in the stack file). Removed: the claim that `*` marks the selected stack in `ls`, the "may not rename the config file on every backend" hedge, the claim that `rm` refuses without `--force`, and the "confirm flags" description hedge.
Method: documentation only; no commands were run.
