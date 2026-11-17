---
id: computing-software.devops-ci-cd.packer.can-try-functions
name: can-try-functions
category: computing-software
field: devops-ci-cd
product: packer
tags: [can, try, validation, errors, fn-can-try]
level: advanced
status: docs-checked
description: "Use can() in validation conditions and try() to fall back when an expression errors."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/functions/conversion/can/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`can(expression)` evaluates the expression and returns a boolean: `true` if it produced a result without errors, `false` otherwise.

```
> local.foo
{
  "bar" = "baz"
}
> can(local.foo.bar)
true
> can(local.foo.boop)
false
```

`can` is intended only for simple tests in variable validation rules. It can technically take any expression, but HashiCorp recommends against using it elsewhere; for error handling elsewhere prefer `try`.

`try(expr1, expr2, ...)` evaluates its arguments in turn and returns the result of the first one that does not produce an error, which gives a concise fallback:

```
> try(local.foo.bar, "fallback")
baz
> try(local.foo.boop, "fallback")
fallback
```

Guidance from the docs:

- `try` suits normalising data whose shape is not well known, for example `groups = try(local.raw_value.groups, [])`. Confine it to special local values that perform normalisation, so the rest of the configuration uses plain references.
- Use `try` only with simple attribute references and type conversion functions. Overuse to suppress errors makes a configuration hard to maintain.
- If `try` exhausts all expressions without one succeeding, it returns an error describing all the problems it encountered.
- Neither function catches errors for constructs provably invalid regardless of input, such as a malformed reference or a reference to an undeclared local (`can(local.nonexist)` still fails with "Reference to undeclared local value"). They catch only dynamic errors from data not known until runtime.

## Checked

Method: docs-checked 2026-11-09 against the Packer `can` function page and the companion `try` function page (read in full as published page source). Dropped the cidrnetmask example, the bool-condition note and the lookup/merge aside as unconfirmed.
