---
id: computing-software.software-engineering.api-design.linting-apis-with-spectral
name: linting-apis-with-spectral
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, spectral-linting, spectral, openapi-lint, api-style-guide, governance, ci]
level: practitioner
status: docs-checked
description: "Enforce an API style guide with Spectral rulesets: extend spectral:oas, write custom JSONPath rules, set severities and fail CI on violations."
sources: ["https://github.com/stoplightio/spectral/blob/develop/docs/guides/2-cli.md", "https://github.com/stoplightio/spectral/blob/develop/docs/guides/4a-rules.md", "https://github.com/stoplightio/spectral/blob/develop/docs/guides/4b-extends.md", "https://github.com/stoplightio/spectral/blob/develop/docs/getting-started/2-installation.md", "https://github.com/stoplightio/spectral/blob/develop/docs/getting-started/3-rulesets.md", "https://github.com/stoplightio/spectral/blob/develop/docs/reference/functions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linting OpenAPI with Spectral

## Setup
```bash
npm install -g @stoplight/spectral-cli
spectral lint openapi.yaml --fail-severity=warn
```
Without `--ruleset`, the CLI looks in the working directory for `.spectral.yml`, `.spectral.yaml`, `.spectral.json` or `.spectral.js`. If no ruleset is given and none is found, it does not lint the document. Standalone binaries and a `stoplight/spectral` Docker image also exist.

## Ruleset
```yaml
extends: ["spectral:oas"]
rules:
  operation-description: warn      # severity shortcut for an inherited rule
  operation-tags: error
  paths-kebab-case:
    description: Paths should be kebab-case.
    message: "{{property}} should be kebab-case (lower-case and separated with hyphens)"
    severity: warn
    given: $.paths[*]~
    then:
      function: pattern
      functionOptions:
        match: "^(\/|[a-z0-9-.]+|{[a-zA-Z0-9_]+})+$"
```
Rule properties: `given` (required, JSONPath, or an array of them) and `then` (required) plus optional `description`, `message`, `severity`, `formats`, `recommended` and `resolved`. `then` takes a `function`, an optional `field` (`@key` targets object keys) and `functionOptions`; a list of `then` entries checks several fields. Built-in functions include `pattern`, `truthy`, `falsy`, `enumeration`, `casing`, `schema`, `length`, `alphabetical`, `defined` and `undefined`. `~` in `given` selects the key itself. Message placeholders: `{{error}}`, `{{description}}`, `{{path}}`, `{{property}}`, `{{value}}`.

`spectral:oas` covers OpenAPI v2/v3; `spectral:asyncapi` and `spectral:arazzo` also ship built in.

## Gotchas
- Severities are `error`, `warn`, `info`, `hint` (and `off` in a rule). A rule's default severity is `warn`. Only errors give a failure exit code by default; `--fail-severity=warn` also fails on warnings. `--display-only-failures` (`-D`) hides lower-severity output without changing the exit code.
- Redefining a rule with the same name in your ruleset replaces the inherited rule; `rule-name: warn` only changes its severity.
- `extends` accepts a string or array of local file paths, URLs or npm modules, so one shared ruleset can serve every repo.
- Rules run on the resolved document (`$ref`s replaced) unless you set `resolved: false`.
- `-f` selects formatters (for example `json`, `junit`, `github-actions`, `sarif`); several `-f` flags need an `-o` target for each.
- A `given` path that matches nothing passes silently; test each rule against a deliberately bad sample.

Verify: write a spec that violates each custom rule and confirm `spectral lint` reports exactly those rule codes and exits non-zero; then run it on the real spec in CI.

## Checked
2026-11-08. Confirmed against the Spectral repo docs (CLI guide, rules, extends, installation, rulesets getting-started, core functions reference) and the `operation-description`, `operation-tags` and `operation-success-response` entries of the OpenAPI rules reference (found by search, not read in full). Removed: the `no-unbounded-lists` schema rule (untested construction), the pin-the-version advice, and the stoplight.io docs links (not fetched; the repo docs carry the same content).
Method: documentation only; no commands were run.
