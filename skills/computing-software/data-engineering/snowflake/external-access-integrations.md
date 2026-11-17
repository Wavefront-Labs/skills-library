---
id: computing-software.data-engineering.snowflake.external-access-integrations
name: external-access-integrations
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, external-access-integration, network-rule-egress, snowflake-secrets, api-ingestion, python-udf-network, oauth-secret, egress-control]
level: advanced
status: docs-checked
description: "Let Snowflake Python UDFs/procedures call external APIs: egress network rules, secrets (generic string/OAuth), external access integrations, granting usage, and code use."
sources:
  - https://docs.snowflake.com/en/developer-guide/external-network-access/external-network-access-overview
  - https://docs.snowflake.com/en/developer-guide/external-network-access/creating-using-external-network-access
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# External access integrations

**Goal:** a Snowflake procedure or UDF can call a specific external endpoint (REST API, SaaS), with credentials held as Snowflake secrets and egress restricted to approved hosts.

## 1. Network rule (egress allow-list)
```sql
create or replace network rule ops.net.acme_api_egress
  mode = egress type = host_port
  value_list = ('api.acme-vendor.com:443');
```

## 2. Secret
```sql
create or replace secret ops.secrets.acme_api_key type = generic_string secret_string = '<token>';
-- or an OAuth2 secret: create secret ... type = oauth2 api_authentication = <security integration> ...
```

## 3. Integration
```sql
create or replace external access integration acme_api_access
  allowed_network_rules = (ops.net.acme_api_egress)
  allowed_authentication_secrets = (ops.secrets.acme_api_key)
  enabled = true;
grant usage on integration acme_api_access to role ingest_role;
-- also grant the privileges the role needs on the secret (see the external network access pages)
```

## 4. Use it
```sql
create or replace procedure ingest.pull_acme(since string)
returns string language python runtime_version = '3.12'
packages = ('snowflake-snowpark-python', 'requests')
handler = 'run'
external_access_integrations = (acme_api_access)
secrets = ('token' = ops.secrets.acme_api_key)
as $$
import _snowflake, requests
def run(session, since):
    token = ...  # read the secret through the _snowflake secret-access function for its type (see the external network access pages)
    rows, url = [], f"https://api.acme-vendor.com/v1/orders?since={since}"
    while url:
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=30)
        r.raise_for_status()
        body = r.json(); rows += body["data"]; url = body.get("next")
    # persist `rows` with the Snowpark session (see the Snowpark docs)
    return f"{len(rows)} rows"
$$;
```

## Notes
- Respect API rate limits (backoff) since tasks can run concurrently.
- For big extracts, a dedicated EL tool may be more appropriate than a procedure.

## Verify
- [ ] Procedure succeeds with the integration; the same code without it fails to connect.
- [ ] Secret value never appears in query history or logs.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the external network access pages and CREATE EXTERNAL ACCESS INTEGRATION / CREATE SECRET references: network rule MODE = EGRESS TYPE = HOST_PORT, GENERIC_STRING and OAUTH2 secrets, ALLOWED_NETWORK_RULES, ALLOWED_AUTHENTICATION_SECRETS, ENABLED, EXTERNAL_ACCESS_INTEGRATIONS and SECRETS clauses on the handler, GRANT USAGE ON INTEGRATION, RUNTIME_VERSION example.

Removed: the generic-secret retrieval function name and the Snowpark DataFrame write (not on the pages read; the pages show an OAuth access token function).

Method: documentation only; no commands were run.
