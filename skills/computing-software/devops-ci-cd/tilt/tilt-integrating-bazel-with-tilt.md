---
id: computing-software.devops-ci-cd.tilt.tilt-integrating-bazel-with-tilt
name: tilt-integrating-bazel-with-tilt
category: computing-software
field: devops-ci-cd
product: tilt
tags: [integrating-bazel-with-tilt, tilt, bazel, custom-build]
level: advanced
status: docs-checked
description: "Wire a Bazel project (rules_docker, rules_k8s) into a Tiltfile with local(), custom_build and bazel query for YAML and image dependencies."
sources:
  - "https://docs.tilt.dev/integrating_bazel_with_tilt.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integrating Bazel with Tilt

Goal: a Tiltfile needs only Kubernetes YAML and Docker images; ask Bazel for both, then tell Tilt which files matter.

## YAML

`bazel run //:snack-server.apply` builds, puts the image into the YAML and runs `kubectl apply`. Running the target without `.apply` just prints the YAML. So:

```python
def bazel_k8s(target):
  return local("bazel run %s" % target)

k8s_yaml(bazel_k8s(":snack-server"))
```

## Images

rules_docker loads an image into Docker with `bazel run //path/to/my-command:image -- --norun`, producing `bazel/path/to/my-command`. The image name is `"bazel/" + directory of the build file + ":" + rule name`, so `bazel/snack:image`. Use `custom_build`:

```python
def bazel_build(image, target):
  custom_build(
    image,
    'bazel run --platforms=@io_bazel_rules_go//go/toolchain:linux_amd64 %s -- --norun' % target,
    [],
    tag="image",
  )

bazel_build('bazel/snack', '//snack:image')
```

`--platforms` makes Bazel build Go binaries for the Linux container; other languages may need an equivalent. The third argument is the watched file list (empty is fine at first).

## Dependencies

Without dependencies, editing `snack/main.go` updates nothing. Tilt distinguishes Tiltfile dependencies (files read during execution; changes re-execute the Tiltfile) from image dependencies (build context or container files; changes update a container). Use `bazel query`:

```python
BAZEL_SOURCES_CMD = """
  bazel query 'filter("^//", kind("source file", deps(set(%s))))' --order_output=no
  """.strip()
BAZEL_BUILDFILES_CMD = """
  bazel query 'filter("^//", buildfiles(deps(set(%s))))' --order_output=no
  """.strip()
```

For YAML, feed both query results through a `watch_labels` helper that calls `watch_file()` on each label's path (skipping `@` and `//external` labels). For images, `watch_labels` the build files and pass the source files as `custom_build` deps, so a change rebuilds the image and updates the YAML.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Integrating Bazel with Tilt page in full including all code snippets (Getting YAML, Building Images, YAML and image dependencies, `watch_labels`). Confirmed the `.apply` behaviour, the `--norun` image load, the `bazel/` image naming formula, the `--platforms` note, the empty dependency list, the two `bazel query` commands and which labels are skipped. Not opened: the linked bazel_example and tilt-example-bazel repositories, rules_docker and rules_k8s docs. Trimmed: the "(rules_k8s resolve)" label (only present in a link anchor on the page); "patches YAML" reworded to the page's "put that image in to my YAML". 

Method: documentation only; no commands were run.
