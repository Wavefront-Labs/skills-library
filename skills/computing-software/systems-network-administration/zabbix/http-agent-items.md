---
id: computing-software.systems-network-administration.zabbix.http-agent-items
name: http-agent-items
category: computing-software
field: systems-network-administration
product: zabbix
tags: [http-agent, url, query-fields, retrieve-mode, status-codes, http, agent]
level: practitioner
status: docs-checked
description: "Poll web endpoints with HTTP agent items: request type, body, headers, required status codes, redirects and proxy."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/http
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HTTP agent items poll an HTTP or HTTPS URL without any agent on the target. The server (or the proxy, if the host is proxied) runs the check and needs libcurl support. Checks are asynchronous with up to 1000 concurrent per poller (MaxConcurrentChecksPerPoller); the poller count is StartHTTPAgentPollers. Persistent cURL connections have been used since 7.0.

Item fields:
- URL, with Query fields as attribute and value pairs (values are URL-encoded automatically).
- Request type: GET, POST, PUT or HEAD.
- Request body type: Raw data (macros substituted, no encoding), JSON data, or XML data (needs libxml2).
- Headers as attribute and value pairs.
- Required status codes, for example 200,201,210-299. A code outside the list makes the item unsupported; empty means no check.
- Follow redirects (hard limit 10).
- Retrieve mode: Body, Headers, or Body and headers.
- Convert to JSON: headers are saved under a "header" key; a body is parsed as an object only when Content-Type is application/json.
- HTTP proxy in the form [protocol://][username[:password]@]host[:port], with protocols such as socks5 allowed.

Supported macros in URL, query, body and headers include {HOST.IP}, {HOST.CONN}, {HOST.DNS}, {HOST.HOST}, {HOST.NAME}, {HOST.PORT}, {ITEM.ID}, {ITEM.KEY}, user macros and LLD macros.

Pair an HTTP item that returns JSON with dependent items and JSONPath preprocessing so one request feeds many metrics. Trapping is also possible with zabbix_sender or the history.push API method.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/itemtypes/http): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
