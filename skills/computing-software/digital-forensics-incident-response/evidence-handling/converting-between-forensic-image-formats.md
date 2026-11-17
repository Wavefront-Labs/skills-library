---
id: computing-software.digital-forensics-incident-response.evidence-handling.converting-between-forensic-image-formats
name: converting-between-forensic-image-formats
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [image-conversion, e01, raw-dd, vmdk, vhd, qemu-img, dfir]
level: practitioner
status: docs-checked
description: "Convert evidence between raw, VMDK, VHD and VHDX with qemu-img and handle EWF (E01) via libewf's tools, proving the media hash is unchanged."
sources: ["https://github.com/libyal/libewf", "https://www.qemu.org/docs/master/tools/qemu-img.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Converting between image formats (raw, E01, VMDK, VHD)

**Goal:** get evidence into the format each tool needs without losing integrity, and prove it with hashes of the logical content.

## Key principle
The media hash (hash of the decompressed, logical disk content) must be identical before and after conversion. Container files (E01 versus raw) have different file hashes, so compare the media hash, never the container file hash.

## Virtual disk formats with qemu-img
```bash
qemu-img info disk.vmdk                   # format, virtual size, backing file
qemu-img info --backing-chain disk.qcow2  # every image in a backing chain
qemu-img convert -O vpc  source.raw disk.vhd
qemu-img convert -O vhdx source.raw disk.vhdx
qemu-img convert -O vmdk source.raw disk.vmdk
qemu-img convert -O raw  disk.vmdk disk.raw
```
- Per the qemu-img page, `convert` takes `-O OUTPUT_FMT`, and `info` takes `--backing-chain` to enumerate information about the backing files of a chain.
- The page lists VMDK, VDI, VHD (`vpc`), VHDX, qcow1 and QED as other supported formats; run `qemu-img --help` for the full list on your build.
- Image chains: inspect with `info --backing-chain` and convert from the topmost image so the result includes the data in its backing files. (Practitioner advice; the page describes backing chains but does not state forensic handling.)

## EWF (E01)
libewf is a library to access the Expert Witness Compression Format (EWF); its repository lists `ewftools` among its components. Use those tools to export or acquire EWF images and follow their own manual pages for options; this skill does not repeat their flags.

## Verification
Hash the output (for example with `sha256sum`) and compare with the media hash of the input. Record tool name, version, command, input and output media hashes in case notes.

## Gotchas
- Booting a converted image for live view changes it; boot a copy, never the master.
- Split images: keep every segment together.

## Self-check
Input and output media hashes match and are recorded with the exact command used.

## Checked
Confirmed against the qemu-img documentation page (`convert -O`, `info --backing-chain`, supported formats VMDK, VDI, VHD (vpc), VHDX) and the libewf repository page (EWF library, ewftools component). Removed unconfirmed content: all ewfexport, ewfacquire, ewfmount, ewfverify and ewfinfo commands and flags, the aff4imager command and AFF4 coverage, FTK Imager menu steps, and thin-disk specifics.

Method: docs-only read of cited pages, 2026-11-09
