---
id: computing-software.devops-ci-cd.concourse-ci.instanced-pipelines
name: instanced-pipelines
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [instanced-pipelines, instance-vars, instance-group, set-pipeline, fly, templating]
level: practitioner
status: docs-checked
description: "Group related pipelines from one template as instance groups using --instance-var, address them with group/var:value syntax in fly, and avoid the quoting traps."
sources:
  - https://concourse-ci.org/docs/pipelines/grouping-pipelines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Instanced pipelines let several pipelines built from one template appear as a single instance group in the UI. Before v7.0.0 the version was encoded in the name (`release-1.0.x`). The recommended way is the same pipeline name with `--instance-var` instead of `--var`:

```shell
fly -t example set-pipeline --pipeline release --config template.yml --instance-var version=1.0.x
fly -t example set-pipeline --pipeline release --config template.yml --instance-var version=2.0.x
```

Pipelines sharing a name form the group automatically; there is no command to construct a group. The feature is not enabled by default on versions below v8; set `CONCOURSE_ENABLE_PIPELINE_INSTANCES` to `true` on the web node. `-i/--instance-var` behaves like `-y/--yaml-var` and can hold arbitrary YAML, while `-v/--var` only defines strings.

Because instance vars are part of the identifier, the `--pipeline` flag takes `group/var1:value1,var2:value2`:

```shell
fly -t example pause-pipeline --pipeline release/version:1.0.x
fly -t example trigger-job --job release/version:1.0.x/test
fly -t example check-resource --resource release/version:1.0.x/repo
```

For object values prefer dot notation, such as `--instance-var version.from=1.0.0 --instance-var version.to=2.0.0`. Without spaces, `version={from:1.0.0, to:2.0.0}` yields keys `"from:1.0.0"` and `"to:2.0.0"` with null values. Names or values containing `.`, `,`, `/`, `{`, `}` or whitespace must be double-quoted, which usually means quoting the whole flag in your shell.

## Checked

2026-11-04. Syntax, flag differences, enablement and warnings confirmed on the Grouping Pipelines page.

Method: documentation only; no commands were run.
