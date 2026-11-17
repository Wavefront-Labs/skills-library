---
id: computing-software.cloud-infrastructure-engineering.kyverno.cli-jp-query
name: cli-jp-query
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [kyverno-jp, jp-query, jmespath-testing, unquoted-output, cli-jp]
level: intro
status: docs-checked
description: "Test JMESPath expressions with kyverno jp query: input file or stdin, query files, compact and unquoted output, and the usage forms."
sources:
  - https://kyverno.io/docs/kyverno-cli/reference/kyverno_jp_query/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Usage: `kyverno jp query [-i input] [-q query|query]... [flags]`.

Flags:
- `-i`/`--input`: read JSON or YAML from a file instead of stdin.
- `-q`/`--query`: read a JMESPath expression from a file; repeat to evaluate several.
- `-c`/`--compact`: compact JSON without extra whitespace.
- `-u`/`--unquoted`: print a string result without quotes.

Forms, all from the reference:
- Inline: `kyverno jp query -i object.yaml 'request.object.metadata.name | truncate(@, `9`)'`
- From file: `kyverno jp query -i object.yaml -q query-file`
- Several files plus inline: `-q query-file-1 -q query-file-2 '<expr>'`
- Query on stdin: `cat query-file | kyverno jp query -i object.yaml`
- Object on stdin: `cat object.yaml | kyverno jp query -q query-file`

Use it to check Kyverno custom filters (such as `truncate`) before putting them in a policy; number literals need backticks inside the expression. A sibling command in the CLI reference is `kyverno jp parse`.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/kyverno-cli/reference/kyverno_jp_query/.

Method: documentation only; no commands were run.
