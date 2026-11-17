---
id: computing-software.systems-network-administration.windows-server.iis-url-rewrite-and-arr-reverse-proxy
name: iis-url-rewrite-and-arr-reverse-proxy
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iis, iis-administration, url-rewrite, arr, application-request-routing, reverse-proxy, http-to-https-redirect, server-farm]
level: advanced
status: docs-checked
description: "Use IIS URL Rewrite and Application Request Routing: HTTP to HTTPS redirects, rewrite rules, ARR reverse proxy to backend servers, server farms, health tests and headers."
sources:
  - https://learn.microsoft.com/en-us/iis/extensions/url-rewrite-module/using-the-url-rewrite-module
  - https://learn.microsoft.com/en-us/iis/extensions/url-rewrite-module/url-rewrite-module-configuration-reference
  - https://learn.microsoft.com/en-us/iis/extensions/url-rewrite-module/reverse-proxy-with-url-rewrite-v2-and-application-request-routing
  - https://learn.microsoft.com/en-us/iis/extensions/planning-for-arr/using-the-application-request-routing-module
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL Rewrite and ARR reverse proxy

URL Rewrite rewrites or redirects requests using HTTP headers and server variables; Application Request Routing
(ARR) is a proxy-based routing module that forwards requests to content servers by headers, server variables and
load-balance algorithms. Both are separate IIS extensions you install; use URL Rewrite 2.0 or later for outbound rules.

## HTTP to HTTPS redirect (web.config)
```xml
<system.webServer>
  <rewrite><rules>
    <rule name="HTTPS redirect" stopProcessing="true">
      <match url="(.*)" />
      <conditions><add input="{HTTPS}" pattern="off" /></conditions>
      <action type="Redirect" url="https://{HTTP_HOST}/{R:1}" redirectType="Permanent" />
    </rule>
  </rules></rewrite>
</system.webServer>
```
- The `HTTPS` and `SERVER_PORT_SECURE` server variables tell you whether the connection was secure; `HTTP_HOST` holds
  the host name.
- `Redirect` returns a redirect status to the client (`redirectType` 301 Permanent and others); the module does not
  support 308. `Rewrite` changes the URL internally.
- `stopProcessing="true"` ends rule evaluation when the rule matches.

## Reverse proxy to a backend
Enable proxy: IIS Manager > server > Application Request Routing Cache > Server Proxy Settings > **Enable proxy**
(leave the other defaults for a basic setup). Microsoft's walkthrough then adds a rule on the front site:
```xml
<rule name="To app" stopProcessing="true">
  <match url="^api/(.*)" />
  <action type="Rewrite" url="http://app01:5000/{R:1}" />
</rule>
```
Setting request headers such as `X-Forwarded-Proto` through `<serverVariables>` requires the variable to be allowed
in URL Rewrite (confirm the exact steps in the module's server variable documentation).

## Outbound rules
Links in backend responses that point at the backend name can be rewritten with an outbound rule (URL Rewrite 2.0).
Outbound evaluation of response bodies is CPU intensive, so use a precondition (for example content type
`text/html`) to limit where it applies.

## Server farm (load balancing)
IIS Manager > Server Farms: add backend servers and ARR creates the routing rule. Load-balance algorithm, health
tests and client affinity options live in the farm settings (see the ARR planning page).

## Gotchas
- The ARR proxy timeout and maintenance status of the module are not covered by the pages checked here; verify them
  in current Microsoft documentation before relying on them.
- Consider whether a newer gateway fits better for new builds.

## Verify
- [ ] A request to http://site returns a redirect to https; the proxied path returns backend content with correct
  host and forwarded headers.

## Checked
Date 2026-10-27. Documentation: URL Rewrite module overview and configuration reference, "Reverse Proxy with URL
Rewrite v2 and ARR" walkthrough, ARR planning page. Confirmed: rule and action syntax shown, server variables,
redirect types, 308 not supported, outbound rule precondition advice, Enable proxy setting.
Method: documentation only; no commands were run.
