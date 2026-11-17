---
id: computing-software.digital-forensics-incident-response.evidence-handling.kape-remote-collection-to-sftp-s3-and-vhdx
name: kape-remote-collection-to-sftp-s3-and-vhdx
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [kape-remote-collection, kape, kape-targets, triage-collection, dfir]
level: advanced
status: docs-checked
description: "Run KAPE collections to a share, SFTP, S3 or Azure as VHDX/ZIP containers: UNC limits, running kape.exe from a share, transfer switches, footprint trade-offs and logs."
sources: ["https://ericzimmerman.github.io/KapeDocs/", "https://github.com/EricZimmerman/KapeFiles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KAPE remote collection to SFTP, S3 and VHDX

**Goal:** collect triage artefacts from remote hosts to central storage, knowing what is
written to the endpoint on the way.

## Three ways to collect remotely
1. **UNC or mapped drive as `--tsource`** (`--tsource \\target-1\c`): the target's C drive must be
   shared. Limits stated by the KAPE docs: volume shadow copies cannot be copied over a UNC
   path, and locked in-use files (registry hives) are deferred to a raw-disk-read copy that
   Windows does not allow across UNC. Fine for files like LNKs and jump lists, not for hives.
2. **Run `kape.exe` from a share on the collection system** (map it on the target, e.g.
   `net use k: \\kape-server-vm\triage /user:...`, then run
   `kape.exe --tsource C --target RegistryHives --tdest <share-out-dir> --vss` from the mapped drive).
   This copies locked files and VSCs, and writes no collected data or temp files to the target;
   running a program still leaves artefacts (a Prefetch file, registry entries).
3. **Upload from the target** with container and transfer switches (below). Data is written to
   `--tdest` first.

## Container output
```cmd
kape.exe --tsource C: --tdest <tout-dir> --target !SANS_Triage --vhdx %COMPUTERNAME% --zv false
```
- `--vhd`, `--vhdx` or `--zip` take a base name used in the container file name; if none is
  given the switch is ignored and no container is created.
- `--zv` (zip the VHD(X)) defaults to true; the docs example for an SFTP upload uses a VHDX
  that is then zipped to reduce transfer time. `--zpw` sets a zip password.
- KAPE shortens paths over 255 characters for container formats and keeps the original in
  `LongFileNames`.
- `*_copylog.csv` records source and destination file, SHA-1 (`SourceFileSha1`), size and
  timestamps, and `DeferredCopy` for locked files read raw; `*_skiplog.csv` lists files not
  copied ("Excluded" or "Deduped"). Keep both and the console log.

## Transfer options
```cmd
:: SFTP (needs a container; compressed VHD(X) and/or zipped module output)
kape.exe ... --vhdx %COMPUTERNAME% --scs sftp.example.org --scp 22 --scu <user> --scpw <password> --scd uploads/case
:: S3 with keys
kape.exe ... --vhdx %COMPUTERNAME% --s3p spAmazonS3 --s3r eu-west-1 --s3b <bucket> --s3k <key> --s3s <secret> --s3kp CASE-014
:: S3 with a presigned PUT URL (no other S3 options needed)
kape.exe ... --vhdx %COMPUTERNAME% --s3url "<presigned-put-url>"
:: Azure storage with a container SAS URI that has write permission
kape.exe ... --zip %COMPUTERNAME% --asu "<container-sas-uri>"
```
- `--scd` must not start with a slash; it is created if missing. `--scp` defaults to 22.
  `--s3st` supplies a session token for temporary credentials; `--s3p` defaults to
  `spAmazonS3`. The S3 key "must at least be writable". `--scc`, `--s3c`, `--asc` add a comment
  (default: the machine name). The AWS CLI cannot create PUT URLs; use an SDK.
- `--rlc` keeps the local copy after upload (default: deleted after transfer).
- KAPE can itself act as the SFTP server (`kape.exe --sftpc <config.skape>`) with per-user
  `Access` (`Download|Upload|Delete|List|All`) and `Jail`. `LogLevel Verbose` logs client
  passwords, so avoid it.

## Credentials and footprint
- Credentials sit on the command line you run on the endpoint; the SFTP password is redacted
  from the KAPE console log. Prefer a presigned URL or a narrowly scoped SAS URI, and rotate
  after the case.
- The KAPE docs flag the trade-off: with `--tdest` on a local drive of the target, the
  container and its zip are first written there, which risks overwriting unallocated space. Make that
  choice knowingly, especially if a full image may be needed later.

## Verify
- Count uploaded containers against the host list; re-run for missing hosts.
- Mount a sample VHDX and compare against the copy log entries.

## Gotchas
- `--tsource C:` covers only that volume; run per volume as needed.
- Run `--sync` on the master KAPE copy rather than on every endpoint.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against KapeDocs source pages: Using KAPE (switch reference), Log files, SFTP, Getting started, and "Remote Collections with KAPE".
Corrected: SFTP password switch is `--scpw` (not `--scw`); presigned S3 uses `--s3url` (`--s3o` is the Oracle namespace); log is `_copylog.csv`; `--scd` takes no leading slash.
Removed as not in the pages: VHDX timestamp-preservation claim, 4688/EDR logging, SYSTEM-account proxy problem, chroot advice for an arbitrary SFTP server, and the write-only IAM recommendation.
