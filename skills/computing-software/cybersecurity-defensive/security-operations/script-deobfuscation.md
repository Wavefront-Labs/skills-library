---
id: computing-software.cybersecurity-defensive.security-operations.script-deobfuscation
name: script-deobfuscation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [malware-analysis, script-deobfuscation, powershell-deobfuscation, encodedcommand, javascript-malware, vbscript, cyberchef, amsi-logs, script-block-logging]
level: advanced
status: draft
description: "Deobfuscate malicious PowerShell, JavaScript and VBScript safely with CyberChef and logging, to recover the real commands, URLs and payloads."
sources: ["Microsoft Learn - PowerShell script block logging (event 4104)", "GCHQ CyberChef documentation", "CySA+ CS0-003 objective 1.2 (indicators in scripts)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Script deobfuscation

**Goal:** turn an obfuscated script into readable commands and indicators, without
executing the malicious parts.

## First, check if Windows already did it for you
PowerShell script block logging (event **4104** in `Microsoft-Windows-PowerShell/Operational`)
records the deobfuscated script as executed, including each dynamically generated layer.
AMSI-integrated EDRs also capture decoded content. Search those before working by hand.

## PowerShell
- `-EncodedCommand` / `-enc`: base64 of UTF-16LE. CyberChef: From Base64 -> Decode text (UTF-16LE).
- `FromBase64String` + `IO.Compression.DeflateStream`/`GzipStream`: From Base64 -> Raw Inflate / Gunzip.
- String building (`'Inv'+'oke-Ex'+'pression'`), format operator (`"{1}{0}" -f 'ex','I'`), backticks,
  `[char]` arrays: let PowerShell itself evaluate only the string expression in an isolated VM,
  replacing `Invoke-Expression`/`IEX`/`| iex` with `Write-Output` so the payload is printed, not run.
- Repeat layer by layer; recording each layer in the case notes.

## JavaScript (.js via wscript, HTML smuggling)
- Replace `eval(` with `console.log(` and run in Node inside the lab VM with no network, or use
  a JS beautifier and CyberChef for string arrays.
- Watch for `ActiveXObject("WScript.Shell")`, `MSXML2.XMLHTTP`, `ADODB.Stream`: download-and-execute.

## VBScript / HTA
- Replace `Execute`/`ExecuteGlobal`/`Eval` with `WScript.Echo` and run with `cscript` in the lab.
- `Chr()` arithmetic chains: evaluate with a small Python script rather than running VBScript.

## Batch / CMD
- `set` variable substring tricks (`%var:~3,1%`): run with `echo` instead of the final call, or
  expand with a script; look for `certutil -decode`, `bitsadmin`, `curl`, `mshta`.

## CyberChef recipes worth saving
From Base64, Decode text UTF-16LE, Raw Inflate, Gunzip, XOR (with key brute force), From Hex,
Regular expression (extract URLs/IPs), Defang URL.

## Gotchas
- "Just run it with IEX replaced" still executes everything before the IEX; read the whole script first.
- Scripts check for sandboxes or domain membership and may behave differently in the lab.
- Never deobfuscate on a production analyst workstation with network access.

## Verify
- [ ] Final layer documented with all URLs, IPs, file paths and commands as defanged IOCs.
- [ ] Detections cover the behaviour (e.g. encoded PowerShell from Office) not just this sample's strings.
