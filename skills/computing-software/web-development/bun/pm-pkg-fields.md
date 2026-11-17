---
id: computing-software.web-development.bun.pm-pkg-fields
name: pm-pkg-fields
category: computing-software
field: web-development
product: bun
tags: [bun-pm-pkg, package-json-edit, pkg-fix]
level: practitioner
status: docs-checked
description: "Read and edit package.json from scripts with bun pm pkg get, set, delete and fix, using dot paths, array indices and bracketed literal keys."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/pm.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun pm pkg get                        # omit fields to print everything
bun pm pkg get name version
bun pm pkg get scripts.build
bun pm pkg get contributors.name      # name of every element
bun pm pkg set scripts.test="bun test"
bun pm pkg set keywords[]=cli         # append to array
bun pm pkg set private=true --json    # parse value as JSON
bun pm pkg delete scripts.old --dry-run
bun pm pkg fix --dry-run              # auto-fix common issues
```

Path notation:
- Dot paths: `scripts.build`.
- Array indices: `contributors[0]`.
- Bracketed literal keys when the key contains dots or colons: `scripts[test:watch]`, `exports[./package.json]`.

Gotchas:
- With `--json`, a value that is not valid JSON is an error.
- `set`, `delete` and `fix` accept `--dry-run`, which prints the result without writing.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/pm.mdx: get, set, delete and fix examples, dot and bracket notation, literal bracketed names, --json error behaviour, --dry-run on set, delete and fix. Removed an unsourced Verify line and the claim about values being strings without --json.

Method: documentation only; no commands were run.
