---
id: computing-software.cloud-infrastructure-engineering.kubernetes.backstage-plugin-and-scaffolder-action-development
name: backstage-plugin-and-scaffolder-action-development
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [backstage, plugin-development, scaffolder-action, createtemplateaction, backend-plugin, frontend-plugin, idp, internal-developer-portal, new-backend-system, entity-page, typescript]
level: sme
status: docs-checked
description: "Writing a custom Backstage backend plugin and scaffolder action (createTemplateAction) to expose a platform API as a self-service capability."
sources: ["https://backstage.io/docs/plugins/new-backend-system", "https://backstage.io/docs/plugins/backend-plugin", "https://backstage.io/docs/features/software-templates/writing-custom-actions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backstage custom plugin and scaffolder action development

**Goal:** when the built-in catalog/scaffolder/kubernetes plugins
(`computing-software.cloud-infrastructure-engineering.kubernetes.backstage-software-catalog-and-techdocs`,
`...backstage-scaffolder-golden-path-templates`) don't cover a platform
capability, write the backend plugin or custom action that does — the actual
code-level work of extending the portal, not just configuring it.

## 1. New backend system — don't write the old way
In the new backend system a backend plugin is a `createBackendPlugin` call with a `pluginId` and a `register`
method that calls `env.registerInit` with typed `deps` resolved from the service container
(`coreServices.logger`, `coreServices.httpRouter`, etc.). A `createRouter` function that builds an express
router is still the documented way to build the routes, which you then mount with `httpRouter.use(...)`.
Write new plugins against the new system; migration of old plugins is a separate exercise.

```ts
export const examplePlugin = createBackendPlugin({
  pluginId: 'example',
  register(env) {
    env.registerInit({
      deps: { logger: coreServices.logger, httpRouter: coreServices.httpRouter },
      async init({ logger, httpRouter }) {
        httpRouter.use(await createRouter({ logger }));
      },
    });
  },
});
```

## 2. Custom scaffolder action — the highest-leverage plugin type
Most platform teams never write a frontend plugin; the action that pays off is
a **custom scaffolder action**, because it's the thing golden-path templates
call to touch real infrastructure. Register with `createTemplateAction<Input>`,
giving it an `id`, a `schema.input` (an object of `z => z.string()` style zod builders; `schema.output` likewise, for values set with
`ctx.output`), optional `examples`, and a `handler(ctx)` that gets `ctx.input`, `ctx.workspacePath` (the
working directory of the template run, so files written there are available to later steps), `ctx.logger`,
`ctx.output`, `ctx.checkpoint` (for idempotent actions) and `createTemporaryDirectory`.

```ts
export const createNamespaceClaimAction = () =>
  createTemplateAction({
    id: 'platform:namespace-claim',
    schema: { input: { name: z => z.string(), owner: z => z.string() } },
    async handler(ctx) {
      ctx.logger.info(`provisioning namespace ${ctx.input.name}`);
      await crossplaneClient.applyClaim(ctx.input.name, ctx.input.owner);
      await waitForReady(ctx.input.name, { timeoutMs: 120_000 });
      ctx.output('namespaceReady', true);
    },
  });
```
Register it from a backend module through `scaffolderActionsExtensionPoint` with
`scaffolder.addActions(...)`. `crossplaneClient` and `waitForReady` above stand for your own helpers.
Make `handler` throw when provisioning fails so the step is reported as failed.

## 3. Entity page cards — the common frontend ask
The one frontend extension most platform teams eventually want is a custom
card on the entity page (next to the Kubernetes/CI cards) showing something
platform-specific — a Crossplane claim's status, a cost estimate, an SLO
burn rate. Build it as a frontend plugin component that reads the current entity with `useEntity()` and
add it to the entity page of your app. Keep it read-only first; a card that lets users mutate state needs
its own RBAC story.

## 4. Testing without a full deploy
`@backstage/backend-test-utils` provides `startTestBackend`, which returns the HTTP server for use with
`supertest` to test a plugin. For scaffolder actions, test the `handler` directly with a hand-built `ctx`
before reaching for the full test backend.

## Verify
- A custom scaffolder action's handler throws (not silently fails) when the
  downstream provisioning call errors, and the scaffolder UI shows the step
  red with the real error message, not a generic failure.
- The action's `schema.input` rejects a malformed template invocation at
  parameter-entry time in the UI, not deep inside `handler`.
- A new entity-page card renders only on entities carrying the annotation it
  depends on, and degrades (hides, not crashes) on entities without it.

## Checked

Checked against `backstage/backstage` master docs (last commit 2026-10-25): `plugins/new-backend-system.md`, `plugins/backend-plugin.md`, `features/software-templates/writing-custom-actions.md`.
Confirmed: `createBackendPlugin` with `pluginId`/`register`/`registerInit`, `coreServices.httpRouter`, `createRouter` still used to build routes, `createTemplateAction` from `@backstage/plugin-scaffolder-node`, `schema.input`/`schema.output` as zod schemas, `ctx.workspacePath`, `ctx.logger`, `ctx.output`, `ctx.checkpoint`, `scaffolderActionsExtensionPoint` with `addActions`, `startTestBackend` with supertest.
Corrected: removed `ctx.logStream` and a misspelled `createTemputFile`, the JSON Schema claim for input, the v1.16 default claim and the lifecycle-hook claim.

Method: documentation only; no commands were run.
