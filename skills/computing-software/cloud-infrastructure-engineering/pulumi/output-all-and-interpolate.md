---
id: computing-software.cloud-infrastructure-engineering.pulumi.output-all-and-interpolate
name: output-all-and-interpolate
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-interpolate, output-all, pulumi-concat, output-string]
level: practitioner
status: docs-checked
description: "Combine multiple Pulumi outputs with pulumi.all, Output.all, interpolate, concat and JSON helpers, in TypeScript and Python (Output.format)."
sources:
  - https://www.pulumi.com/docs/iac/concepts/inputs-outputs/all/
  - https://www.pulumi.com/docs/iac/concepts/inputs-outputs/helpers/
  - https://www.pulumi.com/docs/iac/concepts/inputs-outputs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Output.all and interpolate

```typescript
const conn = pulumi.interpolate`postgres://${user}:${pw}@${db.endpoint}/app`;
const both = pulumi.all([db.address, db.port]).apply(([a, p]) => `${a}:${p}`);
const c2 = pulumi.concat("arn:aws:s3:::", bucket.bucket, "/*");
```
```python
conn = pulumi.Output.format("postgres://{0}:{1}@{2}/app", user, pw, db.endpoint)
both = pulumi.Output.all(db.address, db.port).apply(lambda a: f"{a[0]}:{a[1]}")
named = pulumi.Output.all(server=sql_server.name, db=database.name)   # keyword form gives an Output dictionary
```

`pulumi.interpolate` is a tagged template literal that accepts Outputs directly inside `${}`; it is the idiomatic TypeScript option. `pulumi.concat` joins strings and Outputs into one `Output<string>`. `Output.format` works like Python's `str.format()`.

## Gotchas
- Python f-strings with an Output fail with `Calling __str__ on an Output[T] is not supported`; use `Output.format`.
- Use `all` (not nested `apply`) when you need several Outputs at once; the `apply` page says `apply` is for a single Output.
- For JSON that contains Outputs (IAM policy documents, container definitions) use `pulumi.jsonStringify(obj)` in TypeScript or `pulumi.Output.json_dumps(obj)` in Python, which return an Output of the JSON string, instead of `JSON.stringify` on Outputs.

## Verify
If `conn` is exported, `pulumi stack output conn --show-secrets` shows the final string with values substituted after `pulumi up`.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Inputs and Outputs index and helpers pages (`pulumi.interpolate`, `pulumi.concat`, `Output.format`, `pulumi.jsonStringify`, `pulumi.Output.json_dumps`), the `all` page (TypeScript array form, Python positional and keyword forms), the apply page (`__str__` message, single-Output note) and the `pulumi stack output` reference (`--show-secrets`). Removed: the object-argument form of `pulumi.all`, the claims that interpolate preserves secretness and that `Output.all` fails as a whole, and the "confirm availability" hedges and duplicate note.
Method: documentation only; no commands were run.
