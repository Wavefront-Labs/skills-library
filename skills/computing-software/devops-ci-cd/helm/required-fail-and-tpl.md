---
id: computing-software.devops-ci-cd.helm.required-fail-and-tpl
name: required-fail-and-tpl
category: computing-software
field: devops-ci-cd
product: helm
tags: [required, fail, tpl, default, error-messages, validation, dynamic-values]
level: practitioner
status: docs-checked
description: "Fail rendering early with required and fail, and evaluate templated strings inside values with tpl."
sources:
  - https://helm.sh/docs/chart_template_guide/function_list/
  - https://helm.sh/docs/howto/charts_tips_and_tricks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`required` declares a value mandatory. If the value is empty or undefined, the template does not render and Helm returns your message. "Empty" follows the `default` rules: `0`, `""`, `[]`, `{}`, `false`, `nil`.

```yaml
value: {{ required "A valid .Values.who entry required!" .Values.who }}
```

Go's `missingkey=error` option would fail on every missing map key; `required` lets a chart enforce this for selected values only.

`fail` returns an error with your text unconditionally, so use it in a branch after other conditions decided rendering must stop:

```yaml
{{- if and .Values.a .Values.b }}
{{- fail "set only one of a and b" }}
{{- end }}
```

`tpl` evaluates a string as a template inside a template: `{{ tpl TEMPLATE_STRING VALUES }}`. It lets values carry template expressions, or renders external config files:

```yaml
# values
template: "{{ .Values.name }}"
name: "Tom"

# template
{{ tpl .Values.template . }}      # renders: Tom

# external file conf/app.conf containing firstName={{ .Values.firstName }}
{{ tpl (.Files.Get "conf/app.conf") . }}
```

The second argument is the context the string is evaluated against; pass `.` at the top level so `.Values` and `.Release` resolve (inside `range` or `with`, pass `$`, the root).

Notes:

- `default` treats `false` and `0` as empty, so it cannot preserve an explicit `false`; use `hasKey` (or an explicit nil test) when false is meaningful.
- `required` and `fail` fire at render time, so they also run in dry-run and template renders; they are a cheap validation layer next to a schema file.

## Checked

2026-11-08. Checked against the Helm 4 function-list and template-guide pages for required, fail and tpl. Removed unsourced claims.

Method: documentation only; no commands were run.
