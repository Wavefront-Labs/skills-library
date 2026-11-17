---
id: computing-software.cloud-infrastructure-engineering.pulumi.pulumi-watch-inner-loop
name: pulumi-watch-inner-loop
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-watch, inner-loop, watch-paths, dev-loop]
level: practitioner
status: draft
description: "Use pulumi watch to continuously deploy a dev stack on file changes, with path filters, and where it should not be used."
sources:
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_watch/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_up/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# pulumi watch

```bash
pulumi watch                          # re-run `up` on any change under the project dir
pulumi watch --path src --path ./handlers   # watch these paths (confirm repeatable flag)
pulumi watch --stack dev --refresh=false
```
Combine with a fast-feedback Lambda or container workflow:
```typescript
new aws.lambda.CallbackFunction("api", { callback: async () => ({ statusCode: 200 }) });
```
Edit the handler and `watch` redeploys within seconds without a prompt.

## Gotchas
- `watch` implicitly answers yes; run it only against a personal dev stack, never shared or production stacks.
- Edits that trigger replacement of databases will replace them; protect those resources (`protect: true`) so watch fails instead.
- Node `node_modules` and virtualenv directories can trigger loops; use `--path` to scope.
- Long-running updates queue: rapid saves are debounced, but a failure leaves a partial update.
- It does not run policy packs unless `--policy-pack` is passed.

## Verify
Save a change; the terminal prints a new preview/update cycle within seconds and `pulumi stack history` shows additional updates.
