---
id: computing-software.devops-ci-cd.backstage.scaffolder-conditional-logic
name: scaffolder-conditional-logic
category: computing-software
field: devops-ci-cd
product: backstage
tags: [template-if, conditional-steps, conditional-fields, backstage]
level: practitioner
status: docs-checked
description: "Run steps conditionally with if expressions and show fields based on earlier answers in template parameters."
sources:
  - https://backstage.io/docs/features/software-templates/input-examples
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Templates can branch on user input.

Conditional steps use an `if` expression evaluated with the same `${{ }}` syntax:

```yaml
steps:
  - id: deployStaging
    name: Deploy to staging
    action: acme:deploy
    if: ${{ parameters.environment === "staging" or parameters.environment === "development" }}
  - id: approveProd
    name: Request approval
    action: acme:approve
    if: ${{ parameters.environment === "prod" or parameters.environment === "production" }}
```

The docs examples use `===`, `!==`, `and` and `or`. The inline `if` uses Nunjitsu's Nunjucks-compatible syntax, and the `not` keyword is unavailable: use JavaScript equality instead.

Conditional form fields use JSON Schema `dependencies` with `allOf` and `if`/`then`, so a later field appears only after an earlier answer:

```yaml
parameters:
  - title: Fill in some steps
    properties:
      includeName:
        title: Include Name?
        type: boolean
        default: true
    dependencies:
      includeName:
        allOf:
          - if:
              properties:
                includeName:
                  const: true
            then:
              properties:
                lastName:
                  title: Last Name
                  type: string
              required:
                - lastName
```

`ui:order` controls field order when several fields are conditional.

Other patterns in the input examples page: simple text with validations and custom error messages, multi-line text, arrays with custom titles, multi-choice lists, boolean variants, Markdown text blocks, and conditionally setting parameters.

## Checked

2026-11-03. Confirmed against the Backstage Input Examples page: step `if` expressions, the `not` limitation, the `dependencies`/`allOf`/`if`/`then` pattern. Removed: the `oneOf` example (the docs use `allOf` with `if`/`then`), the `not` operator, and the claim about skipped-step outputs.

Method: documentation only; no commands were run.
