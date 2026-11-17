---
id: computing-software.cloud-infrastructure-engineering.kubernetes.backstage-scaffolder-golden-path-templates
name: backstage-scaffolder-golden-path-templates
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [backstage, scaffolder, golden-path, paved-road, software-templates, self-service, template-entity, scaffolder-actions, cookiecutter, nunjucks, idp, developer-portal, bootstrap]
level: advanced
status: docs-checked
description: "Authoring Backstage Software Templates (Template entities) as golden paths that scaffold a new service with CI, RBAC and catalog registration pre-wired."
sources: ["https://backstage.io/docs/features/software-templates/writing-templates", "https://backstage.io/docs/features/software-templates/builtin-actions", "https://backstage.io/docs/features/software-templates/writing-custom-actions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backstage Scaffolder — golden-path templates

**Goal:** make "create a new service" a 5-minute self-service form that produces
a repo already wired to the platform's defaults (CI, Dockerfile, k8s manifests,
RBAC, catalog registration) — the actual mechanism behind "golden path" or
"paved road." Owning the catalog that templates publish into is
`computing-software.cloud-infrastructure-engineering.kubernetes.backstage-software-catalog-and-techdocs`.

## 1. Template entity anatomy
A `Template` entity (`kind: Template`, `apiVersion: scaffolder.backstage.io/v1beta3`)
has `spec.parameters` (a JSON Schema form, rendered by the frontend) and
`spec.steps` (an ordered list of **actions**). Parameters support `ui:field`
custom widgets — `OwnerPicker` to let the user choose an owner (a searchable list of catalog `Group`/`User` entities) instead of free text, `RepoUrlPicker` to pick
org/repo/visibility. Steps run server-side in the scaffolder backend, each
invoking a registered action by `action:` name with `input:` templated via
Nunjucks (`${{ parameters.name }}`).

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: nodejs-service
spec:
  parameters:
    - properties:
        name: {type: string}
        owner: {type: string, ui:field: OwnerPicker}
  steps:
    - id: fetch
      action: fetch:template
      input: {url: ./skeleton, values: {name: '${{ parameters.name }}'}}
    - id: publish
      action: publish:github
      input: {repoUrl: '${{ parameters.repoUrl }}', defaultBranch: main}
    - id: register
      action: catalog:register
      input: {catalogInfoPath: /catalog-info.yaml}
```

## 2. The three built-ins that actually matter
`fetch:template` copies a skeleton dir and renders its templated values (in skeleton files, form values
are referenced as `${{ values.name }}`, while `${{ parameters.name }}` works only in the template file). `publish:github`
(or gitlab/bitbucket) creates the real repo and pushes the rendered content.
`catalog:register` (input `catalogInfoPath`, as in the documented example) registers the new repo's
`catalog-info.yaml` so the user lands on the entity page after creation.

## 3. Writing a good skeleton, not a toy one
The skeleton under `./skeleton` IS the golden path — what's in it is the
opinion. A real golden path skeleton includes: a working CI pipeline file
(not a stub — it should pass on first push), a Dockerfile matching the org's
base image policy, k8s manifests (or a Helm chart / Crossplane claim) with
resource requests/limits already set to sane defaults, a `catalog-info.yaml`
pre-filled from parameters, and pre-wired RBAC/service-account scoping so the
new service starts inside the guardrails rather than needing a follow-up
ticket. Ship **one or two** templates per archetype (`nodejs-service`,
`python-worker`) rather than one mega-template with 40 conditional parameters —
divergent archetypes with shared conditionals rot fast and nobody can read the
`if` logic a year later.

## 4. Custom actions — when the built-ins aren't enough
Register a custom `TemplateAction` in the scaffolder backend (`createTemplateAction`)
when the paved road needs something built-ins can't do: provisioning a
Crossplane claim and waiting for `status.ready`, creating a namespace with
quota, calling an internal secrets-bootstrap API. Keep custom actions
idempotent (`ctx.checkpoint`) and give them an `examples` array passed to `createTemplateAction`.

## 5. Gotchas
- Templates are catalog entities of kind `Template`; test every template by actually running it, not just
  by linting the YAML.
- `publish:github` needs a GitHub integration token or app that is allowed to create repositories in the
  target org.
- The `${{ }}` expressions in the template are a focused subset of Nunjucks syntax and preserve the type of
  the parameter; check the doc before using other Nunjucks features.

## Verify
- Running the template end-to-end from the Backstage UI produces a repo that
  builds, has a green first CI run, and appears in the catalog as a `Component`
  immediately (via `catalog:register`), without a manual registration step.
- A second archetype template can be added by copying the pattern, not by
  adding conditionals to the first — if it can't, the first template was
  already overloaded.

## Checked

Checked against `backstage/backstage` master docs (last commit 2026-10-25): `features/software-templates/writing-templates.md`, `writing-custom-actions.md`.
Confirmed: `apiVersion: scaffolder.backstage.io/v1beta3`, `OwnerPicker` and `RepoUrlPicker` fields, `fetch:template`, `publish:github`, `catalog:register` with `catalogInfoPath`, `${{ }}` as a Nunjucks subset, `examples` and `ctx.checkpoint`.
Removed as unconfirmed: filename renaming, the silent-blank-for-undefined claim, the exact GitHub error text.

Method: documentation only; no commands were run.
