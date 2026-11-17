---
id: computing-software.cybersecurity-defensive.suricata.rule-files-and-classification
name: rule-files-and-classification
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [rule-files, default-rule-path, classification-file, threshold-file]
level: practitioner
status: docs-checked
description: "Point Suricata at rules: default-rule-path, rule-files, classification-file, threshold-file, and what happens with missing files."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html", "https://docs.suricata.io/en/latest/command-line-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rule files and ancillary configs

- `default-rule-path` plus `rule-files` list what is loaded. With suricata-update the pair is the rules directory and `suricata.rules`. Absolute paths are allowed.
- A missing rule file logs a warning, unless `--init-errors-fatal` is set.
- `classification-file`: short name, description and priority 1 (highest) to 4 (lowest).
- `threshold-file`: path of the threshold configuration (default `/etc/suricata/threshold.config`).
- `-s` adds rule files from the command line (globbing allowed); `-S` loads only those and ignores YAML rules.

## Checked

Method: docs-checked 2026-11-09 against the Rule Files, Threshold-file and Classifications sections of https://docs.suricata.io/en/latest/configuration/suricata-yaml.html and https://docs.suricata.io/en/latest/command-line-options.html; dropped the live-reload re-read claim, which these pages do not state.
