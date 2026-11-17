---
id: computing-software.devops-ci-cd.tilt.tilt-custom-build
name: tilt-custom-build
category: computing-software
field: devops-ci-cd
product: tilt
tags: [custom-build, tilt, expected-ref, image-builders]
level: advanced
status: docs-checked
description: "Build images with a non-docker_build tool in Tilt using custom_build: EXPECTED_REF, tag, outputs_image_ref_to, skips_local_docker, and immutable tags."
sources:
  - "https://docs.tilt.dev/custom_build.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# custom_build

Goal: use any image builder (Jib, Bazel, Buildah, a wrapper script). Check Tilt extensions first; otherwise use `custom_build`, which runs your build as a Tilt subprocess.

It requires an image name (a ref such as `frontend`), a command, and files to watch. A dependency change starts a build then applies the YAML.

## Recipes

Docker wrapper (also for flags `docker_build()` lacks):

```python
custom_build(
  'frontend',
  'docker build -t $EXPECTED_REF frontend',
  ['./frontend'],
)
```

Jib with Gradle:

```
custom_build(
  'example-java-image',
  './gradlew jibDockerBuild --image $EXPECTED_REF',
  deps=['src'])
```

Bazel rules_docker also writes to the local Docker store. Buildah has its own store, so build and push, and set `skips_local_docker=True` so Tilt does not verify the image locally:

```python
custom_build(
  'frontend',
  'buildah bud -t $EXPECTED_REF frontend && buildah push $EXPECTED_REF $EXPECTED_REF',
  ['./frontend'],
  skips_local_docker=True,
)
```

Buildah-style builders often need privileged access (sudo or a sandbox), and insecure registries must be configured in the builder (for Microk8s, add `localhost:32000` to registries.insecure).

## Coordinating with Tilt

Tilt deploys content-based tags such as `gcr.io/company-name/frontend:tilt-ffd9c2013b5bf5d4`.

- Good: Tilt sets `$EXPECTED_REF` (a randomized tag); your script tags the image with it; Tilt re-tags with a content-based tag and pushes.
- Hacky: the tool builds to a fixed tag; declare it with `custom_build(..., tag='gcr.io/company-name/frontend:dev')`. Less robust (mutable tag).
- Better: `outputs_image_ref_to='ref.txt'` means your script writes a tagged ref there. With a detected local registry, `REGISTRY_HOST` (for example `localhost:5000`) is set.
- Find the deploy tag: `tilt dump image-deploy-ref $EXPECTED_REF`. Rarely needed; for pods created by workflow engines prefer the custom resource guide.

## Other options

`live_update` and most `docker_build` options work. `ignore` takes `.dockerignore`-style patterns relative to each dep:

```python
custom_build(
    'image-foo',
    'docker build -t $EXPECTED_REF .',
    deps=['dep1', 'dep2'],
    ignore=['baz']
)
```

This ignores `dep1/baz` and `dep2/baz`.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/custom_build.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
