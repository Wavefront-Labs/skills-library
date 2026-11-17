---
id: computing-software.devops-ci-cd.skaffold.diagnose-effective-config
name: diagnose-effective-config
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [diagnose, debugging, effective-config, templating]
level: practitioner
status: docs-checked
description: "Print the effective skaffold configuration with profiles applied, and optionally expanded templates, to debug unexpected behavior."
sources:
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When a build behaves strangely, check what Skaffold actually sees:

```bash
skaffold diagnose
skaffold diagnose --yaml-only --profile PROFILE
skaffold diagnose --enable-templating
```

- `skaffold diagnose` searches for configuration issues and prints the effective configuration.
- `--yaml-only` prints only the effective `skaffold.yaml` configuration; with `--profile` (`-p`) it shows it for that profile, without running anything.
- `--enable-templating` renders supported templated fields with the Go template engine.
- Other options: `-m/--module`, `-f/--filename`, `-o/--output` (write the result to a file), `--propagate-profiles` and `--profile-auto-activation`.

Typical problems this finds:

1. A profile did not activate, so a field still has the base value. Compare outputs with and without `-p`.
2. A profile patch does not point to the artifact you intended.
3. A templated build argument is empty because the environment variable is unset.
4. An imported config (via `requires`) adds artifacts you did not expect.

Pair with `skaffold build --dry-run`, which only computes the tag for each artifact, and `skaffold render` for the final manifests.

Make this the first debugging step in a support request: paste the effective configuration, not the original file, since profiles, imports and templating can change the result.

## Checked

2026-11-04. Read the CLI reference section for `skaffold diagnose` (examples and options) and the `build` section for `--dry-run`. Confirmed the three commands and all listed options. Changed "resolved configuration" wording to "effective configuration" as the page words it. The claim that `--yaml-only` includes merged `requires` imports is not stated on the page, so it was removed.
Method: documentation only; no commands were run.
