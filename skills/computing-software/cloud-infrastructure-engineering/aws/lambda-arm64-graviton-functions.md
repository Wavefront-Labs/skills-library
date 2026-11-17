---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-arm64-graviton-functions
name: lambda-arm64-graviton-functions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, lambda-arm64, graviton, architectures, native-dependencies]
level: practitioner
status: docs-checked
description: "Move Lambda functions to arm64 (Graviton): build native dependencies for aarch64, multi-arch layers and images, compare cost and performance, and roll out by alias."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/foundation-arch.html", "https://docs.aws.amazon.com/lambda/latest/api/API_UpdateFunctionConfiguration.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuring-alias-routing.html", "https://aws.amazon.com/lambda/pricing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# arm64 (Graviton) Lambda functions

## 1. Switch
The architecture is not a field of `UpdateFunctionConfiguration`; it is set at create time or changed together
with the code (`update-function-code --architectures`):
```bash
aws lambda update-function-code --function-name orders --zip-file fileb://build-arm64.zip --architectures arm64 --publish
```
Valid values are `x86_64` (default) and `arm64`. AWS describes arm64 (Graviton2) as giving significantly better
price and performance for many workloads; check the Lambda pricing page for the per-Region duration rates and
measure your own function.

## 2. Native dependencies
Pure Python/Node/Java code moves as-is. Compiled extensions must be aarch64 builds:
```bash
pip install -r requirements.txt --platform manylinux2014_aarch64 --only-binary=:all: \
  --implementation cp --python-version 3.12 -t build/
```
Go/Rust: build for linux/arm64 and deploy on a custom runtime (`provided.al2023`).
Any function code you uploaded, every layer, every extension and any container image must be rebuilt or
checked for arm64.

## 3. Layers and images
- Check each layer for compatibility with the function's architecture; replace an incompatible layer version.
- Container images: create a new image that is compatible with the function's architecture.
- Third-party extensions (monitoring agents) need arm64 versions.

## 4. Roll out
AWS recommends staging: publish a version on arm64 and use alias routing to split traffic between the x86 and
arm64 versions (10% then 100%), comparing `Duration`, `Errors` and cost; tune memory again with Lambda Power
Tuning because the optimum can move.

## Verify
- [ ] `aws lambda get-function-configuration --function-name orders --query Architectures` returns `["arm64"]`.
- [ ] No `ImportModuleError` / `exec format error` in logs after the shift.

## Checked
Date 2026-10-23. Lambda Developer Guide (instruction set architecture page) and the UpdateFunctionConfiguration API
reference. Confirmed: architectures x86_64 and arm64 (Graviton2), migration steps and alias-routing staging,
layers, extensions and images must each be arm64 compatible, `UpdateFunctionConfiguration` has no
`Architectures` request field (the old example using it was wrong), `provided.al2023` runtime identifier.
Removed the unconfirmed percentage price claim and the unconfirmed `--target` triple.
Method: documentation only; no commands were run.
