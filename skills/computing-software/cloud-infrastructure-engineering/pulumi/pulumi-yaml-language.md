---
id: computing-software.cloud-infrastructure-engineering.pulumi.pulumi-yaml-language
name: pulumi-yaml-language
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-yaml-language, yaml-program, fn-invoke, yaml-resources]
level: practitioner
status: docs-checked
description: "Write Pulumi programs in YAML: config, variables, resources and options, outputs, ${} interpolation, fn::invoke, fn::join and built-in variables."
sources:
  - https://www.pulumi.com/docs/iac/languages-sdks/yaml/
  - https://www.pulumi.com/docs/iac/languages-sdks/yaml/yaml-language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pulumi YAML language

A YAML (or JSON) program has five top-level sections: `config`, `resources`, `variables`, `outputs` and `pulumi` (CLI configuration, e.g. `requiredVersion`).

```yaml
name: yaml-app
runtime: yaml
config:
  environment:
    type: string
  replicas:
    type: integer
    default: 3
variables:
  bucketPrefix: app-${environment}
  modifiedWeight:
    fn::invoke:
      function: std:sum
      arguments:
        input: [400, -255]
      return: result
resources:
  provider:
    type: pulumi:providers:aws
    defaultProvider: true
    options:
      version: 6.45.0
  my-bucket:
    type: aws:s3:BucketV2
    properties:
      bucketPrefix: ${bucketPrefix}
      tags:
        Stack: ${pulumi.stack}
    options:
      protect: true
      dependsOn:
        - ${provider}
outputs:
  bucketId: ${my-bucket.id}
  name: {fn::join: ["-", [app, "${environment}"]]}
```

- Config declarations need `type` or `default` (types `string`, `boolean`, `integer`, `array` with `items`, `object`); `secret: true` encrypts the value, set via `pulumi config set --secret`. The old top-level `configuration` key is deprecated.
- Any string is an interpolation: `${name}` refers to config, variables or resources (one shared namespace); property access like `${web.publicIp}` or `${root["foo"]}`. Escape a literal with `$${value}`. An object with an `fn::` key is a built-in function: `fn::invoke`, `fn::join`, `fn::split`, `fn::select`, `fn::toJSON`, `fn::toBase64`, `fn::fromBase64`, `fn::secret`, `fn::unsecret`, `fn::readFile`, `fn::sha1`, `fn::length`, `fn::stackReference`.
- Built-in variables: `${pulumi.cwd}`, `${pulumi.project}`, `${pulumi.stack}`.
- Resource `options` keys include `additionalSecretOutputs`, `aliases`, `customTimeouts`, `deleteBeforeReplace`, `dependsOn`, `ignoreChanges`, `import`, `parent`, `protect`, `provider`, `providers`, `version`, `pluginDownloadURL`, `replaceOnChanges`, `retainOnDelete`. `dependsOn`, `parent`, `provider`, `providers` need `${}` references.
- Stack references: a resource of type `pulumi:pulumi:StackReference` with `name: org/project/stack`, read with `${reference.outputs["outputName"]}`.

## Gotchas
- `fn::readFile` refuses paths that escape the project directory.
- Only one provider of a type can be the default provider; an explicit `provider` option takes precedence over it.
- Third-party providers may need `pluginDownloadURL` alongside `version`.

## Checked
2026-11-03. Every item above read on the Pulumi YAML reference page (sections, config schema, resource options, providers and versions, outputs and StackReference, interpolation, built-in functions and variables). Removed: the AMI lookup, `t3.micro`, `fn::` map for-each statements, `opts` remark, error-message text and the `pulumi preview` Verify paragraph; none were on the page.
Method: documentation only; no commands were run.
