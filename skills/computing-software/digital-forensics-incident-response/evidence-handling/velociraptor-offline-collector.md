---
id: computing-software.digital-forensics-incident-response.evidence-handling.velociraptor-offline-collector
name: velociraptor-offline-collector
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [velociraptor-offline-collector, velociraptor, triage-collection, live-response, kape-targets, dfir]
level: practitioner
status: docs-checked
description: "Velociraptor offline collectors: when to use them, embedded vs Generic collector, how the zip container is encrypted (X.509, PGP, password), size limits, concurrency and import."
sources: ["https://docs.velociraptor.app/docs/deployment/offline_collections/", "https://docs.velociraptor.app/artifact_references/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Velociraptor offline collector

**Goal:** a standalone Velociraptor binary that collects pre-selected artifacts on a host with no server connection, stores the results in a portable zip, and can be run by non-specialists.

## What it is
- A full-featured Velociraptor binary with a custom configuration and the selected artifacts embedded; any third-party tools the artifacts need are repackaged into it. It is made from the standard binary (no compiling) and still does everything the unmodified binary does. Offline collector behaviour starts only when the binary is launched with no command line arguments.
- On launch it collects the artifacts in the config, stores results, logs and metadata in a structured zip (typically encrypted or password-protected), optionally uploads it to a cloud storage service or network destination, and optionally deletes the local container after upload. It shows progress in a terminal; no user interaction is needed, and an option pauses at the end so a local operator can see whether it completed.
- It can be built for any platform and architecture Velociraptor supports. "Offline" means no client-server connectivity; the endpoint still needs a running operating system (this is not dead-disk analysis).

## When to use it, and when not
Use it where a server cannot be deployed or reached (not permitted to deploy, internet shut down during an incident, a local admin must run it). Plan ahead: it is often a one-shot collection, so offline collections tend to collect more than strictly needed, and a new artifact needs a rebuilt and redistributed collector. Bundled tools can enlarge the file. No progress or resource telemetry reaches a server.

Do not use it only to collect files for later server-side parsing: add the relevant parsing artifacts to the collector so parsing happens on the endpoint. Do not use it when the endpoint can reach the server; an online client (which can run without being installed) lets you pivot and iterate.

## Embedded vs Generic collector
- Embedded collectors are limited to approximately 80KB of config (compressed before embedding); tools are appended to the file and do not count toward that limit.
- The Generic collector is a platform-independent file (collector config, optionally with a tools bundle) used with any Velociraptor binary, with a hard limit of 100 MB (post-extraction). It is required on macOS, because the released Windows and macOS binaries are code-signed, repacking invalidates the signature, and macOS will refuse to run binaries with invalid signatures. It can also be used on Windows, Linux and others for very large artifacts or one cross-platform collector.

## Securing the container
The zip may hold sensitive data and travels outside Velociraptor's control, so protect it. Schemes:
- X.509 (recommended): a long random password is generated per collection and encrypted with the server's certificate (embedded in the collector) or another certificate you provide. The unencrypted password is discarded; only the matching private key recovers it. If the server's certificate is used, the server decrypts automatically on import.
- PGP: same idea with a PGP public key; not recommended, available where PGP/GPG is mandated; no automatic decryption on import.
- Fixed password: embedded in the collector, so anyone with the binary can extract it; not recommended.
- None: avoid except in a lab or training environment.

Zip file names stay visible even with AES, so Velociraptor puts the data in `data.zip` inside an outer zip and protects that; the outer zip also holds an unprotected `metadata.json` with the encrypted password and the scheme.

## Concurrency
Artifacts are collected in effectively random order that cannot be changed, 2 at a time by default. Change it in the GUI builder or with `OptConcurrency` in the spec file; more concurrency is not necessarily faster because collectors run without resource limits by default.

## Import and analyse
Collection containers use a defined structure so a server can import them as if collected by a normal client, then query them like any client collection. The page points to its "Working With Offline Collection Data" section for importing and for working with the data without importing. Hash the zip on receipt and keep the server private key safe, since it is the only way to recover the X.509 password.

## Checked
Confirmed against the Velociraptor Offline Collections page: what an offline collector is and does, the trade-offs and "don't use" guidance, the embedded (about 80KB) and Generic (100 MB) limits and the macOS signing reason, the encryption schemes and the data.zip/metadata.json layout, and the default concurrency of 2. Removed the specific artifact names (Windows.KapeFiles.Targets, Windows.Memory.Acquisition and others), the GUI build path and `Server.Utils` names, the command line example, the runtime and size figures and the AV/EDR and raw-NTFS gotchas, none of which that page states; the artifact reference index page was an unreadable stub. Hashing on receipt is general practice.

Method: docs-only read of cited pages, 2026-11-08
