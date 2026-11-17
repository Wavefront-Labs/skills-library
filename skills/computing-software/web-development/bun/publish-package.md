---
id: computing-software.web-development.bun.publish-package
name: publish-package
category: computing-software
field: web-development
product: bun
tags: [bun-publish, dist-tag, tolerate-republish, publish-config]
level: practitioner
status: docs-checked
description: "Publish to npm with bun publish: dry runs, dist-tags for prereleases, access levels, 2FA, recursive workspace publishing, publishConfig and provenance limits."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/publish.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun publish --dry-run                 # full process, no publish
bun publish --access public --tag alpha
bun pm pack && bun publish ./package.tgz
bun publish -r                        # root + workspaces, dependencies first
bun publish --filter "@acme/*"
bun publish --tolerate-republish      # exit 0 if version exists (CI reruns)
bun publish --otp 123456              # or --auth-type web|legacy
```

`bun publish` strips catalog and workspace protocols, reads `bunfig.toml` and `.npmrc`; CI auth uses `NPM_CONFIG_TOKEN`.

Gotchas:
- A prerelease (`2.0.0-beta.1`) needs `--tag`, otherwise it becomes `latest`. The first version of a package always also gets `latest`. Tags cannot be versions or ranges.
- Passing a tarball skips lifecycle scripts (`prepublishOnly`, `prepack`, `prepare`, ...).
- Provenance is unsupported: `--provenance` and equivalents error; `--provenance=false` is fine.
- Unscoped packages are always public, so `--access restricted` errors.
- `bun --filter "@acme/*" publish` is different: it runs each package's `publish` script.
- Recursive publishing skips `"private"` packages and already-published versions; the first failure stops the run.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/publish.mdx: dry-run, access and tag rules, prerelease and first-version latest behaviour, tarball path skipping lifecycle scripts, provenance errors, recursive and filter publishing semantics and ordering, tolerate-republish, auth-type, otp, NPM_CONFIG_TOKEN.

Method: documentation only; no commands were run.
