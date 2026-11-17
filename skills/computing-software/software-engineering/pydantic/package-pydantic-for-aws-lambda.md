---
id: computing-software.software-engineering.pydantic.package-pydantic-for-aws-lambda
name: package-pydantic-for-aws-lambda
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-aws-lambda, aws-lambda, manylinux, pydantic-core, email-validator, serverless, lambda-layers]
level: practitioner
status: docs-checked
description: "Install Pydantic for AWS Lambda with pip platform flags, and fix the missing pydantic_core module and email-validator package metadata errors."
sources:
  - https://docs.pydantic.dev/latest/integrations/aws_lambda/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: ship Pydantic in a Lambda `.zip` or Layer so the compiled `pydantic_core` matches the Lambda runtime.

## Install for the Lambda platform
`pip` installs wheels compiled for your local platform, which may not match Lambda. Use:
```bash
pip install \
    --platform manylinux2014_x86_64 \
    --target=<your_package_dir> \
    --implementation cp \
    --python-version 3.10 \
    --only-binary=:all: \
    --upgrade pydantic
```
- `--platform`: match your Lambda runtime (`manylinux2014_x86_64` or `manylinux2014_aarch64` at the time of the page; may change with a future major release).
- `--target`: output dir, often `python` for Lambda Layers.
- `--python-version`: must be compatible with the Lambda runtime.
- `--only-binary=:all:` installs pre-built wheels.

Approaches: `.zip` archive, Lambda Layers (good for sharing across functions), or a container image (dependency management is more straightforward).

## Error: no module named `pydantic_core._pydantic_core`
Indicates an incorrect install. Debug before the failing import:
1. List the compiled library and stubs:
```python
from importlib.metadata import files
print([file for file in files('pydantic-core') if file.name.startswith('_pydantic_core')])
```
Expect two files, e.g. `pydantic_core/_pydantic_core.pyi` and `pydantic_core/_pydantic_core.cpython-312-x86_64-linux-gnu.so` (`.so` or `.pyd`).
2. Compare with the runtime:
```python
import sysconfig
print(sysconfig.get_config_var("EXT_SUFFIX"))
```
The suffix (e.g. `.cpython-312-x86_64-linux-gnu.so`) must match the library file. If not, the build installed the wrong native code. Likely causes: OS/CPU mismatch (fix `--platform` or build inside a matching Linux Docker container) or Python version mismatch such as `cpython-310` vs `cpython-312` (fix `--python-version`).

## Error: no package metadata found for `email-validator`
Pydantic uses `importlib.metadata` version to check the installed `email-validator`. Fixes:
- Serverless framework with `serverless-python-requirements`: it strips metadata to shrink packages; set `slim: false`:
```yaml
pythonRequirements:
    dockerizePip: non-linux
    slim: false
    fileName: requirements.txt
```
- `.zip` archive: include the `dist-info` directory of `email-validator`.

## More
The page points to pydantic issue 6557 for further install problems and to a Pydantic blog post on validating Lambda `event` and `context` data.

## Checked

Checked 2026-11-07. Compared every claim with the AWS Lambda integration page (integrations/aws_lambda.md): the three packaging approaches, the `pip install` flags and their meanings, the platform values, the `pydantic_core._pydantic_core` diagnosis steps and likely causes, the `email-validator` metadata fix with `slim: false` and the `dist-info` directory, and the pointers to issue 6557 and the blog post. All confirmed; nothing removed.

Method: documentation only; no commands were run.
