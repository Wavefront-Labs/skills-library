---
id: computing-software.systems-network-administration.powershell.rest-api-authentication
name: rest-api-authentication
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, invoke-restmethod, invoke-webrequest, rest-authentication, oauth2, bearer-token, client-credentials, basic-auth]
level: practitioner
status: docs-checked
description: "Authenticate REST calls from PowerShell: API-key headers, Basic, default credentials, OAuth2 client-credentials tokens, -Authentication Bearer and error handling."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod
  - https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow
  - https://datatracker.ietf.org/doc/html/rfc6750
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REST authentication with Invoke-RestMethod

## API key / custom header
```powershell
$h = @{ 'X-Api-Key' = $apiKey; Accept = 'application/json' }
Invoke-RestMethod -Uri 'https://api.vendor.example/v2/devices' -Headers $h
```
Fetch `$apiKey` from a secret store at the point of use; never hard-code it.

## Basic, bearer and default credentials
```powershell
Invoke-RestMethod -Uri $u -Authentication Basic -Credential $cred
Invoke-RestMethod -Uri $u -Authentication Bearer -Token $secureToken      # SecureString
Invoke-RestMethod -Uri $u -UseDefaultCredentials                          # current user's credentials
```
- `-Authentication` accepts None (default), Basic, Bearer, OAuth. Bearer and OAuth require
  `-Token` (a SecureString) and send an RFC 6750 `Authorization: Bearer` header.
- `-Authentication` cannot be combined with `-UseDefaultCredentials`.
- With `-Authentication` or `-Credential`, a `Uri` not starting with `https://` is an error unless
  you add `-AllowUnencryptedAuthentication` (at your own risk).
- `-Credential` on its own supplies credentials only if the server sends an authentication
  challenge; with `-Authentication` they are sent explicitly. If an API never challenges, use
  `-Authentication Basic` or set the `Authorization` header yourself.

## OAuth2 client credentials (Microsoft Entra example)
The v2.0 token endpoint takes a form-encoded POST with `client_id`, `scope`, `client_secret` and
`grant_type=client_credentials`; for Microsoft Graph the scope is `https://graph.microsoft.com/.default`.
```powershell
$r = Invoke-RestMethod -Method Post -Uri "https://login.microsoftonline.com/$TenantId/oauth2/v2.0/token" -Body @{
  client_id = $ClientId; client_secret = $ClientSecret
  scope = 'https://graph.microsoft.com/.default'; grant_type = 'client_credentials' }
$expires = (Get-Date).AddSeconds($r.expires_in)
Invoke-RestMethod -Uri 'https://graph.microsoft.com/v1.0/users?$top=5' -Headers @{ Authorization = "Bearer $($r.access_token)" }
```
- `expires_in` is the token lifetime in seconds: keep the token and request a new one shortly
  before it expires rather than one per call.
- If `-ContentType` is omitted, a POST uses `application/x-www-form-urlencoded` (what the token
  endpoint expects); a PUT uses `application/json`. For JSON bodies, pass JSON text and
  `-ContentType 'application/json'`.
- For a higher level of assurance Microsoft allows a certificate or federated credential instead
  of a shared secret: the request sends `client_assertion_type` and `client_assertion` (a signed
  JWT) in place of `client_secret`. Never publish the credential in source code.
- Single-quote URIs containing `$top` or `$filter`, or PowerShell expands them as variables.

## Error responses (PowerShell 7)
`-SkipHttpErrorCheck` (introduced in PowerShell 7) writes HTTP error responses to the pipeline
instead of throwing; with `-StatusCodeVariable sc` you can branch on the status code:
```powershell
$body = Invoke-RestMethod -Uri $u -Headers $h -SkipHttpErrorCheck -StatusCodeVariable sc
if ($sc -ge 400) { Write-Error "HTTP $sc : $($body | ConvertTo-Json -Depth 3)" }
```

## Never
- Log headers or tokens.
- Put secrets in the URI query string.

## Verify
- [ ] Token is fetched once and reused until near expiry.
- [ ] 401/403 errors show the API's error message, not just a generic failure.

## Checked
2026-11-09. Read the Invoke-RestMethod reference (parameters -Authentication, -Token,
-AllowUnencryptedAuthentication, -UseDefaultCredentials, -Credential, -ContentType,
-SkipHttpErrorCheck, -StatusCodeVariable) and the Microsoft Entra client credentials flow page
(token request fields, v2.0 endpoint, .default scope, expires_in, certificate variant). RFC 6750 is
cited for the Bearer header (via the cmdlet page). Removed as unconfirmed: the Invoke-WebRequest
versus Invoke-RestMethod comparison, the throttling claim, the Azure metadata-endpoint example,
Get-Secret usage, the ErrorDetails and Response.StatusCode patterns, and the "PS 5.1" Basic header
snippet.

Method: documentation only; no commands were run.
