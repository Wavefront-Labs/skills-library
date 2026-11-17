---
id: computing-software.devops-ci-cd.skaffold.test-structure-and-custom
name: test-structure-and-custom
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [test, structure-tests, container-structure-test, custom]
level: practitioner
status: docs-checked
description: "Run container-structure-test and custom command tests after each build, and know what blocks a deploy."
sources:
  - "https://skaffold.dev/docs/testers/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Tests are configured under `test`, one entry per image.

```yaml
test:
- image: my-registry/app
  structureTests:
  - ./test/structure/*
  custom:
  - command: ./scripts/check.sh
    timeoutSeconds: 60
    dependencies:
      paths: ["scripts/**"]
```

Structure tests:

- `structureTests` takes globs of test configs run by `container-structure-test`, which must be installed.
- They run on each rebuild, and a failure blocks the deploy.

Custom tests:

- `command` runs on the machine where Skaffold runs, and the pipeline blocks until it completes or fails.
- `timeoutSeconds` bounds it; with no timeout Skaffold waits indefinitely.
- `dependencies` has `command`, `paths` and `ignore` for the files watched to re-trigger the test. `ignore` only works together with `paths`. A dependencies `command` must print a JSON array.
- With no dependencies set, only the script file (if the command is a script) is watched.
- The image is passed to the command in `$IMAGE`.
- Skaffold blocks deployment at the first failing test. In the dev loop a failure stops that iteration but not the session.
- Test dependencies cannot trigger rebuilds, and adding a pattern does not enable file sync.
- `structureTestsArgs` passes extra flags to `container-structure-test`.

Skip tests with `--skip-tests`, or run only tests with `skaffold test` (for example `skaffold test --profile quickcheck`, where a profile overrides the structure test patterns).

Long-running tests belong in a dedicated profile if running them on every rebuild is prohibitive. The post-deployment `verify` stage is a separate feature (see verify-post-deploy).

## Checked

2026-11-09: confirmed against the Skaffold docs pages "Container Structure Test" and "Custom Test" (source files docs-v2/content/en/docs/testers/structure.md and custom.md). Removed the unconfirmed claim that a non-zero exit code is the failure signal and the advice to move slower checks to the verify stage; replaced with the documented dedicated-profile advice.

Method: docs-checked 2026-11-09 against skaffold.dev testers structure and custom pages (read in full as source markdown).
