---
id: computing-software.cybersecurity-defensive.splunk.sigma-rule-validation-and-linting
name: sigma-rule-validation-and-linting
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [sigma, sigma-check, sigma-cli, pysigma, detection-as-code, linting, ci-cd, detection-engineering]
level: practitioner
status: gated
description: "Validate and lint Sigma rules in CI with sigma-cli check, pySigma validators, schema checks and backend conversion tests before merging detections."
sources: ["https://github.com/SigmaHQ/sigma-cli", "https://sigmahq-pysigma.readthedocs.io/en/latest/Rule_Validation.html", "https://github.com/SigmaHQ/sigma-specification"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sigma rule validation and linting

## sigma-cli check
```
pip install sigma-cli
sigma plugin install splunk           # backends you convert to
sigma check rules/                    # parses + runs all pySigma validators
sigma check --fail-on-error --fail-on-issues rules/    # -e / -i; fail-on-error is already the default, issues do not fail by default
sigma check -x identifier_uniqueness -x all_of_them_condition rules/   # -x/--exclude drops validators; `-e` is NOT exclude
```
Validators (`sigma list validators`, sigma-cli 3.1.0) include: `identifier_existence` and `identifier_uniqueness`, `duplicate_title`,
`duplicate_filename`, `filename_length`, `attacktag` (valid ATT&CK tags), `tag_format`, `duplicate_tag`, `tlptag`,
`all_of_them_condition`, `dangling_condition`, `dangling_detection`, `invalid_modifier_combinations`,
`wildcards_instead_of_modifiers`, `double_wildcard`, `escaped_wildcard`, `control_character`, `number_as_string`,
`fieldname_logsource`, `specific_instead_of_generic_logsource`. There is NO validator for missing description/author or date format,
and an unknown modifier is a parse error (`SigmaModifierError`), not a validator issue. Checked: a rule with a bad tag and
`CommandLine: '*foo*'` gave `InvalidATTACKTagIssue` and `WildcardsInsteadOfContainsModifierIssue`; `-i` made the exit status 1.

Configure exclusions per rule in a validator config file (`-c` / `--validation-config`; checked, the exclusion removed that rule's wildcard issue):
```yaml
validators: [all, -tlptag]
exclusions:
  5013332f-8a70-4e04-bcc1-06a98a2cca2e: [wildcards_instead_of_modifiers]
```

## Conversion tests
Every rule must convert for each target: `sigma convert -t splunk -p splunk_windows rules/ > /dev/null`.
Conversion errors (unsupported modifiers, missing field mappings) fail the build.

## Additional checks
- JSON schema validation against the Sigma specification schema (`pip install check-jsonschema`, `check-jsonschema --schemafile sigma-detection-rule-schema.json rule.yml`; the schema is in `json-schema/` of SigmaHQ/sigma-specification; the rule above passed).
- Style: filename = title slug, `level` and `status` from allowed values, `falsepositives` filled.
- Test data: each rule ships a positive sample event; run the converted query against sample data
  in a test index or use evtx samples with chainsaw (WithSecureOpenSource/chainsaw) or zircolite (wagga40/Zircolite), neither of which was run here (gated: unconfirmed, tools not run in this review).

## CI wiring (GitHub Actions)
```yaml
- run: pip install sigma-cli && sigma plugin install splunk
- run: sigma check --fail-on-error --fail-on-issues rules/
- run: sigma convert -t splunk -p splunk_windows rules/ -o out.spl
```

## Gotchas
- Pin pySigma and plugin versions; validator sets change between releases.
- `sigma check` validates syntax, not logic; a rule that never matches passes.

## Verify
Introduce a duplicate ID and a malformed ATT&CK tag in a branch; CI fails with both issues.
