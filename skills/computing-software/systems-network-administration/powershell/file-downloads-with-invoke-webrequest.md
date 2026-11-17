---
id: computing-software.systems-network-administration.powershell.file-downloads-with-invoke-webrequest
name: file-downloads-with-invoke-webrequest
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-rest, file-download-webrequest, invoke-webrequest, outfile, resume]
level: practitioner
status: verified
description: "Download files reliably with Invoke-WebRequest -OutFile (and -Resume in PS 7), progress overhead, proxies, hashes, and BITS or curl.exe for big transfers."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest
  - https://learn.microsoft.com/en-us/powershell/module/bitstransfer/start-bitstransfer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File downloads with Invoke-WebRequest

## Basic download
```powershell
$ProgressPreference = 'SilentlyContinue'      # 5.1 progress bar: 200 MB took 78 s with it, 0.6 s without
Invoke-WebRequest -Uri 'https://example.com/tools/agent-2.4.msi' -OutFile "$env:TEMP\agent-2.4.msi" -UseBasicParsing
```
- `-UseBasicParsing` avoids the IE/DOM parsing in 5.1 (the 5.1 docs say it is required when Internet Explorer is not
  installed, such as Server Core); 7.6.7 accepts and ignores it, and the progress bar made no difference there (0.5 s both ways).
- `-OutFile` streams to disk; don't capture `.Content` for big files (it loads them into memory).
- PS 7.4+: `-OutFile` may be a folder; the file name is then the last segment of the resolved URI after redirects, NOT the
  `Content-Disposition` name (a response offering `srv-name.bin` was saved as `file`), and `-Resume` cannot be used with a folder.

## Resume and retries (PowerShell 7)
```powershell
Invoke-WebRequest -Uri $u -OutFile $f -Resume -MaximumRetryCount 5 -RetryIntervalSec 10
```
`-Resume` continues a partial file if the server supports ranges (a 10 KB partial file was completed to the correct
hash). It only compares the local and remote sizes and does no other validation, so verify the hash afterwards.

## Verify integrity
```powershell
(Get-FileHash $f -Algorithm SHA256).Hash -eq $expectedSha256
Get-AuthenticodeSignature $f | Select Status,SignerCertificate
```

## Proxies and TLS
- On this machine 5.1's `[Net.ServicePointManager]::SecurityProtocol` was already `SystemDefault`; older or
  differently configured .NET Framework installs can default to old protocols. Pinning it:
  `[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12` (accepted; see
  tls-and-certificate-handling-web-requests).
- `-Proxy http://proxy:8080 -ProxyUseDefaultCredentials` worked in 5.1 and 7. PS 7 also honoured `HTTP_PROXY` and
  `HTTPS_PROXY` (a tunnel request reached the proxy), but the default proxy is read once per process, so set the variable
  before the first web request. 5.1 ignored `HTTP_PROXY`.

## Big or unattended transfers
```powershell
Start-BitsTransfer -Source $u -Destination $f -Priority Foreground      # needs a server that answers HEAD and ranges; jobs resume after the BITS service restarts (docs)
curl.exe -L --fail --retry 5 -o $f $u                                   # present on current Windows; exit 22 on a 404
```

## Verify
- [ ] File hash matches the publisher's value; script fails (non-zero exit) on a 404 rather than saving an HTML error page.

## Checked
Ran against a local Python HTTP server and a 200 MB file on PowerShell 7.6.7 and Windows PowerShell 5.1.26100:
download with `-OutFile`, SHA-256, a 404 (error, no HTML saved over a good file), `-OutFile <folder>` naming,
`-Resume` (partial 10 KB then 100 KB complete, hash match; a second `-Resume` on a complete file succeeded),
`-MaximumRetryCount` with `-Resume`, progress-bar timing in both editions, `Get-AuthenticodeSignature` on a non-script file
(`UnknownError`), `Start-BitsTransfer` (needed HEAD support; 5.1 completed it), `curl.exe -L --fail --retry` (exit 22 on a
404), proxy variables and `-Proxy`, SecurityProtocol value. Folder-name rule and `-Resume` size-only behaviour match the
Invoke-WebRequest reference (7.5); the BITS recovery sentence is from the Start-BitsTransfer page on Microsoft Learn.
