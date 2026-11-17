---
id: computing-software.data-engineering.prefect.secret-blocks
name: secret-blocks
category: computing-software
field: data-engineering
product: prefect
tags: [secrets, secret-block, credentials, blocks, encryption]
level: intro
status: docs-checked
description: "Store and load sensitive strings in Prefect with the Secret block, update them with overwrite, and use credential blocks such as AwsCredentials."
sources:
  - https://docs.prefect.io/v3/how-to-guides/configuration/store-secrets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep credentials out of code.

Create and save a Secret block:

```python
from prefect.blocks.system import Secret

secret = Secret(value="my-secret-value")
secret.save("surprise-party")
```

Load it in a flow and read the value with `.get()`:

```python
from prefect import flow
from prefect.blocks.system import Secret

@flow
def my_flow():
    secret = Secret.load("surprise-party")
    print(secret.get())
```

- Update by saving a new value under the same name with `overwrite=True`.
- Secret values are encrypted at rest in the Prefect backend.
- Secret blocks can also be created and updated in the UI.

Common configuration: Prefect ships blocks for it, many in integration libraries. For example `AwsCredentials` from `prefect-aws` (`pip install prefect-aws`): save it with `.save(name)`, load with `.load(name)` in a flow, and call `get_boto3_session()` to build a boto3 session.

Variables are not encrypted, so keep sensitive data in Secret or credential blocks, never in variables.

The page does not compare secrets with environment variables.

## Checked
2026-11-08. Confirmed against the store-secrets how-to: Secret block save, load and get, encryption at rest, overwrite=True, UI creation, AwsCredentials from prefect-aws with get_boto3_session. The not-encrypted statement for variables is confirmed on the Variables concept page. Nothing removed.
Method: documentation only; no commands were run.
