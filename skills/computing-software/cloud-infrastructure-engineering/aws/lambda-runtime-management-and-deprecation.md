---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-runtime-management-and-deprecation
name: lambda-runtime-management-and-deprecation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, runtime-management, runtime-deprecation, runtime-update, runtime-version, os-only-runtime, upgrades]
level: practitioner
status: docs-checked
description: "Keep Lambda runtimes current: runtime update modes (Auto, Function update, Manual), pinning a runtime version, runtime identifiers vs versions, and finding functions to upgrade."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html", "https://docs.aws.amazon.com/lambda/latest/dg/runtime-management-configure-settings.html", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda runtime management and deprecation
Two different things change underneath a function:
- **Runtime version** (patches to a runtime such as the one behind `python3.12`) is handled by runtime
  management controls. Version numbers use Lambda's own numbering and are not always sequential.
- **Runtime identifier** (`python3.9` to `python3.14`, `nodejs24.x`) corresponds to a major language
  release; you change it yourself, and old identifiers get deprecated.

## 1. Runtime update modes
Set per function version (`$LATEST` or a published version):
- **Auto** (default): Lambda applies new runtime versions automatically with a two-phase rollout: first
  whenever you create or update the function, then to functions still on Auto.
- **Function update**: the latest runtime version is applied when you update the function, so patches
  go through your pipeline; you must update functions regularly to stay current.
- **Manual**: you specify a runtime version ARN and the function uses it indefinitely. Use it only
  temporarily to roll back from an incompatible patch.
```bash
aws lambda put-runtime-management-config --function-name orders --update-runtime-on Manual \
  --runtime-version-arn arn:aws:lambda:<REGION>::runtime:<RUNTIME_VERSION_ID>
```
Find the ARN in the console or the `INIT_START` log line. The ARN for the same version number can differ
between Regions and architectures. Pinned functions do not receive runtime updates.
Rollout is gradual across Regions, so functions deployed at different times or Regions can run different versions.

## 2. Deprecation lifecycle
Each runtime identifier has a published deprecation schedule on the Lambda runtimes page. Lambda blocks creating
and then updating functions on a deprecated runtime shortly after the deprecation date (the API reference says
Lambda blocks creating new functions and updating existing ones shortly after each runtime is deprecated). Check
the runtimes page for the exact dates of each identifier you use.

## 3. Find what to upgrade
```bash
for r in python3.9 nodejs18.x java8 go1.x; do
  aws lambda list-functions --function-version ALL \
    --query "Functions[?Runtime=='$r'].[FunctionName,Runtime]" --output text
done
```
Replace the identifiers with those flagged on the runtimes page.

## 4. Upgrading
Change the identifier in your infrastructure code, rebuild native dependencies for the new runtime, run tests,
and deploy through an alias canary. OS-only custom runtimes use `provided.al2023`.

## Gotchas
- Container image functions are not updated by runtime management: rebuild from the updated base image and redeploy.
- Customers who need identical runtime versions across environments should deploy container images; Manual mode
  is a temporary mitigation, not a consistency tool.

## Verify
- [ ] No functions on identifiers with a deprecation date within your upgrade window.
- [ ] Production functions use `Auto` or `Function update`; none pinned to `Manual` longer than needed.

## Checked
Date 2026-10-23. Lambda Developer Guide runtime update, runtime management settings pages and the UpdateFunctionConfiguration API
reference (runtime list). Confirmed: three update modes and defaults, two-phase rollout, per-version setting,
`put-runtime-management-config` flags, INIT_START ARN, ARN varies by Region and architecture, container image
behaviour, `provided.al2023` identifier, current identifiers such as `python3.14`, `nodejs24.x`. Removed unconfirmed
claims: the specific "30 and 60 day" block intervals, AWS Health event name, Trusted Advisor and AWS Config
queries, and the `get-runtime-management-config` command.
Method: documentation only; no commands were run.
