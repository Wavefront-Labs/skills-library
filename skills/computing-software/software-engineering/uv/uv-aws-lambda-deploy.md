---
id: computing-software.software-engineering.uv.uv-aws-lambda-deploy
name: uv-aws-lambda-deploy
category: computing-software
field: software-engineering
product: uv
tags: [uv, aws-lambda, serverless, docker, zip-archive, lambda-layer, workspaces, uv-export]
level: practitioner
status: docs-checked
description: "Package a uv project for AWS Lambda as a multi-stage Docker image, a zip archive or a dependency layer, including local workspace members."
sources: [https://docs.astral.sh/uv/guides/integration/aws-lambda/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy a uv project to AWS Lambda

Goal: ship a FastAPI/Mangum style app (handler `app.main.handler`) with locked dependencies. The page's example project uses dependencies `fastapi` and `mangum`; run locally with `uv run fastapi dev`.

## Method

### Docker image

Multi-stage: bundle dependencies into the task root in a builder stage, copy only that into the final image.

```dockerfile
FROM ghcr.io/astral-sh/uv:0.13.7 AS uv
FROM public.ecr.aws/lambda/python:3.13 AS builder
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt && \
    uv pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

FROM public.ecr.aws/lambda/python:3.13
COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}
COPY ./app ${LAMBDA_TASK_ROOT}/app
CMD ["app.main.handler"]
```

Bytecode speeds cold start; no installer metadata makes a deterministic layer; the dependency layer is reused until `uv.lock` changes. For ARM use the `python:3.13-arm64` base. Build with `uv lock` then `docker build -t fastapi-app .`, push to ECR, and create the function with `aws lambda create-function --package-type Image --code ImageUri=...`; update with `aws lambda update-function-code --image-uri ... --publish`.

Workspaces: after `uv init --lib library` and `uv add ./library`, add a second `RUN` that also bind-mounts `library` and runs `uv export --frozen --no-dev --no-editable` (without `--no-emit-workspace`) so third-party dependencies stay cached separately.

### Zip archive (limit 250 MB)

```console
$ uv export --frozen --no-dev --no-editable -o requirements.txt
$ uv pip install --no-installer-metadata --no-compile-bytecode --python-platform x86_64-manylinux2014 --python 3.13 --target packages -r requirements.txt
$ cd packages && zip -r ../package.zip . && cd ..
$ zip -r package.zip app
```

Use `aarch64-manylinux2014` for ARM. Create with `aws lambda create-function --runtime python3.13 --zip-file fileb://package.zip --handler app.main.handler --role ...`. The console defaults to `lambda_function.lambda_handler`, so set the handler.

### Layer

Install with `--prefix packages` instead of `--target`, then `mkdir python`, `cp -r packages/lib python/`, `zip -r layer_content.zip python` (`-X` for deterministic zips). Publish with `aws lambda publish-layer-version --layer-name dependencies-layer --zip-file fileb://layer_content.zip --compatible-runtimes python3.13 --compatible-architectures "x86_64"`, zip only `app` for the function, and attach the layer ARN using `aws lambda update-function-configuration --layers`.

## Verify

`aws lambda invoke --function-name myFunction --payload file://event.json --cli-binary-format raw-in-base64-out response.json` returns `StatusCode` 200; the page's `response.json` body is `"Hello, world!"`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/aws-lambda). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
