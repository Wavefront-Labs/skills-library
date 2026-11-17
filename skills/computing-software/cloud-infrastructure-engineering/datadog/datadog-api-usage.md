---
id: computing-software.cloud-infrastructure-engineering.datadog.datadog-api-usage
name: datadog-api-usage
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, datadog-api, rest-api, api-v2, datadog-api-client]
level: practitioner
status: draft
description: "Submit metrics and read monitors using the v1/v2 REST API and official client libraries with site-specific URLs."
sources: ["https://docs.datadoghq.com/", "https://docs.datadoghq.com/agent/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using the Datadog API
Goal: automate Datadog through the API.

```
curl -X POST "https://api.datadoghq.com/api/v2/series" \
  -H "Content-Type: application/json" -H "DD-API-KEY: <DD_API_KEY>" \
  -d '{"series":[{"metric":"custom.deploys","type":1,"points":[{"timestamp":1767225600,"value":1}],"tags":["env:prod"]}]}'

curl -s "https://api.datadoghq.com/api/v1/monitor?tags=team:payments" \
  -H "DD-API-KEY: <DD_API_KEY>" -H "DD-APPLICATION-KEY: <DD_APP_KEY>"
```

```python
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
with ApiClient(Configuration()) as c:   # reads DD_API_KEY, DD_APP_KEY, DD_SITE
    print(len(MonitorsApi(c).list_monitors()))
```

- Use the right base URL for your site.
- Submitting data needs the API key; reading/modifying needs the app key too.
- Respect rate limits: read `X-RateLimit-*` headers.

Gotcha: timestamps must be within recent windows (about the last hour in the future/past limits: confirm); older points are rejected.

Handle HTTP 429 by backing off using the reset header, and pagination for list calls with large result sets. Use idempotent upserts so retries do not duplicate resources. Prefer the official client libraries over hand-built HTTP calls, since they handle retries, models and site configuration.

## Verify
- HTTP 202 for series submissions and the metric appears in Metrics Summary.
