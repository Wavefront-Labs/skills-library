---
id: computing-software.devops-ci-cd.kustomize.replacements-delimiter-index
name: replacements-delimiter-index
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [replacements, delimiter, index, partial-string]
level: advanced
status: docs-checked
description: "Replace part of a string value with options.delimiter and options.index, in sources or targets, and know the out-of-bounds behavior."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replacements/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`delimiter` and `index` support partial string replacement.

For a value `path: my/path/VALUE`, a target can say:

```yaml
options:
  delimiter: '/'
  index: 2
```

and it replaces only the third segment, giving `my/path/NEW_VALUE`.

Rules from the reference:

- `delimiter` splits and rejoins the field value.
- `index` selects which position after the split; the default is 0.
- Source out of bounds: an index outside the split throws an error.
- Target out of bounds: a value less than 0 prefixes the target, and a value beyond the length of the split suffixes it.
- If `index` and `delimiter` are used on non-scalar values (mappings or lists), kustomize throws an error.

Source side: `options` on `source` can read one segment of the source value, for example to take just the tag of an image string and write it elsewhere.

Test with `kustomize build` and inspect the string output.

## Checked

2026-11-03. Confirmed against: the replacements reference page.
Removed or reworded: the use-case examples and the claim about a wrong delimiter.

Method: documentation only; no commands were run.
