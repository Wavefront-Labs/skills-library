---
id: computing-software.digital-forensics-incident-response.evidence-handling.validating-memory-images-after-capture
name: validating-memory-images-after-capture
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [memory-image-validation, memory-acquisition, volatility3, evidence-integrity, dfir]
level: practitioner
status: docs-checked
description: "Check a memory capture while the host is still available: output format, tool limits for WinPmem and AVML, format conversion and Volatility 3 plugins."
sources: ["https://volatility3.readthedocs.io/en/latest/", "https://github.com/Velocidex/WinPmem", "https://github.com/microsoft/avml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validating memory images after capture

**Goal:** a memory image cannot be re-collected later, so check it while the host is still available and a failed capture can be repeated.

## Know what the tool produces
- **WinPmem** (Windows): `winpmem_mini_x64.exe` and `winpmem_mini_x86.exe` produce RAW images only (the "mini" imager); `winpmem_mini_x64.exe physmem.raw` writes a raw image with the default method, and running it with no arguments prints usage. The driver is unloaded automatically after acquisition. The README documents several reading methods (for example `-1` for MmMapIoSpace) and a limitation: reads fail with STATUS_INVALID_PARAMETER for physical addresses above half the UINT64 maximum.
- **AVML** (Linux, x86_64): `avml acquire output.lime` writes LiME format; `--compress` gives AVML's page-level Snappy-compressed format. Memory sources are `/dev/crash`, `/proc/kcore` and `/dev/mem`; if none is specified it tries them in turn. It cannot acquire memory if the kernel `kernel_lockdown` feature is enabled. `avml convert` converts between AVML, LiME and raw formats (decompress with `avml convert ./compressed.lime ./uncompressed.lime`). `avml stream` sends a snapshot without a local file; the TCP mode has no resume and no TLS.
- Record the tool, its version, the exact command, and the tool's own output.

## Checks to run before leaving the host
1. Confirm an image file exists, was written to the evidence media, and the tool reported success; keep its output.
2. Hash the image and record the hash in the collection log.
3. Confirm the image opens in your analysis stack. Volatility 3's documentation lists Windows plugins including `windows.info`, `windows.pslist`, `windows.psscan` and `windows.netscan`, and Linux plugins including `linux.pslist`. Run an identification plugin and a process-listing plugin on the image; the page index does not describe their output, so read each plugin's own documentation and note failures.
4. For compressed AVML images, check your tools understand the format, or convert to raw or LiME and record the conversion.
5. If a check fails, repeat the capture (a different tool is an option) while the host is still available, and log both attempts.

## Verify
An identification plugin and a process-listing plugin both succeed on the image, the hash is recorded, and tool, version and command are logged, before the responder leaves the host.

## Checked
Confirmed against the WinPmem README (RAW-only mini imagers, usage, driver unload, limitation), the AVML README (formats, sources, kernel lockdown, convert and stream, no TLS) and the Volatility 3 documentation index (plugin module names). Removed unconfirmed content: size-versus-RAM rule, expected process names, zero-region checks, `xxd`, `systeminfo` and `/proc/meminfo` steps, `banners.Banners`, DumpIt and EDR alternatives, and VBS/Hyper-V failure claims; the Volatility index lists plugins but does not describe their output.

Method: docs-only read of cited pages, 2026-11-09
