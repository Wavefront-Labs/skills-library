---
id: computing-software.systems-network-administration.windows-server.iis-request-filtering-and-security-headers
name: iis-request-filtering-and-security-headers
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iis, request-filtering, security-headers, hsts, iis-hardening]
level: practitioner
status: docs-checked
description: "Harden IIS with request filtering (verbs, extensions, URL length, hidden segments) and response security headers (HSTS, X-Content-Type-Options, removing Server header)."
sources:
  - https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/
  - https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/requestlimits
  - https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httpprotocol/customheaders/
  - https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/hsts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIS request filtering and security headers

## Request filtering (`system.webServer/security/requestFiltering`)
```xml
<system.webServer>
  <security>
    <requestFiltering removeServerHeader="true" allowDoubleEscaping="false" allowHighBitCharacters="false">
      <requestLimits maxAllowedContentLength="30000000" maxUrl="4096" maxQueryString="2048" />
      <verbs allowUnlisted="false">
        <add verb="GET" allowed="true" /><add verb="POST" allowed="true" /><add verb="HEAD" allowed="true" />
      </verbs>
      <fileExtensions allowUnlisted="true">
        <add fileExtension=".config" allowed="false" /><add fileExtension=".bak" allowed="false" />
      </fileExtensions>
      <hiddenSegments><add segment="App_Data" /><add segment=".git" /></hiddenSegments>
    </requestFiltering>
  </security>
</system.webServer>
```
- The values shown for `maxAllowedContentLength` (30000000), `maxUrl` (4096) and `maxQueryString` (2048) are the
  defaults; tighten them rather than copying them.
- Blocked requests return 404 with a substatus: 404.5 URL sequence, 404.6 verb, 404.7 file extension, 404.8 hidden
  namespace (segment), 404.11 double-escaped URL, 404.12 high-bit characters, 404.14 URL too long, 404.15 query string
  too long, 404.18 query string sequence, 404.19 denied by filtering rule. Content too long returns 413.1. Check
  `sc-substatus` in the IIS logs.
- `removeServerHeader` was added in IIS 10.0 and works only on Windows Server version 1709 / Windows 10 version 1709
  and later.
- `maxAllowedContentLength` is in bytes (about 28.6 MB by default); raise it per upload application, not globally.

## Security headers
```xml
<httpProtocol>
  <customHeaders>
    <remove name="X-Powered-By" />
    <add name="X-Content-Type-Options" value="nosniff" />
    <add name="Referrer-Policy" value="strict-origin-when-cross-origin" />
    <add name="Content-Security-Policy" value="default-src 'self'" />
  </customHeaders>
</httpProtocol>
```
Custom headers are sent on every response. Native HSTS (IIS 10.0 version 1709 and later) is configured per site
in the `hsts` element (`enabled`, `max-age`, `includeSubDomains`, `preload`, `redirectHttpToHttps`):
```cmd
appcmd set config -section:system.applicationHost/sites "/[name='Shop'].hsts.enabled:True" /commit:apphost
appcmd set config -section:system.applicationHost/sites "/[name='Shop'].hsts.max-age:31536000" /commit:apphost
```
Enable `preload` only if the domain has been submitted to the HSTS preload list. `redirectHttpToHttps` redirects
to https on port 443, so confirm that destination works.

## Gotchas
- Start CSP in report-only mode (`Content-Security-Policy-Report-Only`) to avoid breaking the app.
- Server-level settings are inherited; test each app after a server-wide change.

## Verify
- [ ] A header check of the site shows the headers and no `Server` or `X-Powered-By`; a TRACE request is refused
  (404.6 when TRACE is not in the verbs list).

## Checked
Date 2026-10-27. Documentation: IIS requestFiltering, requestLimits, customHeaders and hsts reference pages.
Confirmed: element and attribute names, defaults, substatus table, removeServerHeader version note, HSTS attributes
and appcmd form. Header values (CSP, Referrer-Policy) are policy choices, not documented defaults.
Method: documentation only; no commands were run.
