---
id: computing-software.devops-ci-cd.backstage.scaffolder-custom-actions
name: scaffolder-custom-actions
category: computing-software
field: devops-ci-cd
product: backstage
tags: [custom-actions, create-template-action, backend-module, backstage]
level: advanced
status: docs-checked
description: "Write a custom scaffolder action with createTemplateAction and package it as a backend module."
sources:
  - https://backstage.io/docs/features/software-templates/writing-custom-actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Scaffold a module with the Backstage CLI:

```sh
yarn backstage-cli new
# choose: scaffolder-backend-module
```

Then define the action with `createTemplateAction`:

```ts
import { resolveSafeChildPath } from '@backstage/backend-plugin-api';
import { createTemplateAction } from '@backstage/plugin-scaffolder-node';
import fs from 'fs-extra';

export const createNewFileAction = () =>
  createTemplateAction({
    id: 'acme:file:create',
    description: 'Create an Acme file.',
    schema: {
      input: {
        contents: z => z.string({ description: 'The contents of the file' }),
        filename: z => z.string({ description: 'The filename to create' }),
      },
    },
    async handler(ctx) {
      await fs.outputFile(
        resolveSafeChildPath(ctx.workspacePath, ctx.input.filename),
        ctx.input.contents,
      );
    },
  });
```

- Namespace the `id` so it does not collide with future built-in actions; the docs suggest `provider:entity:verb` (for example `github:repo:create`) and camelCase over snake_case or kebab-case.
- `schema.input` describes inputs and `schema.output` the values set with `ctx.output`.
- Always build paths with `resolveSafeChildPath` against `ctx.workspacePath` so a template cannot write outside the workspace.
- `ctx.input` holds validated input; `ctx.output(key, value)` makes values available as `steps.<id>.output.<key>`.
- Examples (`TemplateExample`) are shown under `/create/actions`.
- `ctx.checkpoint` supports idempotent actions when tasks are recovered.

Register the action from a backend module using `scaffolderActionsExtensionPoint` and `scaffolder.addActions(...)`.

## Checked

2026-11-03. Confirmed against the Backstage Writing Custom Actions page: `yarn backstage-cli new` with `scaffolder-backend-module`, the example action, `createTemplateAction` fields, context members, naming conventions, extension point. Removed: the claim that JSON Schema is accepted in the Zod form (the page describes zod schema objects) and the `backend.add` registration step.

Method: documentation only; no commands were run.
