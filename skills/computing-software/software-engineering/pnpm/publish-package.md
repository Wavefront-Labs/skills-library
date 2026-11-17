---
id: computing-software.software-engineering.pnpm.publish-package
name: publish-package
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-publish, dist-tag, publish-access, git-checks, publish-branch, publish-config, recursive-publish]
level: practitioner
status: docs-checked
description: "Publish with pnpm publish: --tag, --access, git checks and publishBranch, publishConfig, recursive publish, README embedding, --force, --otp, --dry-run and lifecycle scripts."
sources:
  - https://pnpm.io/cli/publish
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
pnpm [-r] publish [<tarball|folder>] [--tag <tag>] [--access <public|restricted>]
```

- Default tag is `latest`; `pnpm publish --tag next` then `pnpm add foo@next`.
- Git checks: working tree clean, on the publish branch, up to date with remote. `--no-git-checks` skips. Publish branch defaults to `master` or `main`; override with `--publish-branch`, `publishBranch` in `pnpm-workspace.yaml`, or `PNPM_CONFIG_PUBLISH_BRANCH` (CLI beats env beats file). In CI, a detached HEAD skips the branch check.
- `-r` publishes every package whose version is not yet in the registry. `--force` publishes even if the version exists.
- `publishConfig` in `package.json` overrides fields before publish; `publishConfig.directory` publishes a subdirectory.
- README: included automatically from `README.md`, other Markdown READMEs or `README` if the manifest has no `readme`; `--embed-readme` (setting `embedReadme`) embeds it in the manifest.
- Workspace LICENSE at the root is packed unless the package has its own.
- `--otp` or `PNPM_CONFIG_OTP`; otherwise pnpm prompts, and shows a QR code for web auth.
- `--dry-run`, `--json`, `--ignore-scripts`.
- Lifecycle: `prepublishOnly`, `prepublish`, `prepack`, `prepare`, `postpack`, `publish`, `postpublish`.

## Checked

2026-11-04. Confirmed the usage line, --tag, git checks and publish branch precedence, recursive publish, --force, README and LICENSE handling, --otp, --dry-run, --json, --ignore-scripts and the lifecycle script list against pnpm.io/cli/publish. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
