---
id: computing-software.devops-ci-cd.kustomize.json6902-operations
name: json6902-operations
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [json6902, add, replace, remove, copy, move, test]
level: practitioner
status: docs-checked
description: "The six JSON6902 operations accepted by kustomize patches: add, replace, copy, move, remove and test, with what each does."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patchesjson6902/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patches/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The reference lists the operations a JSON patch file may contain, in JSON or YAML:

```yaml
# add: creates a new entry with a given value
- op: add
  path: /some/new/path
  value: value
# replace: replaces the value of the node with the new specified value
- op: replace
  path: /some/existing/path
  value: new value
# copy: copies the value specified in from to the destination path
- op: copy
  from: /some/existing/path
  path: /some/path
# move: moves the node specified in from to the destination path
- op: move
  from: /some/existing/path
  path: /some/existing/destination/path
# remove: deletes the node (and its subtree)
- op: remove
  path: /some/path
# test: checks the node has the value; if it differs it throws an error
- op: test
  path: /some/path
  value: "my-node-value"
```

`copy` and `move` use `from` plus `path`.

The patch format is defined by RFC 6902 (https://tools.ietf.org/html/rfc6902). In the current `patches` field, put these operations inline in `patch:` or in a file named by `path:`; the `target` field is always required for JSON6902 patches. In a patch path a `/` inside a key such as a label name is written as `~1` (for example `/metadata/labels/app.kubernetes.io~1version`).

A patch can refer to a resource by any of its previous names or kinds, so it works after a name-prefix transformation.

The `patchesJson6902` field was deprecated in v5.0.0; move entries into `patches`.

## Checked

2026-11-08: read the patchesJson6902 and patches reference pages in full. Confirmed the six operations, JSON and YAML forms, inline `patch` and file `path`, mandatory target, `~1` escape, previous-names behaviour and the deprecation. Removed the use-case bullets for `test` and `remove` (container index), which are not stated on the pages.

Method: documentation only; no commands were run.
