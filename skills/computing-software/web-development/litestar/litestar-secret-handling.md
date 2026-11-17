---
id: computing-software.web-development.litestar.litestar-secret-handling
name: litestar-secret-handling
category: computing-software
field: web-development
product: litestar
tags: [litestar, security, secret, secretstring, secretbytes, header-parameter, compare-digest]
level: practitioner
status: docs-checked
description: "Use Litestar SecretString and SecretBytes to accept secrets in headers and request bodies, and compare them with secrets.compare_digest."
sources: [https://docs.litestar.dev/latest/usage/security/secret-datastructures.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar secret data structures

Goal: carry sensitive values through handlers without exposing them accidentally.

## Method

`SecretString` and `SecretBytes` (in `litestar.datastructures.secret_values`) are containers for sensitive data.

Secret header parameter, compared in constant time:

```python
from secrets import compare_digest
from typing import Annotated
from litestar import get
from litestar.datastructures.secret_values import SecretString
from litestar.exceptions import NotAuthorizedException
from litestar.params import HeaderParameter

@get(sync_to_thread=False)
def get_handler(secret: Annotated[SecretString, HeaderParameter(name="x-secret")]) -> Sensitive:
    if not compare_digest(secret.get_secret(), SECRET_VALUE):
        raise NotAuthorizedException
    return Sensitive(value="sensitive data")
```

Secret in a body: use a `SecretString` field on a data structure:

```python
@dataclass
class Sensitive:
    value: SecretString

@post(sync_to_thread=False)
def post_handler(data: JSONBody[Sensitive]) -> Sensitive:
    return data
```

Use `.get_secret()` to read the underlying value.

## Gotchas

- These types help move secrets through the framework; storing and comparing them is your job. Keep secrets in environment variables, secret management services or encrypted databases.
- Compare with `secrets.compare_digest` or similar to mitigate timing attacks.
- `ASGIConnection.headers` stores headers exactly as parsed from the ASGI message; do not log or otherwise expose them.
- Add access controls and logging to monitor who can access sensitive information.

## Checked

2026-11-07. Read the full cited page(s) (usage/security/secret-datastructures.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
