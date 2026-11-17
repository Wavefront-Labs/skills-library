---
id: computing-software.cloud-infrastructure-engineering.pulumi.inputs-outputs-apply
name: inputs-outputs-apply
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, output-apply, pulumi-output, unwrap-output, apply]
level: practitioner
status: docs-checked
description: "Work with Pulumi Input and Output values: apply, lifting, unknown values at preview, and why you cannot use outputs as plain strings."
sources:
  - https://www.pulumi.com/docs/iac/concepts/inputs-outputs/
  - https://www.pulumi.com/docs/iac/concepts/inputs-outputs/apply/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inputs and outputs: apply

An `Output<T>` is an asynchronous value that is only known after a resource has finished provisioning. Resource properties are Outputs; inputs accept plain values or Outputs.

```typescript
const url = bucket.bucket.apply(name => `https://${name}.s3.amazonaws.com`); // Output<string>
const arn = bucket.arn;                // pass directly into other resources
const first = vm.networkInterfaces[0].apply(n => n.privateIp);
const lifted = vm.tags.owner;          // lifting: nested access without apply
```
```python
url = bucket.bucket.apply(lambda n: f"https://{n}.s3.amazonaws.com")
```

## Gotchas
- Resources created inside `apply` do not appear in `pulumi preview` unless the value is already known, so the preview can differ from `pulumi up`. Create resources outside `apply`.
- Stack outputs (`export`, `pulumi.export()`) cannot be created inside `apply`; export the Output directly.
- `console.log(output)` prints an Output object (TypeScript) rather than the value; to print the value use `output.apply(v => console.log(v))`.
- Do not concatenate or format an Output as a plain string. Python reports `Calling __str__ on an Output[T] is not supported`; use `apply`, `pulumi.interpolate` (TypeScript) or `Output.format` (Python).
- Lifting works for most nested property and array access, but if an Output resolves to `undefined`, lifted access returns an Output that also resolves to `undefined`; use `apply` with a null check when you need to detect a missing value.
- `apply` is for one Output; combine several with `all` (see output-all-and-interpolate).

## Verify
After `pulumi up`, if the Output is exported as `url`, `pulumi stack output url` shows the resolved string.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Inputs and Outputs page (lifting, behaviour when an Output resolves to undefined) and the apply page (resources inside apply and preview, exports inside apply, printing Outputs, the Python `__str__` message, `output.apply(...)` with `console.log`) and the `pulumi stack output` reference. Removed: the unverified claims that apply on a secret yields a secret, the `Output<string|undefined>` lifted type, `pulumi.log.info`, the `[output]` / `[unknown]` preview placeholders and the `${out}` "throws" wording.
Method: documentation only; no commands were run.
