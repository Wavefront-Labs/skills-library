---
id: computing-software.cybersecurity-defensive.threat-modelling.threagile-threat-model-as-code
name: threagile-threat-model-as-code
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threagile, threat-model-as-code, yaml-model, risk-rules, risk-tracking, agile-threat-modelling]
level: practitioner
status: docs-checked
description: "Model architecture as YAML with Threagile: technical and data assets, trust boundaries, communication links, risk rules, risk tracking and Docker commands."
sources: ["https://github.com/Threagile/threagile", "https://raw.githubusercontent.com/Threagile/threagile/master/README.md", "https://raw.githubusercontent.com/Threagile/threagile/master/docs/model.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threagile (threat model as code)

Threagile is an open-source (MIT) toolkit for agile threat modelling. You model an
architecture and its assets as a YAML file in the IDE. When the toolkit runs, all standard risk
rules, and any custom ones, are checked against the model.

## Run (README)
The easiest way is the Docker image. Examples from the README:
```
docker run --rm -it -v "$(pwd)":/app/work threagile/threagile --create-example-model --output /app/work
docker run --rm -it -v "$(pwd)":/app/work threagile/threagile --create-stub-model --output /app/work
docker run --rm -it -v "$(pwd)":/app/work threagile/threagile --verbose --model /app/work/threagile.yaml --output /app/work
```
- `--create-example-model` writes `threagile-example-model.yaml` and `--create-stub-model`
  writes a minimal `threagile-stub-model.yaml`.
- `--model` selects the input file (default `threagile.yaml`) and `--output` the output
  directory.
- `--list-risk-rules` prints the risk rules, `--skip-risk-rules` skips rules by ID, and
  `--list-types` prints the enum values usable in a model.
- Outputs enabled by default include the report PDF, risks Excel and JSON, stats JSON, tags
  Excel, technical assets JSON, the data-flow diagram and the data asset diagram.
- `--list-model-macros` and `--execute-model-macro <id>` run wizard-style macros that update the
  model (the README example is `add-build-pipeline`).
- `--server <port>` starts a REST API server instead of a command-line run.
- `--create-editing-support` creates syntax validation, autocompletion and live templates for
  an IDE.
- Custom risk rules can be written as YAML scripts without compiling Go code.

## Model (docs/model.md)
The YAML follows a JSON schema. Analysis starts from `technical_assets`; `data_assets` model
which data is stored, processed or sent.
- Technical assets link to each other with `communication_links`, which carry fields such as
  `data_assets_sent` and `data_assets_stored`.
- `data_assets_processed` and `data_assets_stored` say which data a technical asset handles.
- `trust_boundaries` and `shared_runtime` group technical assets.
- After running the analysis, some identified risks are real and some accepted; the
  `risk_tracking` field documents that decision for each risk.

## Gotchas
- The rules only know what the model says. Check the model against reality.
- Risk tracking entries that match no concrete risk are called orphaned; the
  `--ignore-orphaned-risk-tracking` flag just logs them.

## Verify
- [ ] The generated data-flow diagram matches the team's picture of the system.
- [ ] Each identified risk has a tracking decision.

## Checked
Confirmed 2026-11-09 against the Threagile README and docs/model.md (both read in full).
Removed as unconfirmed: the "about 40" risk rule count, the YAML example with enum values and field values, the risk status list, the ticket and checked_by fields, the CI failure rule, the output file names report.pdf and risks.xlsx, and the false-positive and noise gotchas. The OWASP threat-model project source was dropped because it was not read.
Method: docs-checked 2026-11-09 against Threagile README.md and docs/model.md on raw.githubusercontent.com
