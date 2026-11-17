---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-datafrom-rewrite
name: external-secrets-operator-datafrom-rewrite
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [rewrite, datafrom, regexp, key-collisions]
level: advanced
status: docs-checked
description: "Rewrite keys from dataFrom extract or find with Regexp, Transform and Merge operations to remove prefixes, fix invalid characters or resolve collisions."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/datafrom-rewrite.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`dataFrom.rewrite` is a stackable list of operations applied before `conversionStrategy`; each takes the previous output, and keys that match nothing are kept unchanged.

- `regexp`: `source` regular expression and `target` replacement. An invalid source puts the ExternalSecret in error. It uses Go RE2, so there are no lookaheads, lookbehinds, negation, conditionals or possessive repetition.
- `transform`: a Go `template` where `.value` is the key, with helper functions available, for example to upper-case and replace `-` with `_`, then prefix `ENV_`.
- `merge`: merge JSON-valued secrets by `strategy`. `Extract` hoists all inner keys to the top level; `JSON` places them under the required `into` key. `conflictPolicy` is `Ignore` or `Error`. Keys are processed alphabetically; `priority` lists keys to process last, and `priorityPolicy: IgnoreNotFound` tolerates missing ones (default `Strict` errors). Non-JSON values error.

Typical uses: strip a common path (`path/to/my/secrets/username` becomes `username`), prefix `dev_` and `prod_` to avoid duplicate `password` keys, or turn `foo/bar` and `foo$baz` into `foo_bar` and `foo_baz`.

## Checked

2026-11-03. Claims were read against guides/datafrom-rewrite.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
