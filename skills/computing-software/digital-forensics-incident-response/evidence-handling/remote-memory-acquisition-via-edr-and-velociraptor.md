---
id: computing-software.digital-forensics-incident-response.evidence-handling.remote-memory-acquisition-via-edr-and-velociraptor
name: remote-memory-acquisition-via-edr-and-velociraptor
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [remote-memory-acquisition, velociraptor, winpmem, edr-live-response, memory-acquisition, dfir]
level: practitioner
status: docs-checked
description: "Acquire memory remotely with Velociraptor (Windows.Memory.Acquisition, Linux.Memory.AVML), AVML streaming or Defender live response: compression, limits and image checks."
sources: ["https://docs.velociraptor.app/artifact_references/pages/windows.memory.acquisition/", "https://github.com/Velocidex/WinPmem", "https://github.com/microsoft/avml", "https://docs.velociraptor.app/exchange/artifacts/pages/linux.memory.avml", "https://learn.microsoft.com/en-us/defender-endpoint/live-response"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Remote memory acquisition via EDR and Velociraptor

For remote or cloud hosts, or many hosts at once, memory is captured through an agent and uploaded. Size, bandwidth and agent limits drive the method.

## Velociraptor
- **Windows**: collect `Windows.Memory.Acquisition` (windows amd64 only). It acquires a full image with the built-in WinPmem driver into a temp file and uploads it as `PhysicalMemory.dd`. Parameters: `ServiceName` (override the driver service name), `DriverPath` (default `winpmem.sys` under the Windows Temp directory), `Compression` (`None` default; `S2`, `Snappy`, `Gzip`; the parameter text recommends None, S2 or Snappy). The artifact notes that images smear, so acquire quickly; compression cuts IO time but costs CPU, and S2 gave reasonable compression with very high speed. Decompress with the Go WinPmem binary: `go-winpmem.exe extract image.compressed image.raw`.
- The artifact says it usually transfers a lot of data and you should increase the default timeout.
- **Linux**: the exchange artifact `Linux.Memory.AVML` (linux amd64) downloads Microsoft's AVML from the microsoft/avml GitHub project, writes a LiME-format image to a temp file and uploads it as `memory.lime`; it needs the EXECVE permission and carries the same raise-the-timeout note. It runs avml with only the output path and exposes no compression parameter. AVML cannot acquire memory when the kernel `kernel_lockdown` feature is enabled.

## AVML directly (Linux)
- `avml acquire output.lime` (LiME format) or `avml acquire --compress output.lime.compressed` (Snappy page-level compression); memory sources tried are `/dev/crash`, `/proc/kcore`, `/dev/mem`.
- Upload options: `--sas-url` for an Azure Blob SAS URL, `--url` for a presigned S3 or GCP URL, `--delete` to remove the local file after upload.
- `avml stream blob <SAS_URL>` or `avml stream tcp host:port` write the snapshot with no local file, for hosts where a local write is undesirable (read-only root, limited disk, chain-of-custody concerns). A dropped TCP connection aborts the snapshot with no resume, and there is no TLS (use an SSH tunnel or stunnel).
- `avml convert` converts between AVML, LiME and raw formats (for example to decompress).

## WinPmem directly (Windows)
`winpmem_mini_x64.exe physmem.raw` writes a RAW image and loads and unloads the driver itself. The README lists support for Windows 7 to Windows 10.

## Defender for Endpoint live response
- Upload WinPmem and a wrapper script to the live response library (library limit 250 MB; 5 MB default in US Government cloud), `putfile` it to the device (limit 300 MB Windows, 10 MB other platforms), `run` the library script (PowerShell or Bash scripts only from the library; unsigned PowerShell needs an advanced-features setting), then `getfile` the output.
- Limits: `getfile` 3 GB; commands time out at 10 minutes except `getfile`, `findfile` and `run` at 30 minutes; sessions time out after 30 minutes of inactivity; a device can be in one session at a time. For large files in low bandwidth the page advises splitting the file and downloading the parts.
- `getfile <path> &` runs the download in the background; `fg <id>` brings it forward. CTRL+C cancels a command only in the portal, not on the agent.
- Live response requires Defender for Endpoint Plan 2 and enabling it in the portal's advanced features; only users with the matching permissions can open sessions.

## Procedure
1. Check free disk space on the target for the image, or stream directly (AVML `stream`) where supported.
2. Record start/end times and tool version in the collection log.
3. Hash on the target after writing, hash after download, compare.
4. Open the image in your analysis tool to confirm it parses before releasing the host.
5. Delete the temporary image from the target and record the deletion.

## Gotchas
- Writing the image to the target's own disk uses space on the evidence drive; prefer streaming or an attached volume if disk evidence matters.
- Memory smear grows with acquisition time; slow transfers and heavy compression CPU affect it.

## Verify
The downloaded image's hash matches the hash computed on the host, and the analysis tool parses it.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against: Velociraptor Windows.Memory.Acquisition and Linux.Memory.AVML artifact pages, the WinPmem and AVML READMEs, and the Microsoft Learn live response page (updated 2026-07-28).
Removed as not stated by the pages: server-side upload hashing and directory, offline-collector cloud upload advice, CrowdStrike and SentinelOne behaviour, per-process EDR dumps, Secure Boot/HVCI/self-protection blocking of the driver, and specific Volatility plugin names.
