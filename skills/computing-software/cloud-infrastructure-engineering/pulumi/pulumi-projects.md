---
id: computing-software.cloud-infrastructure-engineering.pulumi.pulumi-projects
name: pulumi-projects
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-yaml, pulumi-project, pulumi-runtime, pulumi-main]
level: practitioner
status: docs-checked
description: "Define a Pulumi project with Pulumi.yaml: name, runtime, main entry point, config schema and backend options, with the field rules from the project file reference."
sources:
  - https://www.pulumi.com/docs/iac/concepts/projects/
  - https://www.pulumi.com/docs/iac/concepts/projects/project-file/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Projects and Pulumi.yaml

A project is a directory with a `Pulumi.yaml` at its root; one project can have many stacks.

```yaml
name: webapp            # required; alphanumerics, hyphens, underscores, periods
runtime:                # required: nodejs, python, go, dotnet, java, yaml, hcl or bun
  name: nodejs
  options:
    typescript: true    # runtime-specific; applies to the nodejs runtime
description: Static site and CDN
main: ./infra           # optional: path to the program, relative to Pulumi.yaml
config:
  aws:region: {default: us-east-1}
  instanceCount: {type: integer, default: 2}
backend:
  url: s3://my-state-bucket   # optional explicit backend URL
```

Create one with `pulumi new aws-typescript` or by writing the file and running `pulumi stack init dev`.

## Gotchas
- `name` and `runtime` are required; the default for `main` is the current working directory.
- A config key declares `type` (`string`, `boolean`, `integer`, `array` or `object`) and/or `default`; one of the two is required, and the type is inferred from `default` when omitted.
- Entry points follow language conventions: for TypeScript a `package.json` pointing at e.g. `index.ts`, for Python a `__main__.py` or `setup.py`.
- Project-namespaced config keys are stored with the project name as prefix in `Pulumi.<stack>.yaml`, so changing the project name needs those keys renamed (see pulumi-stacks).

## Verify
`pulumi about` prints information about the Pulumi environment; `pulumi preview` should resolve the program from the project directory.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Projects page (entry point conventions) and the project file reference (`name`, `runtime` values, `main`, `backend.url`, config `type`/`default` rules, `typescript` runtime option) and the `pulumi about` reference. Removed: the "confirm" hedges, the claim that undeclared keys are accepted but not validated, and the "no Pulumi.yaml found" error text.
Method: documentation only; no commands were run.
