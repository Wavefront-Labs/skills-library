---
id: computing-software.cybersecurity-defensive.system-hardening.iis-hardening
name: iis-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [web-server-hardening, iis-hardening, iis, request-filtering, app-pool-identity, tls-registry, iiscrypto]
level: practitioner
status: docs-checked
description: "Harden Microsoft IIS: minimal role services, app pool identities, request filtering, remove server headers, disable directory browsing and WebDAV, and configure TLS via SCHANNEL."
sources: ["https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/", "https://learn.microsoft.com/en-us/windows-server/security/tls/tls-registry-settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIS hardening

**Goal:** an IIS server with only required features, isolated app pools, request filtering, no banners and modern TLS.

## Role services
Install only what the apps need. Remove WebDAV, FTP, CGI, classic ASP, directory browsing and the management service if unused.

## App pools
- One app pool per application, identity `ApplicationPoolIdentity` (virtual account) or a gMSA - never LocalSystem.
- NTFS permissions: app pool identity read-only on content; write only to specific upload dirs, with execute disabled there (handler mappings: Read only).

## Request filtering (`web.config` / applicationHost)
```xml
<system.webServer>
  <security>
    <requestFiltering removeServerHeader="true" allowDoubleEscaping="false" allowHighBitCharacters="false">
      <requestLimits maxUrl="4096" maxQueryString="2048" />
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
`removeServerHeader` needs IIS 10.0 or later.

## TLS
Configured in SCHANNEL registry (`HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols`) - each protocol has its own subkey with Client and Server keys; disable SSL 3.0, TLS 1.0 and TLS 1.1 as your clients allow (see Microsoft's TLS registry settings page).

## Logging
Enable request logging with the fields you need, including the real client address when behind a proxy; forward to SIEM.

## Verify
- [ ] `curl -sI` shows no `Server` header.
- [ ] A TLS scanner shows only the protocol versions you intend.
- [ ] Directory browsing is disabled for all sites.

## Checked
2026-10-28. Confirmed against official pages: requestFiltering attributes removeServerHeader (IIS 10.0+), allowDoubleEscaping, allowHighBitCharacters, requestLimits maxUrl and maxQueryString, verbs, fileExtensions, hiddenSegments; SCHANNEL protocol registry path (Microsoft Learn).
Removed or rewritten: maxAllowedContentLength, directoryBrowse/customHeaders/httpErrors snippets, ASP.NET settings, IIS Crypto, HSTS version gate, SchUseStrongCrypto, X-Powered-By, named features, and the CIS benchmark source (blocked).
Method: documentation only; no commands were run.
