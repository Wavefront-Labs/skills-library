---
id: computing-software.devops-ci-cd.tilt.tilt-file-changes
name: tilt-file-changes
category: computing-software
field: devops-ci-cd
product: tilt
tags: [file-changes, tilt, tiltignore, filewatch]
level: advanced
status: docs-checked
description: "Debug Tilt rebuilds and ignores: where file watches come from, .dockerignore, ignore=, only=, .tiltignore, watch_settings and the FileWatch CLI."
sources:
  - "https://docs.tilt.dev/file_changes.html"
  - "https://docs.tilt.dev/custom_build.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging file changes in Tilt

Goal: understand why a file change did or did not trigger a build.

## Where watches come from

- The Tiltfile is always watched. A change re-executes it (re-running `local()` calls), then only changed `docker_build()` and `k8s_yaml()` configs rebuild.
- `helm()`, `load()` and `read_file()` watch the files they read. A `local()` call reading a file is invisible to Tilt; add `watch_file()`.
- `docker_build()` watches its whole context directory; `custom_build()` and `local_resource()` watch their `deps` paths.

## Where ignores come from

- `.git` is always ignored and removed from the `docker_build` context. To include it, use `custom_build`.
- Hard-coded editor temp files (Emacs, Vim and so on) do not trigger builds, but are still in Docker contexts by default.
- `.dockerignore` in the build directory: matching files neither trigger rebuilds nor enter the context.
- `docker_build(..., ignore=[...])`: image-specific patterns relative to `context`. `docker_build('image-foo', './foo', ignore=['bar'])` ignores `foo/bar`. `custom_build` and `local_resource` also take `ignore=` but handle it differently; for `custom_build` the patterns are evaluated relative to each dep.
- `only=` keeps only listed paths (paths, not globs, relative to context):

```python
docker_build('image-foo', './foo', only=['./src', './static-files'])
```

equivalent to a `.dockerignore` of `**`, `!./src`, `!./static-files`. Other build types have no `only=`.
- `.tiltignore` next to the Tiltfile, `.dockerignore` syntax: stops rebuild triggers but does not affect Docker contexts.
- `watch_settings(ignore=)`: same as `.tiltignore`; useful for extensions that download files. Also does not affect Docker contexts.

## Inspect watches

```shell
tilt get filewatches
tilt describe filewatches
tilt get filewatches configs:singleton -o yaml
```

Names look like `configs:singleton` (Tiltfile reload) and `image:example-html-image` (image rebuild). The status lists seen file events.

`tilt edit` changes a watch live:

```
EDITOR=emacs tilt edit filewatch configs:singleton
```

Removing paths stops reloads. Reloading the Tiltfile regenerates all watches, discarding edits. The tilt-dev/ignore-examples repo lets you experiment.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/file_changes.html, https://docs.tilt.dev/custom_build.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Reworded the ignore= claim for custom_build and local_resource; only the custom build guide (added to sources) states the relative-to-dep rule.

Method: documentation only; no commands were run.
