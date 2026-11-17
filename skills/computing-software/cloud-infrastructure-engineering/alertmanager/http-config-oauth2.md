---
id: computing-software.cloud-infrastructure-engineering.alertmanager.http-config-oauth2
name: http-config-oauth2
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, oauth2, client-credentials, http-config]
level: advanced
status: docs-checked
description: "OAuth 2.0 client credentials in Alertmanager http_config: client_id, client_secret, scopes, token_url, endpoint_params and proxy settings."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# oauth2 in http_config

The `oauth2` block provides OAuth 2.0 authentication using the client credentials grant type. Alertmanager fetches an access token from the specified endpoint using the given client id and secret.

```yaml
http_config:
  oauth2:
    client_id: my-client
    client_secret_file: /path/to/secret
    scopes: [alerts.write]
    token_url: https://auth.example.org/oauth/token
    endpoint_params:
      audience: https://api.example.org
```

Fields:
- `client_id`: required string.
- `client_secret`, or `client_secret_file` (mutually exclusive with `client_secret`).
- `scopes`: list of scopes for the token request.
- `token_url`: URL to fetch the token from.
- `endpoint_params`: optional parameters appended to the token URL.
- `tls_config`: TLS settings for the token request.
- `proxy_url`, `no_proxy`, `proxy_from_environment` (default `false`), `proxy_connect_header`: same meaning as in `http_config`, applied to the token request.

Constraint: `oauth2` cannot be used at the same time as `basic_auth` or `authorization` in the same `http_config`.

Because `http_config` is available on receivers such as webhook, Slack, PagerDuty and incident.io, OAuth 2.0 can be set per integration or once in `global.http_config`.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference (http_config and oauth2 sections): client credentials grant, client_id, client_secret and client_secret_file (mutually exclusive), scopes, token_url, endpoint_params, tls_config, proxy_url, no_proxy, proxy_from_environment (default false), proxy_connect_header, the rule that oauth2 cannot be used with basic_auth or authorization, and http_config on Slack, PagerDuty, webhook and incident.io receivers defaulting to global.http_config. The YAML values (my-client, alerts.write, example.org URLs) are placeholders.

Method: documentation only; no commands were run.
