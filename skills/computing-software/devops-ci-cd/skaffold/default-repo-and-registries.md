---
id: computing-software.devops-ci-cd.skaffold.default-repo-and-registries
name: default-repo-and-registries
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [default-repo, registry, rewrite, insecure-registries]
level: practitioner
status: docs-checked
description: "Push all images to one registry prefix with default-repo, understand name rewriting, and allow insecure registries."
sources:
  - "https://skaffold.dev/docs/environment/image-registries/"
  - "https://skaffold.dev/docs/design/global-config/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Use a `default-repo` so developers do not have to edit image names. Set it one of three ways:

```bash
skaffold dev --default-repo <myrepo>
SKAFFOLD_DEFAULT_REPO=<myrepo> skaffold dev
skaffold config set default-repo <myrepo>
```

With no `default-repo`, there is no rewriting and Skaffold tries to push the image names as written in the YAML.

Rewriting is designed to be conflict-free: the full original image name is placed under the repo. The strategy depends on the default-repo:

- Domain does not contain `gcr.io` or `-docker.pkg.dev`: escape, concatenate and truncate to 256 characters. For example `gcr.io/k8s-skaffold/skaffold-example1` under an ECR registry becomes `<registry>/gcr_io_k8s-skaffold_skaffold-example1`.
- Contains `gcr.io` or `-docker.pkg.dev` (these allow arbitrarily deep paths): concatenate unless the prefix matches. Default-repo `gcr.io/myproject/myimage` gives `gcr.io/myproject/myimage/gcr.io/k8s-skaffold/skaffold-example1`; default-repo `gcr.io/k8s-skaffold` leaves the name unchanged; a shared prefix is not repeated.

The global config option `multi-level-repo` (boolean) stops Skaffold replacing `.` and `/` with `_` in the image name.

Insecure registries: Skaffold never downgrades to plain HTTP by itself; each registry must be named explicitly. Ways to do it:

- the repeatable `--insecure-registry` flag
- the `SKAFFOLD_INSECURE_REGISTRY` variable (comma-separated)
- `build.insecureRegistries` in `skaffold.yaml`
- `skaffold config set insecure-registries host:5000` for the current kube-context, or `skaffold config set --global insecure-registries host:5000` for any context. Repeated sets add to the list; `skaffold config unset insecure-registries` clears it.

Lists from several sources are joined.

Use `skaffold build --dry-run` or `skaffold render` to see the final image names before pushing. Keep a personal default repo in per-user config (or the flag or variable), not in `skaffold.yaml`, so the project stays usable by anyone. If behaviour surprises you, check all three places for a stale value.

## Checked

2026-11-04. Read the Skaffold "Image Repository Handling" page, the Global Configuration page and the CLI reference for `build`. Confirmed the three ways to set default-repo, the no-default behaviour, both rewriting strategies with the examples, `multi-level-repo`, and the four insecure-registry mechanisms and merging. Replaced the strategy names `escape`, `concat` and `concat-unless-prefix-matches` with the page's descriptions (the page does not name them as config values).
Method: documentation only; no commands were run.
