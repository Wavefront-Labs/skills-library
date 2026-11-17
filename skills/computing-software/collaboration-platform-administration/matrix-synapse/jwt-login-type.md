---
id: computing-software.collaboration-platform-administration.matrix-synapse.jwt-login-type
name: jwt-login-type
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, jwt, json-web-token, login, org-matrix-login-jwt, jwt-config, authlib, sso]
level: advanced
status: docs-checked
description: "Enable the org.matrix.login.jwt login type with jwt_config, know which JWT claims are required or validated, and test with an HS256 token generated locally using authlib."
sources:
  - https://element-hq.github.io/synapse/latest/jwt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Synapse has a non-standard login type for JSON Web Tokens. A client calls `/login` with:

```json
{
  "type": "org.matrix.login.jwt",
  "token": "<jwt>"
}
```

The usual extra login fields such as `device_id` and `initial_device_display_name` may be included. Claim rules:

- A claim carrying the localpart of the user ID is required. By default it is `sub`; a custom claim can be set in config.
- `exp`, `nbf` and `iat` are optional but validated if present.
- `iss` and `aud` are optional but required and validated when configured. Sending an audience when none is configured makes validation fail.

An invalid token must get `403 Forbidden` with errcode `M_FORBIDDEN`.

**Preparing Synapse.** It uses the Authlib library. The matrix.org Docker images and Debian packages include it; for a virtualenv, install the jwt extra for Synapse. Then add a `jwt_config` option to the config (see the configuration manual for more settings).

**Testing locally with a shared secret.** The docs' example uses HS256:

```yaml
jwt_config:
    enabled: true
    secret: "my-secret-token"
    algorithm: "HS256"
```

Generate a token with Authlib, making sure the secret and the algorithm in `header` match the config:

```python
from authlib.jose import jwt

header = {"alg": "HS256"}
payload = {"sub": "user1", "aud": ["audience"]}
secret = "my-secret-token"
result = jwt.encode(header, payload, secret)
print(result.decode("ascii"))
```

Check that `GET /_matrix/client/r0/login` lists `org.matrix.login.jwt`, then POST the token to `/login`. A successful response returns `access_token`, `device_id`, `home_server` and `user_id`. Note the sample payload includes an `aud`, so only use it when `jwt_config` also sets the audience; otherwise omit it.

## Checked

2026-11-04. Confirmed against the Synapse JWT Login Type page: login body, claim rules, 403 M_FORBIDDEN, Authlib and jwt extra, jwt_config HS256 example, token snippet, login types check, response fields. Nothing removed.
Method: documentation only; no commands were run.
