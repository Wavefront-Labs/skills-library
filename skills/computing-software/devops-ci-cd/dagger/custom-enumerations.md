---
id: computing-software.devops-ci-cd.dagger.custom-enumerations
name: custom-enumerations
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, enumerations, enums, arguments, validation]
level: practitioner
status: docs-checked
description: "Define an enum type in a Dagger module (Go, Python, TypeScript, Java) to restrict string argument values, and read the CLI help and error for invalid choices."
sources: [https://docs.dagger.io/0.21/extending/modules/enumerations]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enumerations in Dagger modules

Goal: restrict a string argument to a fixed set of values (Dagger 0.21 docs). Supported in Go, Python, TypeScript and Java; not in the PHP SDK. Enum values are validated strictly, so null, true or false cannot slip through.

## Rules (GraphQL spec)

Enum names cannot start with a digit and may contain only letters, digits and `_`. Values are case-sensitive and conventionally upper-case. Enums are strings in the API schema.

## Define

Go: a string type with typed constants; doc comments become descriptions.

```go
// Vulnerability severity levels
type Severity string

const (
	// Undetermined risk; analyze further.
	Unknown  Severity = "UNKNOWN"
	Low      Severity = "LOW"
	Medium   Severity = "MEDIUM"
	High     Severity = "HIGH"
	Critical Severity = "CRITICAL"
)

func (m *MyModule) Scan(ctx context.Context, ref string, severity Severity) (string, error) { ... }
```

Python: `@enum_type` on an `enum.Enum` subclass (`dagger.Enum` is a convenience base for documentation, `enum.Enum` works directly); use `severity.name` when passing to a command.

```python
@enum_type
class Severity(enum.Enum):
    """Vulnerability severity levels"""
    UNKNOWN = "UNKNOWN"
    LOW = "LOW"
```

TypeScript: `export enum Severity { Unknown = "UNKNOWN", Low = "LOW", ... }`. Java: annotate the enum with `@Enum` or Dagger will not recognize it.

The docs example is a Trivy scan: `scan <ref> <severity>`, passing `--severity=...` to `trivy image`.

## Use from the CLI

`dagger call scan --help` lists the choices:

```
--severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL   [required]
```

An invalid value fails with:

```
Error: invalid argument "FOO" for "--severity" flag: value should be one of UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL
```

Shell: `.help scan` shows `severity MyModuleSeverity (possible values: ...)`.

## Gotcha

The page's TypeScript snippet passes `` `severity=${severity}` `` to the command (no leading dashes) while the Go and Python snippets pass `--severity=`; use the dashed form. (Observation from the snippets, not stated in prose.)

## Related

computing-software.devops-ci-cd.dagger.function-arguments-basic-types

## Checked

2026-11-07

Read in full from the docs source: extending/modules/enumerations.mdx and its snippets. Every claim and snippet matched. No corrections needed.

Method: documentation only; no commands were run.
