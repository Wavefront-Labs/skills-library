---
id: computing-software.devops-ci-cd.helm.template-control-flow
name: template-control-flow
category: computing-software
field: devops-ci-cd
product: helm
tags: [if-else, with, range, whitespace, control-structures, scope, trimming, template-language]
level: practitioner
status: docs-checked
description: "Go template control flow in Helm: if/else, with, range, truthiness rules and whitespace trimming with {{- and -}}."
sources:
  - https://helm.sh/docs/chart_template_guide/control_structures/
  - https://helm.sh/docs/chart_template_guide/variables/
  - https://helm.sh/docs/chart_template_guide/functions_and_pipelines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`if/else` evaluates a pipeline, not just a value:

```yaml
{{ if PIPELINE }}
  # Do something
{{ else if OTHER PIPELINE }}
  # Do something else
{{ else }}
  # Default case
{{ end }}
```

A pipeline is false when it is a boolean false, numeric zero, empty string, `nil`, or an empty collection (map, slice, tuple, dict, array). Everything else is true. Operators (`eq`, `ne`, `lt`, `gt`, `and`, `or`) are functions, so group with parentheses: `{{ if and .Values.favorite.drink (eq .Values.favorite.drink "coffee") }}`.

`with` changes scope: inside `{{ with .Values.favorite }}` the dot is that object, and the block runs only if the value is not empty. The previous scope returns after `{{ end }}`. Reading `.Release.Name` inside the block fails; use `$`, which is mapped to the root scope when execution begins and does not change (`{{ $.Release.Name }}`).

`range` iterates lists and maps and sets the dot to the current element. Capture index and value with variables: `{{ range $index, $topping := .Values.pizzaToppings }}`, keys and values with `{{ range $key, $val := .Values.favorite }}`. `tuple` makes a fixed list inline: `{{ range tuple "small" "medium" "large" }}`.

Variables: `{{ $relname := .Release.Name }}` assigns with `:=`. They are scoped to the block that declares them, so a top-level variable is visible for the whole template while `$key` and `$val` live only inside the `range`. `$` always points at the root context, handy for `$.Chart.Name` inside a loop.

Whitespace: the engine removes what is inside `{{ }}` but leaves the surrounding whitespace. `{{- ` chomps whitespace to the left (including newlines) and ` -}}` to the right. A space must follow the dash: `{{- 3 }}` trims and prints 3 while `{{-3 }}` prints -3. Chomping both sides of a line can merge lines, for example `food: "PIZZA"mug: "true"`. Typical safe block:

```yaml
  food: {{ .Values.favorite.food | upper | quote }}
  {{- if eq .Values.favorite.drink "coffee" }}
  mug: "true"
  {{- end }}
```

The `indent` function is an alternative to hand-tuning spaces.

Pipelines: `default` supplies fallbacks, e.g. `{{ .Values.favorite.drink | default "tea" | quote }}`; the piped value is the last argument. Template comments are `{{/* comment */}}`.

## Checked

2026-11-08. Checked against the Helm 4 template-guide pages for control structures, variables and named templates, read in full. Removed unsourced claims.

Method: documentation only; no commands were run.
