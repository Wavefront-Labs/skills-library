---
id: computing-software.cloud-infrastructure-engineering.aws.aws-cli-generate-skeleton-and-cli-input-json
name: aws-cli-generate-skeleton-and-cli-input-json
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-cli, cli-skeleton, cli-input-json, cli-input-yaml, generate-cli-skeleton, parameter-files]
level: practitioner
status: docs-checked
description: "Drive complex AWS CLI calls from parameter files: generate-cli-skeleton for input and output shapes, cli-input-json and cli-input-yaml, overrides and validation errors."
sources: ["https://github.com/aws/aws-cli/blob/v2/awscli/customizations/generatecliskeleton.py", "https://github.com/aws/aws-cli/blob/v2/awscli/customizations/cliinput.py", "https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-skeletons.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS CLI skeletons and cli-input-json/yaml

**Goal:** stop hand-writing 40-flag commands; keep the request in a reviewed file.

## Generate an input skeleton
```bash
aws ec2 run-instances --generate-cli-skeleton input > run.json      # JSON
aws ecs register-task-definition --generate-cli-skeleton yaml-input > td.yaml
aws ec2 describe-instances --generate-cli-skeleton output           # validates inputs, prints sample output JSON
```
`--generate-cli-skeleton` takes `input` (the default when no value is given), `yaml-input` or `output`, prints without calling the API, and its output is not stable between CLI versions.

## Edit, then run
- Delete every key you do not set: the skeleton's placeholder values are not defaults and would otherwise be sent as given.
```bash
aws ec2 run-instances --cli-input-json file://run.json
aws ecs register-task-definition --cli-input-yaml file://td.yaml
aws ec2 run-instances --cli-input-json file://run.json --instance-type m7g.large --dry-run
```
- Parameters in the file are overwritten by arguments given on the command line: one base file, small per-run overrides.
- `--dry-run` (EC2) checks permissions and parameters without acting.

## Round-trip existing resources
```bash
aws ecs describe-task-definition --task-definition web:12 --query taskDefinition > td.json
# edit td.json: remove fields that register-task-definition does not accept (generate the
# input skeleton to see which keys it takes), then register it:
aws ecs register-task-definition --cli-input-json file://td.json
```
The input skeleton for the target command shows which keys it accepts; delete the others from a described resource.

## file:// vs fileb://
- `file://` reads text (JSON/YAML/policy documents) into a parameter.
- `fileb://` reads raw bytes (zip files, binary payloads).

## Gotchas
- `--cli-input-yaml` and `yaml-input` are CLI v2 features.
- The skeleton comes from the installed CLI's API model; newer parameters need a CLI upgrade.
- Keys in the skeleton are the API parameter names, not the CLI flag names.
- Secrets in input files end up in git; reference Secrets Manager/SSM where the API allows it.

## Verify
- [ ] `--dry-run` or a `validate-*` call passes with the input file.
- [ ] The input file is in version control and diffs are reviewed.

## Checked
Date: 2026-10-24. Sources: aws-cli v2 branch source and help text (generatecliskeleton.py, cliinput.py).
Confirmed: generate-cli-skeleton values input (default), yaml-input and output, no API call is made, skeleton is not stable between CLI versions, --cli-input-json and --cli-input-yaml exist, command-line arguments overwrite file parameters, file:// and fileb:// prefixes.
Removed as unconfirmed: jq read-only-field list for task definitions, Windows absolute-path note, specific error names for leftover placeholder values.
Method: documentation only; no commands were run.
