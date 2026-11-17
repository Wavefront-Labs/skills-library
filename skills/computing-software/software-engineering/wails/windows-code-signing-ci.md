---
id: computing-software.software-engineering.wails.windows-code-signing-ci
name: windows-code-signing-ci
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, code-signing, windows, github-actions, signtool, ci]
level: practitioner
status: docs-checked
description: "Sign a Wails Windows binary in GitHub Actions with a base64 PFX certificate secret and signtool, including timestamp flag differences between certificate providers."
sources: [https://wails.io/docs/guides/signing]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows code signing in GitHub Actions

Goal: produce a signed `build/bin/<outputfilename>.exe` in CI.

## Prerequisites

- A standard code signing certificate. An EV certificate is not required unless you write kernel-level software such as drivers.
- Learn to sign locally with your provider first; requirements differ. SSL.com certificates need the `/tr` flag of SignTool while other providers may only need `/t` for the timestamp server. The popular code-sign GitHub Action does not support `/tr`, so the guide signs with PowerShell commands.

## Steps

1. Get the app building in CI first: matrix of `windows-latest`/`macos-latest`, `actions/setup-go`, `actions/setup-node`, `go install github.com/wailsapp/wails/v2/cmd/wails@latest`, then `wails build`, then upload `build/bin/*`. (Build your frontend explicitly unless `frontend:install`/`frontend:build` are in `wails.json`.)
2. Encode the certificate (.pfx/.p12) in PowerShell:
   ```PowerShell
   certutil -encode .\my-cert.p12 my-cert-base64.txt
   ```
   The output starts with BEGIN CERTIFICATE and ends with END CERTIFICATE.
3. Create two repo Actions secrets (Settings -> Secrets -> Actions): `WIN_SIGNING_CERT` (the base64 text) and `WIN_SIGNING_CERT_PASSWORD`.
4. Add after the build step:
   ```yaml
   - name: Sign Windows binaries
     if: matrix.platform == 'windows-latest'
     run: |
       New-Item -ItemType directory -Path certificate
       Set-Content -Path certificate\certificate.txt -Value '${{ secrets.WIN_SIGNING_CERT }}'
       certutil -decode certificate\certificate.txt certificate\certificate.pfx
       & '<WINDOWS_SDK_BIN>/x86/signtool.exe' sign /fd sha256 /tr http://ts.ssl.com /f certificate\certificate.pfx /p '${{ secrets.WIN_SIGNING_CERT_PASSWORD }}' .\build\bin\app.exe
   ```
   Replace the algorithm (usually sha256), timestamp server URL, and binary path for your setup.

## Alternative

A marketplace Action ("Code sign a file with pfx certificate") can do it automatically but needs the certificate SHA1 hash and name.

## Related

macOS counterpart: `computing-software.software-engineering.wails.macos-code-signing-ci`.

## Checked

2026-11-07. Read the whole Code Signing guide (website/docs/guides/signing.mdx), the Windows half in detail: certificate and EV-not-required statement, SSL.com /tr versus /t timestamp flags, the code-sign-action /tr limitation, the base workflow template, certutil -encode, the two secrets, Method 1 (PowerShell commands with the signtool line and its three placeholders, and the worked SSL.com workflow using /fd sha256 /tr http://ts.ssl.com) and Method 2 (marketplace action needing a SHA1 hash and certificate name). The macOS half of the page was read but belongs to another skill. The signtool path in the skill is a <WINDOWS_SDK_BIN> placeholder for the page's Windows Kits folder. The linked SSL.com guide, SignTool docs and Action repositories were not opened. No claims were trimmed.

Method: documentation only; no commands were run.
