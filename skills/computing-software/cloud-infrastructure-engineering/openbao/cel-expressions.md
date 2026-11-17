---
id: computing-software.cloud-infrastructure-engineering.openbao.cel-expressions
name: cel-expressions
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, cel, expressions, validation, pki]
level: advanced
status: docs-checked
description: "How OpenBao uses CEL in PKI and JWT: variables, the request map, the main expression and the validation responsibility it hands you."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/cel.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CEL in OpenBao

CEL (Common Expression Language) declares validation rules and policies in PKI and JWT. The main expression decides acceptance: success returns the engine's output object (`ValidationOutput` for PKI, `pb.Auth` for JWT/OIDC); failure returns a string or bool error message, which can itself be a CEL expression.

## Variables

Named expressions (`Name`, `Expression`) that later variables and the main expression can use. Order matters: a variable may only reference ones defined before it.

## The request map

Every key/value pair in the request body is copied into `request`. The program decides what to honor, ignore or override. Reusing familiar names like `common_name` and `ttl` avoids breaking existing automation.

## Example pieces

```
has(request.ttl) && duration(request.ttl) < duration("4h")
validate_cn ? output : err
```

The second is the main expression of a program with variables such as `validate_cn`, `small_ttl`, `cert` and `output`.

## Warning

Advanced topic. OpenBao does limited to no validation beyond what the CEL program contains, so a permissive program issues whatever it permits.

## Checked

2026-11-04. Confirmed against the CEL concepts page: PKI and JWT use, main expression and ValidationOutput or pb.Auth, string or bool failure value, variable ordering, the request map and the validation warning. Removed the advice to test failure paths, which the page does not give.

Method: documentation only; no commands were run.
