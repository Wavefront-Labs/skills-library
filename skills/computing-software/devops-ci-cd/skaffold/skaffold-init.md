---
id: computing-software.devops-ci-cd.skaffold.skaffold-init
name: skaffold-init
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [init, bootstrap, generate, detection]
level: intro
status: docs-checked
description: "Generate a first skaffold.yaml by letting Skaffold detect builders and manifests in an existing project."
sources:
  - "https://skaffold.dev/docs/init/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`skaffold init` inspects the project and writes a skaffold.yaml.

```bash
skaffold init
skaffold init --force
```

It detects Dockerfiles, Jib projects (Maven or Gradle), Ko and Buildpacks. It generates `kubectl` or `kustomize` deploy configuration when it finds Kubernetes manifests or kustomization files. Files larger than 500MB are skipped.

Flow: run it in the project root. With several build files it prompts you to pair each image found in your deploy configuration with a build file; choose `None (image not built from these sources)` when none fits, and then set up that artifact's build by hand.

- `--force` removes the prompts and makes a best-effort config. With one image and several detectable builders it picks Docker, then Jib, Ko, Bazel, Buildpacks in that order. It does not support multiple images yet.
- `--generate-manifests` tries to generate basic Kubernetes manifests for a project that has none.
- `--default-kustomization` picks the default kustomize overlay. Otherwise Skaffold uses an overlay named `dev`, else the first overlay not named `prod`; other overlays become profiles. It expects the Kustomize `base/` and `overlays/` layout.
- `--analyze` prints JSON of the Dockerfiles and image names found, and `--artifact` (`-a`) generates build config from a JSON or `=`-delimited pair, which IDEs use.

Build detection looks for files such as `Dockerfile`, `build.gradle`, `pom.xml`, `package.json`, `requirements.txt` and `go.mod`.

Exit codes on failure: 101 no build configuration found, 102 no Kubernetes manifest found or generated, 103 an existing skaffold.yaml was found, 104 builders could not be matched to image names automatically.

Use `skaffold fix` later to upgrade an older file to a newer schema version.

## Checked

2026-11-09: confirmed against the Skaffold docs page "Init" (source docs-v2/content/en/docs/init.md): supported builders, the 500MB skip, deploy detection, --force, --generate-manifests, kustomize overlay heuristic, init API flags and exit codes; `skaffold fix` is in the CLI reference. Removed unverified post-init advice.

Method: docs-checked 2026-11-09 against skaffold.dev init page and CLI reference (read as source markdown).
