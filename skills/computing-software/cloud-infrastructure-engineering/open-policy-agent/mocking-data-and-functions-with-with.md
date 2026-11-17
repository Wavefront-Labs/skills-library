---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.mocking-data-and-functions-with-with
name: mocking-data-and-functions-with-with
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [mocking, with-keyword, stubs, builtin-replacement, rego-tests]
level: advanced
status: docs-checked
description: "Replace input, data, rules and built-in functions such as io.jwt.decode_verify in Rego tests using with, and the arity and internal-function limits that apply."
sources:
  - https://www.openpolicyagent.org/docs/policy-testing
  - https://www.openpolicyagent.org/docs/policy-language
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: isolate a rule from its dependencies in a test.

`with` can replace the input, base or virtual documents under `data`, rules, and functions (built-in or user-defined):

```rego
test_allow_with_data if {
    authz.allow with input as {"user": "alice", "role": "admin"}
        with data.policies as [{"name": "test_policy"}]
        with data.roles as {"admin": ["alice"]}
}

test_replace_rule if {
    authz.allow1 with authz.allow2 as true
}
```

Replace a built-in with a mock function:

```rego
mock_decode_verify("my-jwt", _) := [true, {}, {}]
mock_decode_verify(x, _) := [false, {}, {}] if x != "my-jwt"

test_allow if {
    authz.allow with input.headers["x-token"] as "my-jwt"
        with data.jwks.cert as "mock-cert"
        with io.jwt.decode_verify as mock_decode_verify
}
```

A function can also be replaced by a plain value, for example `with io.jwt.decode_verify as [true, {}, {}]`; every call then returns that value whatever the arguments.

Constraints:
- `internal.*`, `rego.metadata.*`, `eq` and relations such as `walk` cannot be replaced.
- The replacement must have the same arity as the original.
- A replacement may call the function it replaces; that call reaches the original, not itself, so there is no recursion.
- The replacement value can be a plain value, a reference to another function (built-in or user-defined), or a reference to a rule used as the value. The types must be compatible. Function replacement does not change how the function arguments are evaluated.

Mock only the boundary (token verification, external data), not the rule you are testing.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Testing page, section Data and Function Mocking (base and virtual documents can be replaced; internal.*, rego.metadata.*, eq and relations such as walk cannot; same arity; replacements may call the original without recursion) and the Policy Language page, section With Keyword (valid replacement values for a function target, type compatibility, new scope per replacement call, arguments unaffected). Replaced an unsupported bullet about built-in-for-non-built-in replacement with the documented list of replacement kinds; added the Policy Language page to sources.

Method: documentation only; no commands were run.
