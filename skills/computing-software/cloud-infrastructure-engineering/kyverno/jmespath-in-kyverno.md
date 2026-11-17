---
id: computing-software.cloud-infrastructure-engineering.kyverno.jmespath-in-kyverno
name: jmespath-in-kyverno
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [jmespath, kyverno-jp, custom-filters, quoting, escaping, regex-match, semver-compare]
level: practitioner
status: docs-checked
description: "Write JMESPath in Kyverno: quoting, defaults with ||, literal wildcards, testing with kyverno jp query, and the custom filter families and traps."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/jmespath/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrap expressions in `{{ }}`; if a field is only an expression, quote it (`appns: "{{request.namespace}}"`). JMESPath works on JSON, so convert YAML with `yq` first, or just use `kyverno jp query -i pod.yaml "<expr>"` which takes YAML. Flatten with `[]`: `spec.[initContainers, containers][].image`.

Quoting: keys with dots or dashes need escaped quotes (`spec.hard.\"limits.memory\"`, `images.containers.\"my-container\".tag`). Number literals use backticks, quantities and durations single quotes (`'6Mi'`, `'6h'`). Wrap the whole expression in double quotes and use single quotes for string inputs.

Defaults: `field || ''` supplies a value when missing, but `||` also fires on `null` and `false`; use `to_string()` on booleans. To match a literal `*` use `contains(element.host, '*')`.

Custom filter families: arithmetic (`add`, `subtract`, `multiply`, `divide`, `modulo`, `sum`, `round`); strings (`base64_decode`, `base64_encode`, `compare`, `equal_fold`, `split`, `replace`, `replace_all`, `to_lower`, `to_upper`, `trim`, `trim_prefix`, `truncate`, hashes); regex (`regex_match`, `regex_replace_all`, `pattern_match`, `semver_compare`); data (`items`, `object_from_lists`, `label_match`, `lookup`, `parse_json`, `parse_yaml`, `random`); time (`time_add`, `time_since`, `time_diff`, `time_now`, `time_parse`...); `image_normalize`, `is_external_url`, `to_boolean`, `x509_decode`.

Traps: bare numbers added to a duration are seconds (minutes unsupported since `m` means milli); `replace()` count `-1` replaces all; `image_normalize()` cannot be tested with the CLI; `round()` needs `to_number()` on strings; `regex_match()` in YAML needs doubled backslashes.

## Checked

2026-11-08. Read the Kyverno JMESPath page sections on installation tooling, formatting and quoting, flattening arrays, non-existence checks, wildcards, and the custom filter headings; checked the Add, Image_normalize, Regex_match, Replace, Round and Sum filter text. Filter names listed in the skill all appear as filter headings on the page. Individual filter sections not named here were not read in full. Removed the earlier note about a truncated page read.

Method: documentation only; no commands were run.
