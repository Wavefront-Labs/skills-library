---
id: computing-software.data-science-and-analytics.apache-superset.cors-and-talisman
name: cors-and-talisman
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [cors, talisman, csp, frame-ancestors, csrf]
level: advanced
status: docs-checked
description: "Configure Superset network security headers: ENABLE_CORS and CORS_OPTIONS, Talisman content security policy with frame-ancestors, CSRF exemptions and middleware."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/networking-settings.mdx
  - https://github.com/apache/superset/blob/master/docs/admin_docs/security/securing_superset.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: allow the cross-origin and framing access you need and no more. All keys go in `superset_config.py`.

CORS:
- `ENABLE_CORS`: must be `True` to enable CORS.
- `CORS_OPTIONS`: options passed to Flask-CORS (see the Flask-CORS documentation for the keys).
- In Superset versions before 5.x you must install flask-cors yourself (`pip install flask-cors`).

Talisman (security headers): Superset bundles flask-talisman. In Superset 4.0 and later Talisman is disabled by default (`TALISMAN_ENABLED = False`); enable it explicitly, with a strict content security policy, for `TALISMAN_CONFIG` to take effect.

Embedding with a public direct link: copy the entire `TALISMAN_CONFIG` section from Superset's `config.py` into `superset_config.py` and add a `frame-ancestors` entry listing the sites allowed to embed, for example:
```python
TALISMAN_ENABLED = True
TALISMAN_CONFIG = {
    "content_security_policy": {
        # ... rest of the default policy ...
        "frame-ancestors": ["*.my-domain.com", "*.another-domain.com"],
    },
}
```
Restart Superset afterwards. Anyone who knows a public dashboard link can access it. For SSO embedding the docs also say to set `SESSION_COOKIE_SAMESITE = 'None'` with `SESSION_COOKIE_SECURE = True`; the security guide notes that 'None' disables some built-in CSRF protection, so use it only when iframe embedding is necessary (the recommended default is 'Lax').

Other settings on the networking page:
- `WTF_CSRF_EXEMPT_LIST`: exempt endpoints from CSRF (flask-wtf), for example a custom auth postback endpoint.
- `ADDITIONAL_MIDDLEWARE`: list of your extra middleware classes, for example to map a proxy header to Gunicorn's REMOTE_USER for `AUTH_REMOTE_USER` behind nginx.
- `SSH_TUNNELING` feature flag and `SSH_TUNNEL_LOCAL_BIND_ADDRESS`.
- Domain sharding (`SUPERSET_WEBSERVER_DOMAINS`) is deprecated as of 5.0.0 and slated for removal in 6.0.0; enable HTTP2 instead.

## Checked

Confirmed against the Superset docs pages "Network and Security Settings" and "Securing Superset": the CORS keys and Flask-CORS note, Talisman default state from 4.0, the frame-ancestors procedure, CSRF, middleware, SSH tunnelling and domain sharding notes. Removed the sample CORS_OPTIONS dictionary, the advice to avoid `*` origins, and the map tile connect-src hint, which these pages do not state.

Method: docs-only read of cited pages, 2026-11-08
