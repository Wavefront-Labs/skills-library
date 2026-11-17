---
id: computing-software.cloud-infrastructure-engineering.pulumi.automation-api-inline
name: automation-api-inline
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, inline-program, inline-source, automation-api-inline, pulumi-run-inline]
level: practitioner
status: docs-checked
description: "Run an inline Pulumi program function through the Automation API without Pulumi.yaml files, using InlineProgramArgs and LocalWorkspace."
sources:
  - https://www.pulumi.com/docs/iac/automation-api/
  - https://www.pulumi.com/docs/iac/automation-api/getting-started-automation-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inline programs

The infrastructure is a function inside your application; no separate package on disk with its own file and `Pulumi.yaml` is needed. Inline programs can be authored in the same file as the Automation API program or imported from another package.

```typescript
import * as aws from "@pulumi/aws";
import { LocalWorkspace, InlineProgramArgs } from "@pulumi/pulumi/automation";

const program = async () => {
  const bucket = new aws.s3.Bucket("b");
  return { name: bucket.bucket };       // returned object = stack outputs
};
const args: InlineProgramArgs = { stackName: "dev", projectName: "inline", program };
const stack = await LocalWorkspace.createOrSelectStack(args);
await stack.setConfig("aws:region", { value: "us-west-2" });
const r = await stack.up({ onOutput: console.info });
```
```python
def program():
    b = aws.s3.Bucket("b")
    pulumi.export("name", b.bucket)
stack = auto.create_or_select_stack(stack_name="dev", project_name="inline", program=program)
```

The `up` result includes the stack outputs and a summary of the changes, so the calling program can branch on them.

## Gotchas
- The program's lifecycle must be fully contained within the function, callback or closure passed as the inline program; doing work outside it is unsafe and can lead to unpredictable behaviour.
- The Pulumi CLI must be available at runtime (on `PATH`, or installed programmatically by the TypeScript, Python, Go and .NET SDKs; the Java SDK cannot install it).
- Provider plugins from the Pulumi Registry are downloaded automatically before an operation. Call `installPlugin` only to pin a plugin version, pre-fetch (for example air-gapped), or for local or parameterized packages.
- The `Workspace` holds a single Pulumi project, a program and one or more stacks.

## Verify
`up` returns the outputs including `name`.

## Checked

Method: docs-checked 2026-11-09 against the Pulumi Automation API overview and Using Automation API pages. Removed unconfirmed claims: plugins must be installed explicitly, parallel-stack limits in Node, stack traces in onOutput, and the backend-listing check.
