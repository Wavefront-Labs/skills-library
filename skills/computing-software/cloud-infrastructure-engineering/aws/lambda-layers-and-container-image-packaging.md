---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-layers-and-container-image-packaging
name: lambda-layers-and-container-image-packaging
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, lambda-layers, container-image-lambda, lambda-packaging, deployment-package, ecr, native-dependencies]
level: practitioner
status: docs-checked
description: "Package Lambda code: zip limits, building native dependencies for the right arch, layers (limits, versions, sharing), and container images and their size limit."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html", "https://docs.aws.amazon.com/lambda/latest/dg/foundation-arch.html", "https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda packaging: zip, layers, container images

## 1. Limits that decide the format
| | Zip (+ layers) | Container image |
|---|---|---|
| Size | 50 MB zipped when uploaded through the API/SDK (use S3 for larger zips); **250 MB unzipped**, including layers and custom runtimes | **10 GB** maximum uncompressed image size including all layers |
| Source | S3 or direct upload | Amazon ECR (see the ECR quotas page for storage) |
| Layers | at most 5 per function | n/a for the image package |
Over the 250 MB unzipped limit (ML libraries, headless Chrome), move to a container image.
Other limits from the quotas page: environment variables 4 KB in aggregate, `/tmp` 512 MB to 10,240 MB.
Code storage for uploaded zip functions and layers is 300 GB per Region (not increasable; use self-managed S3
code storage beyond it), counting every function and layer version.

## 2. Build native deps for the Lambda environment
```bash
# Python for arm64 Lambda from any machine:
pip install -r requirements.txt --platform manylinux2014_aarch64 --only-binary=:all: \
  --python-version 3.12 --implementation cp --target package/
cd package && zip -qr ../function.zip . && cd .. && zip -g function.zip app.py
```
A zip that you upload must contain code compatible with the function's architecture, and so must every layer;
an architecture mismatch shows up as import errors at run time.

## 3. Layers
- Check every layer for architecture compatibility before attaching it.
- Layers are versioned; functions reference a layer version ARN, so updating a layer means updating each
  function to the new version ARN.
- When code signing is enabled on a function, its layers must be signed by an allowed profile too.
- Use layers for genuinely shared runtime bits (extensions, shared libraries), not as a dependency manager for
  every function. Extensions for zip functions are deployed as layers.

## 4. Container images
- Create a new image compatible with the function's architecture; for runtime updates, rebuild from the updated
  base image and redeploy (Lambda publishes each runtime version as a container image).
- Runtime updates are not applied to container-based functions automatically.

## Gotchas
- Layers and the function share the 250 MB unzipped limit.
- Code signing does not apply to container image functions (see the code signing skill).

## Verify
- [ ] A cold invocation imports all native modules without errors on the target architecture.
- [ ] `get-function-configuration` shows the intended layer versions or image digest.
- [ ] Package size has headroom under the limit (CI check).

## Checked
Date 2026-10-23. Lambda Developer Guide quotas, architecture and runtime update pages. Confirmed: 50 MB zipped upload,
250 MB unzipped including layers, 10 GB image size, 5 layers, 4 KB environment variables, 300 GB code storage,
architecture compatibility of code, layers, extensions and images, runtime updates for container functions need
a rebuilt image. Removed
unconfirmed layer path conventions, the Runtime Interface Emulator walkthrough, base image tags, the
cross-account ECR statement, and the "image functions cannot use layers" and "package type cannot be switched"
claims.
Method: documentation only; no commands were run.
