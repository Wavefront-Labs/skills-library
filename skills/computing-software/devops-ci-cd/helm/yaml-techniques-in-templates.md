---
id: computing-software.devops-ci-cd.helm.yaml-techniques-in-templates
name: yaml-techniques-in-templates
category: computing-software
field: devops-ci-cd
product: helm
tags: [yaml, multiline-strings, block-scalars, anchors, indent, nindent, quote, strings]
level: practitioner
status: docs-checked
description: "YAML tricks in Helm templates: strings and quoting, block scalars, indent vs nindent, anchors and type surprises."
sources:
  - https://helm.sh/docs/chart_template_guide/yaml_techniques/
  - https://helm.sh/docs/chart_template_guide/functions_and_pipelines/
  - https://helm.sh/docs/chart_template_guide/function_list/
  - https://helm.sh/docs/chart_best_practices/values/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

YAML scalars are typed by content, which causes common chart bugs.

Types: an unquoted integer, float or `true`/`false` is numeric or boolean; quoted is a string (`count: "1"` is a string). The empty value is `null`, not `nil`. `port: "80"` passes the template engine and the YAML parser but fails if Kubernetes expects an integer. Node tags can force a type (`age: !!str 21`, `port: !!int "80"`), but the best-practices guide warns the parser consumes tags, so the type data is lost after one parse. Large integers such as `12345678` can be converted to scientific notation in some cases; the guide suggests storing them as strings and using `{{ int $value }}` in the template.

Quoting: `quote` wraps a string in double quotes and `squote` in single quotes; `{{ .Values.favorite.drink | quote }}` is the usual guard for strings. In YAML itself, bare words are unescaped, double-quoted strings use `\` escapes, and single-quoted strings are literal (only `''` is an escape).

Multi-line strings:

- Literal block `|` keeps newlines (one trailing newline).
- Folded `>` folds newlines to spaces.
- `|-` / `>-` strip the final newline; `|+` keeps all trailing newlines.
- Indented lines inside a block keep their indentation and line breaks, even in folded blocks.
- The first line after `|` must be indented correctly; a fake commented first line protects against the parse error when injecting file contents, but that line is preserved in the string.

Inject a static file or an included template with `nindent`:

```yaml
myfile: |
  {{- .Files.Get "myfile.txt" | nindent 2 }}
```

`indent N` indents every line by N spaces; `nindent N` does the same and prepends a newline. `{{-` trims the whitespace to the left, and `nindent` re-adds the newline with correct indentation.

Documents: a template file may hold several documents separated by `---`; the file is rendered as one object and then split before it reaches Kubernetes. The guide recommends this only when necessary because it is hard to debug. Files such as `values.yaml` use only the first document.

JSON is valid YAML, so `values.yaml` may contain JSON, but Helm does not treat a `.json` extension as a valid suffix for it.

Anchors and aliases (`&name`, `*name`) are expanded the first time the YAML is consumed and then discarded. Because Helm and Kubernetes read, modify and rewrite YAML, the anchors are lost on the round trip. For sharing snippets across charts the docs point to library charts instead.

## Checked

2026-11-08. Checked against the Helm 4 docs (docs/ tree of helm-www): the cited template-guide pages were read, and the Helm 3 copies compared where behaviour differs. Removed unsourced claims.

Method: documentation only; no commands were run.
