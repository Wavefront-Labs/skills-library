---
id: computing-software.cloud-infrastructure-engineering.pulumi.templates-and-pulumi-new
name: templates-and-pulumi-new
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-new, templates, pulumi-template, new-project]
level: practitioner
status: docs-checked
description: "Start Pulumi projects with pulumi new: flags, template sources (git URLs, org templates), and authoring templates with Pulumi.yaml template fields."
sources:
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_new/
  - https://www.pulumi.com/docs/iac/guides/building-extending/creating-templates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Templates and pulumi new

```bash
pulumi new aws-typescript --name web --stack dev --yes
pulumi new https://github.com/org/repo                      # git template
pulumi new https://github.com/org/repo/tree/main/subdir    # branch or tag plus subdirectory
pulumi new aws-python -c aws:region=us-west-2 --generate-only
pulumi new --list-templates                                 # locally installed templates
```

Flags: `-c/--config`, `--config-path`, `-d/--description`, `--dir`, `-f/--force` (generate even if it changes existing files), `-g/--generate-only` (no stack, config or dependency install), `-l/--list-templates`, `-n/--name`, `-o/--offline`, `--runtime-options`, `--secrets-provider` (default, passphrase, awskms, azurekeyvault, gcpkms, hashivault), `-s/--stack`, `-y/--yes`.

Templates can come from git over https or ssh (private repos can use token URLs). Organization templates are distributed through the Private Registry.

Authoring: put template metadata under `template:` in the template's `Pulumi.yaml`:
```yaml
template:
  displayName: Web app
  description: Static site on S3
  config:
    aws:region: {description: Region, default: us-east-1}
    dbPassword: {description: DB password, secret: true}
  metadata: {}
```

## Gotchas
- `--generate-only` skips stack creation, config and dependency installation; run `pulumi stack init` and install dependencies yourself.
- Use `--force` only when overwriting existing files is intended.

## Verify
The directory contains `Pulumi.yaml` (and `Pulumi.<stack>.yaml` unless `--generate-only`).

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the `pulumi new` reference (all flags above) and the Creating templates guide (`template` fields, git URL forms, token URLs). Removed: a Console templates path, the claim about `--yes` and required values, the `ls` verification and an unconfirmed default-description gotcha; the listed project-templates source page was not read and is dropped.
Method: documentation only; no commands were run.
