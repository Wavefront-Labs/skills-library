---
id: computing-software.cloud-infrastructure-engineering.netdata.bearer-token-protection
name: bearer-token-protection
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, bearer-token, cloud-sso, mcp-key]
level: practitioner
status: docs-checked
description: "Protect an Agent dashboard and API with Netdata Cloud SSO bearer tokens: requirements, which endpoints stay public, MCP behaviour and troubleshooting."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configuration/secure-your-netdata-agent-with-bearer-token.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: Agent claimed to Netdata Cloud, ACLK connection active, users with a Cloud account in the Agent's Space. Works on Community and Business plans.

```
cd /etc/netdata
sudo ./edit-config netdata.conf
```

```
[web]
    bearer token protection = yes
```

Then `sudo systemctl restart netdata`. Users are redirected to Cloud for SSO and access follows their Cloud role. Tokens last 24 hours and renew while the Cloud session is active.

Protected: `/api/v3/data`, `/api/v3/allmetrics`, `/api/v3/alerts`, `/api/v3/contexts`, `/api/v3/nodes`, `/api/v3/function(s)`, `/api/v3/config` and other v1/v2 APIs.
Still public: static web files (dashboard loads empty), `/api/v3/info`, `/api/v3/me`, claim endpoints, `/api/v3/stream_info`, `/api/v1/registry?action=hello`, `/api/v1/manage/health`.

MCP: with protection on, anonymous MCP requests are rejected; send `Authorization: Bearer <mcp_key>`.

Disable temporarily with `bearer token protection = no`, or `POST /api/v3/bearer_protection` (Cloud Admin or Manager).

Troubleshoot: check `cloud.status` (should be `online`) and `cloud.reason` at `http://your-server:19999/api/v3/info`; run `sudo netdatacli aclk-state`.

Combine with `allow connections from` and a firewall blocking port 19999 from untrusted networks.

## Checked

2026-11-04. Confirmed against the Netdata bearer token protection page: plans and claim requirement, the edit and restart steps, the 24-hour token life, protected and public endpoint lists, MCP behaviour with the Authorization header, disabling by config or POST /api/v3/bearer_protection, the troubleshooting steps via /api/v3/info and netdatacli aclk-state, and the combine-with advice. Nothing removed.

Method: documentation only; no commands were run.
