---
id: computing-software.devops-ci-cd.helm.template-functions-reference
name: template-functions-reference
category: computing-software
field: devops-ci-cd
product: helm
tags: [template-functions, sprig, pipelines, default, quote, toyaml, tojson, include, tpl, required]
level: practitioner
status: docs-checked
description: "Helm template functions: Go template plus Sprig (minus env/expandenv), pipelines, default, quote, required, tpl, include, toYaml, semver."
sources:
  - https://helm.sh/docs/chart_template_guide/function_list/
  - https://helm.sh/docs/chart_template_guide/functions_and_pipelines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Helm templates combine the Go template language, most of the Sprig library, and a few Helm additions. The docs state that Sprig `env` and `expandenv` are intentionally removed so rendering does not depend on the machine running Helm; pass environment-specific data through values instead.

Pipelines chain with `|`, and the piped value becomes the last argument of the next function: `{{ .Values.favorite.drink | repeat 5 | quote }}`. `default DEFAULT GIVEN` supplies a fallback; the docs say static defaults belong in `values.yaml` and `default` suits computed values.

Emptiness (used by `default`, `required`, `empty`, `if`): numeric 0, `""`, `[]`, `{}`, `false` and `nil`. Structs are never empty.

Logic: `and` returns the first empty argument or the last; `or` returns the first non-empty or the last; `not`, `eq`, `ne`, `lt`, `le`, `gt`, `ge`, `coalesce` (first non-empty), `ternary "yes" "no" TEST`, `empty`, `required "msg" VALUE`, `fail "msg"`. The current docs also list `all` and `any`, and note that Go's `and` does not short-circuit, which is why `dig` is recommended to avoid nil-field panics.

Helm-flavoured functions:

- `include "name" CTX` renders a named template to a string so it can be piped (`include "mychart.labels" . | indent 4`).
- `tpl STRING CTX` evaluates a string as a template.
- `lookup apiVersion kind namespace name` queries the cluster; it returns an empty response under `helm template`.
- `.Capabilities.APIVersions.Has "apps/v1"` tests API availability.
- `semver "1.2.3-alpha.1+123"` parses (with `.Major`, `.Minor`, `.Patch`, `.Prerelease`, `.Metadata`); `semverCompare "~1.2.0" "1.2.3"` tests a constraint with `~`, `^`, ranges, wildcards and `||`. Constraints without a prerelease part skip prereleases (`>=1.2.3` skips them, `>=1.2.3-0` finds them).
- `getHostByName` needs `--enable-dns`.

Serialisation: `toYaml`, `toYamlPretty` (indents list items further), `fromYaml`, `fromYamlArray`, `toJson`/`toPrettyJson`/`toRawJson`, `fromJson`, `fromJsonArray`, `toToml`, `fromToml`. `toJson` returns an empty string on failure whereas `mustToJson` raises an error; the same `must` prefix pattern applies across many functions.

Common groups:

- Strings: `trim`, `trimAll`, `trimPrefix`, `trimSuffix`, `upper`, `lower`, `title`, `trunc` (negative counts from the end), `quote`, `squote`, `replace OLD NEW STR`, `contains`, `hasPrefix`, `hasSuffix`, `cat`, `printf`, `snakecase`, `kebabcase`, `camelcase`, `indent`, `nindent`.
- Regex: `regexMatch`, `regexFind`, `regexFindAll PATTERN INPUT N`, `regexReplaceAll PATTERN INPUT REPL`, `regexSplit`.
- Math (int64): `add`, `sub`, `mul`, `div`, `mod`, `max`, `min`, `len`; float forms end in `f` (`addf`, `divf`, ...).
- Lists (immutable): `list`, `first`, `rest`, `last`, `initial`, `append`, `prepend`, `concat`, `uniq`, `without`, `has`, `compact`, `index`, `slice`, `until`, `untilStep`, `seq`, `chunk`, and `sortAlpha`.
- Dicts (string keys, mutable): `dict`, `get` (returns `""` when missing), `set`/`unset` (return the dict, so assign to `$_`), `hasKey`, `pluck`, `dig`, `merge` (earlier arguments win), `mergeOverwrite` (later arguments win), `keys`, `pick`, `omit`, `values`, `deepCopy`.
- Crypto: `sha1sum`, `sha256sum`, `htpasswd`, `genCA`, `genSelfSignedCert`, `genSignedCert`, `randAlphaNum`, `randBytes`; encoding: `b64enc`/`b64dec`, `b32enc`/`b32dec`.
- Dates: `now`, `date "2006-01-02"` (Go reference-date layout), `dateInZone`, `dateModify`, `toDate`, `unixEpoch`, `ago`, `duration`.

Operators are functions, so group with parentheses. Emit nested YAML with `{{ toYaml .Values.resources | nindent 12 }}`.

## Checked

2026-11-08. Checked against the Helm 4 function-list page (sections read and grepped for each cited function) and the Helm 3 copy. Confirmed Sprig env and expandenv are removed from Helm templates. Removed unsourced claims.

Method: documentation only; no commands were run.
