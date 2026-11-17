---
id: computing-software.devops-ci-cd.renovate.custom-datasources
name: custom-datasources
category: computing-software
field: devops-ci-cd
product: renovate
tags: [custom-datasources, datasource, registry-url-template, renovate]
level: advanced
status: docs-checked
description: "Fetch release lists from APIs or static sites with customDatasources and connect them to custom managers."
sources:
  - https://docs.renovatebot.com/configuration-options/
  - https://docs.renovatebot.com/modules/datasource/custom/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When Renovate has no datasource for a release source, define one under `customDatasources`. A custom manager (or a rule overriding a default datasource) then refers to it by name.

```json5
{
  customDatasources: {
    internalTools: {
      defaultRegistryUrlTemplate: "https://tools.example.com/{{packageName}}/releases.json",
      format: "json",
      transformTemplates: ['{"releases": versions}'],
    },
  },
  customManagers: [
    {
      customType: "regex",
      managerFilePatterns: ["/tools.txt$/"],
      matchStrings: ["(?<depName>\\S+)=(?<currentValue>\\S+)"],
      datasourceTemplate: "custom.internalTools",
    },
  ],
}
```

Notes from the docs:

- `defaultRegistryUrlTemplate` builds the `registryUrl`. It is unnecessary if the datasource has default registries, or if your match already captures a `registryUrl` group.
- The template is dynamic, so you can include the `packageName`.
- Custom datasources can also overwrite a default datasource for a package.
- The datasource is referenced with the `custom.` prefix.

Options per datasource:

- `defaultRegistryUrlTemplate` : the URL used when no `registryUrl` is provided.
- `format` : the API format, `json` by default, or `html`, `plain`, `toml` or `yaml`.
- `transformTemplates` : JSONata rules evaluated one after another to reshape the API output. Test them with the JSONata Exerciser.

Template variables available are `packageName` and `currentValue`. After all transformations the result must be an object with a `releases` array whose entries each have a `version`; `sourceUrl` and `changelogUrl` are optional extras.

The custom datasource has no default versioning, so set `versioning` explicitly (for example `versioningTemplate` in a custom manager). It does not support release timestamps. The `customDatasources` option is flagged experimental. Other optional release fields include `isDeprecated`, `releaseTimestamp`, `changelogContent`, `sourceUrl`, `digest` and `isStable`.

## Checked

2026-11-09: read https://docs.renovatebot.com/modules/datasource/custom/ (table of values, options, template variables, output formats) and the customDatasources sections of https://docs.renovatebot.com/configuration-options/. Claims matched; added the no-default-versioning, experimental and extra release field details.

Method: documentation only; no commands were run.
