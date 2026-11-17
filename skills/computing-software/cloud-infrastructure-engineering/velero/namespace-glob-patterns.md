---
id: computing-software.cloud-infrastructure-engineering.velero.namespace-glob-patterns
name: namespace-glob-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [namespace-glob, include-namespaces, exclude-namespaces, glob-patterns, namespace-filter]
level: practitioner
status: docs-checked
description: "Use glob patterns with --include-namespaces and --exclude-namespaces, and know which characters are rejected by validation."
sources:
  - https://velero.io/docs/main/namespace-glob-patterns/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--include-namespaces` and `--exclude-namespaces` accept glob patterns on both backup and restore.

Supported characters:
- `*` any sequence of characters: `"app-*"` matches app-prod, app-staging, app-dev.
- `?` exactly one character: `"ns?"` matches ns1, nsa, but not ns10.
- `[abc]` one character from a set: `"ns[123]"` matches ns1, ns2, ns3.
- `[a-z]` one character from a range: `"ns[a-c]"` matches nsa, nsb, nsc.

Not supported, and they cause validation errors: `**`, `|`, `()`, `!`, `{}` and `,` inside a pattern (the comma only separates list entries). Empty brackets `[]` and unclosed brackets are also invalid.

Special case: `*` alone means all namespaces and is not expanded.

If the patterns resolve to no namespaces, the backup succeeds with a warning, so check the warnings rather than assuming data was captured.

```bash
velero backup create prod-backup \
  --include-namespaces "*-prod" \
  --exclude-namespaces "test-*"

velero restore create my-restore --from-backup my-backup \
  --include-namespaces "frontend-*,backend-*"
```

Quote patterns so the shell does not expand them against local files.

## Checked

2026-11-08. Read in full: the Namespace Glob Patterns page. Every remaining claim was confirmed there. Removed or reworded: nothing.

Method: documentation only; no commands were run.
