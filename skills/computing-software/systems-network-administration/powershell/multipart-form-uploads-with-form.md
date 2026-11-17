---
id: computing-software.systems-network-administration.powershell.multipart-form-uploads-with-form
name: multipart-form-uploads-with-form
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-rest, multipart-form-upload, invoke-restmethod, form-parameter, file-upload]
level: practitioner
status: verified
description: "Upload files and fields as multipart/form-data with Invoke-RestMethod -Form in PowerShell 7, and the manual MultipartFormDataContent approach for 5.1 or custom parts."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod
  - https://learn.microsoft.com/en-us/dotnet/api/system.net.http.multipartformdatacontent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multipart form uploads

## PowerShell 7: -Form
`-Form` arrived in PowerShell 6.1 (6.1 changelog: "Add Simplified multipart/form-data support to Web Cmdlets through -Form").
```powershell
$form = @{
  description = 'nightly export'
  tags        = 'finance','daily'                       # arrays become repeated fields
  file        = Get-Item '<EXPORTS>\report.csv'          # FileInfo = file part
}
Invoke-RestMethod -Uri 'https://api.example.com/v1/uploads' -Method Post -Form $form -Headers @{ Authorization = "Bearer $token" }
```
PowerShell builds `multipart/form-data` with the boundary and content-type: the test server saw
`multipart/form-data; boundary="..."`, the file part as `application/octet-stream` with `filename=report.csv; filename*=utf-8''report.csv`,
plain fields as `text/plain; charset=utf-8`, and `tags` as two separate `tags` parts. The hashtable order is not part order
(the parts arrived as description, file, tags, tags). There is no reason to set `-ContentType` with `-Form`; passing
`multipart/form-data` did not break the request in 7.6.7 and the boundary was still added.

## Custom parts (or PowerShell 5.1)
```powershell
Add-Type -AssemblyName System.Net.Http
$client  = [System.Net.Http.HttpClient]::new()
$content = [System.Net.Http.MultipartFormDataContent]::new()
$fs      = [System.IO.File]::OpenRead('<EXPORTS>\report.csv')
$file    = [System.Net.Http.StreamContent]::new($fs)
$file.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse('text/csv')
$content.Add($file, 'file', 'report.csv')   # arrives as Content-Type: text/csv, filename=report.csv
$content.Add([System.Net.Http.StringContent]::new('nightly export'), 'description')
$client.DefaultRequestHeaders.Authorization = [System.Net.Http.Headers.AuthenticationHeaderValue]::new('Bearer', $token)
try {
  $resp = $client.PostAsync('https://api.example.com/v1/uploads', $content).GetAwaiter().GetResult()
  $resp.EnsureSuccessStatusCode() | Out-Null
  $resp.Content.ReadAsStringAsync().GetAwaiter().GetResult() | ConvertFrom-Json
} finally { $fs.Dispose(); $client.Dispose() }
```
Use this when the API needs a specific part content-type, file name, or a JSON part alongside the file.

## Gotchas
- Field names must match exactly what the API expects (`file` vs `upload`); check its docs or a browser request.
- Large files: set a generous `-TimeoutSec` (default timeouts are per request; whether `-Form` streams from disk was not tested).
- Some APIs want raw body uploads instead (`-InFile` with `-ContentType`), not multipart.

## Verify
- [ ] API returns 2xx with the stored file's size/hash matching the local file.

## Checked
Ran against a local Python server that echoed the request: the `-Form` hashtable (string, string array, `Get-Item` FileInfo) in
PowerShell 7.6.7 with a bearer header, `-Form` plus `-ContentType`, and the `HttpClient` / `MultipartFormDataContent` block in both 7.6.7
and Windows PowerShell 5.1.26100 (custom `text/csv` part content type, `description` field, bearer header). `-Form` in 6.1 is from
CHANGELOG/6.1.md. The real `api.example.com` URL is a placeholder and was not called; no streaming or large-file test was run.
