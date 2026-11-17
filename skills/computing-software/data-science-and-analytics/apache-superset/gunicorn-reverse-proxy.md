---
id: computing-software.data-science-and-analytics.apache-superset.gunicorn-reverse-proxy
name: gunicorn-reverse-proxy
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [gunicorn, reverse-proxy, proxy-fix, health-check, load-balancer]
level: practitioner
status: docs-checked
description: "Run Superset under Gunicorn behind a load balancer: ENABLE_PROXY_FIX, the /health endpoint, documented worker flags and the app root for sub-paths."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/configuring-superset.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve Superset correctly behind a proxy or load balancer.

Run the web server with Gunicorn, not `superset run` or `flask run` (development only). The docs recommend Gunicorn in async mode and show this setup as known to work in production:

```bash
gunicorn -w 10 -k gevent --worker-connections 1000 --timeout 120 \
  -b 0.0.0.0:6666 --limit-request-line 0 --limit-request-field_size 0 \
  --statsd-host localhost:8125 "superset.app:create_app()"
```

- The BigQuery Python SDK is not compatible with gevent: with a BigQuery datasource use a Gunicorn worker type other than gevent.
- If you do not use Gunicorn, consider `COMPRESS_REGISTER = False` to disable flask-compress.
- TLS can be offloaded at a load balancer or reverse proxy (for example nginx); Celery workers taking Alerts and Reports screenshots can then reach Superset over a `http://` URL behind the ingress. SSL can also be configured in Gunicorn with the official Docker image.

Behind a proxy that inserts `X-Forwarded-For` and `X-Forwarded-Proto`, set `ENABLE_PROXY_FIX = True` in `superset_config.py` so Superset uses those headers. If the proxy provides SSL, an explicit `X-Forwarded-Proto` may be needed (Apache: `RequestHeader set X-Forwarded-Proto "https"`).

Health checks: `/health` returns a 200 response containing "OK" while the web server is running. The health blueprint routes (`/health`, `/healthcheck`, `/ping`, `/version`) are exempt from forced password change.

Sub-path hosting (marked BETA): the prefix must start with `/` (for example `/analytics`) and is set by one of: `superset_app_root` passed to `create_app` (via `FLASK_APP` or `flask --app`), the `SUPERSET_APP_ROOT` environment variable, or the `APPLICATION_ROOT` config. For Swagger UI behind a prefix also set `FAB_API_SWAGGER_UI_SUPERSET_APP_ROOT = True` (needs `FAB_API_SWAGGER_UI`).

## Checked

2026-11-08. Confirmed against the Configuring Superset page, sections "Running on a WSGI HTTP Server", "HTTPS Configuration", "Configuration Behind a Load Balancer" and "Configuring the application root" (rest of the page not read for this skill). Removed: the `--bind`/`--workers` example (replaced by the documented one), the claim that missing ENABLE_PROXY_FIX gives wrong OAuth redirect URIs, advice to match proxy timeouts, and the shared database and cache requirement for several instances, none stated there.
Method: documentation only; no commands were run.
