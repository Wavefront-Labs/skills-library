---
id: computing-software.cloud-infrastructure-engineering.terraform.validate-json-diagnostics-output
name: validate-json-diagnostics-output
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, validate-json, diagnostics-json, terraform-validate, ci-annotations, jq, error-count, warning-count, static-check]
level: practitioner
status: verified
description: "Parse terraform validate -json: the diagnostics schema (severity, summary, detail, range, snippet), turning it into PR annotations, and the limits of what validate can see."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/validate#json-output-format", "https://developer.hashicorp.com/terraform/cli/commands/validate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `validate -json` diagnostics output

**Goal:** turn validation errors into file:line annotations on the pull request
instead of a wall of text in a CI log.

## 1. Produce
```bash
terraform init -backend=false -input=false     # providers needed for schema checks; no state
terraform validate -json > validate.json
echo $?    # 0 valid, 1 invalid (checked); the -json document is still written to stdout
```

## 2. Schema
```json
{
  "format_version": "1.0",
  "valid": false,
  "error_count": 1,
  "warning_count": 0,
  "diagnostics": [
    {
      "severity": "error",
      "summary": "Unsupported argument",
      "detail": "An argument named \"contnt\" is not expected here. Did you mean \"content\"?",
      "range": {
        "filename": "main.tf",
        "start": {"line": 9, "column": 3, "byte": 181},
        "end":   {"line": 9, "column": 9, "byte": 187}
      },
      "snippet": {
        "context": "resource \"local_file\" \"f\"",
        "code": "  contnt   = \"x\"",
        "start_line": 9, "highlight_start_offset": 2, "highlight_end_offset": 8,
        "values": []
      }
    }
  ]
}
```
- `range` and `snippet` are optional: a diagnostic not tied to a file (run: `Missing
  required provider`) has neither, only `severity`, `summary`, `detail`.
- `snippet.values` is an array of `{traversal, statement}` objects explaining
  complex expressions; it was `[]` for every diagnostic in my runs, and the
  `statement` text may change between versions (docs).
- Warnings do not flip `valid` to false; `error_count` is 0 when `valid` is true (docs).

## 3. Annotations
```bash
jq -r '.diagnostics[] | "::\(.severity) file=\(.range.filename // "unknown"),line=\(.range.start.line // 1),col=\(.range.start.column // 1)::\(.summary): \(.detail // "" | gsub("\n";" "))"' validate.json
```
Other report formats need their own mapping of the same fields. Make the job fail
on `.valid == false`, not just on exit code, so a crashed `jq` does not pass.

## 4. What validate can and cannot catch
Caught in runs: unknown arguments (`Unsupported argument`, with a "Did you mean"
hint), undeclared variable references, unsupported attributes on a resource,
duplicate resources, an invalid variable default type.
Not caught in runs: `tonumber(var.s)` on a variable defaulting to `"abc"` (variables
are unknown to validate, so it reported `valid: true`) and an out-of-range static
`terraform_data.a["zzz"]` key. Also outside validate: anything needing state or
real values, provider-side checks (invalid instance type), backend reachability.
Note validate can stop at the first parse-level error class (a duplicate resource
hid the other mistakes), so fix and re-run.

## Gotchas
- `validate` with no prior `init` reports `Missing required provider` (run) and
  suggests `terraform init`; `init -backend=false` is enough and needs no backend
  credentials.
- Run it per **root module**; it does not recurse. For a module repo, validate
  each `examples/*` directory (they have root-module context).
- `terraform validate -json` in a module with a `cloud {}` block still works after
  `init -backend=false` (ran: `valid: true`).
- `format_version` is `"1.0"` since Terraform 1.1.0; per the docs, ignore unknown
  properties and reject an unsupported major version.

## Verify
- [ ] Introducing a typo in an attribute yields a diagnostic with `range.filename` and the correct line.
- [ ] The CI annotation appears on that line in the PR diff.
- [ ] `jq .valid validate.json` is `true` on main.

## Checked
- Terraform 1.17.0 with `hashicorp/local`: ran `validate -json` before init (`Missing required provider`, no range) and after `init -backend=false` with a misspelt argument and an undeclared variable (range, snippet, values `[]`, exit 1); ran the skill's jq annotation command with jq 1.8.2 (prints `::error file=main.tf,line=9,col=3::...`); a `cloud {}` config validated true; `tonumber(var.s)` and `zzz` key were not flagged.
- Docs page for validate: format_version 1.0 since 1.1.0, optional range/snippet, values objects, warnings keep valid true. GitHub workflow-commands docs confirm `::error file=,line=,col=::` and `::warning` syntax. A subdirectory with a broken `.tf` file did not affect validate of the parent (no recursion).
