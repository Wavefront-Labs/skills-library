---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.zeek-file-extraction-and-files-log
name: zeek-file-extraction-and-files-log
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [zeek-file-extraction, zeek, file-extraction-pcap, network-security-monitoring, dfir]
level: advanced
status: docs-checked
description: "Extract files from traffic with Zeek: files.log fields, the file analysis framework, extract and hash analyzers, MIME filtering, and linking files to connections."
sources: ["https://docs.zeek.org/en/master/frameworks/file-analysis.html", "https://docs.zeek.org/en/master/scripts/base/files/extract/main.zeek.html", "https://docs.zeek.org/en/master/scripts/base/frameworks/files/main.zeek.html", "https://docs.zeek.org/en/master/scripts/policy/frameworks/files/hash-all-files.zeek.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zeek file extraction and files.log

**Goal:** Zeek identifies files transferred over HTTP, SMTP, FTP, SMB and other analysed protocols,
logs their metadata and hashes, and can write them to disk - at scale, from live traffic or PCAP.

## files.log key fields
`ts`, `fuid` (file ID), `uid` and `id` (the connection, linking to conn.log/http.log), `source` (HTTP, SMTP, SMB, FTP_DATA),
`mime_type`, `filename`, `total_bytes`, `seen_bytes`, `missing_bytes`, `md5`/`sha1`/`sha256` (when the hash analyzers run),
`extracted` (path when the extract analyzer ran). Since Zeek 5.1 a file seen over several connections produces one
entry per connection, all sharing the same `fuid`; earlier versions logged `conn_uids` in a single entry.

## Extract files
```zeek
# extract.zeek
@load base/files/extract
@load frameworks/files/hash-all-files
redef FileExtract::prefix = "./extract_files/";
event file_sniff(f: fa_file, meta: fa_metadata)
    {
    if ( meta?$mime_type && meta$mime_type in set("application/x-dosexec", "application/zip", "application/vnd.ms-cab-compressed", "application/x-7z-compressed") )
        Files::add_analyzer(f, Files::ANALYZER_EXTRACT);
    }
```
```bash
zeek -C -r capture.pcap extract.zeek
zeek-cut ts uid source mime_type filename sha256 extracted < files.log
```
- `-C` ignores checksum errors (common with offloaded captures).
- Extracted names look like `extract-<last_active>-<source>-<fuid>`; hash them and send to the malware lab. The extract analyzer stops at `FileExtract::default_limit` (100 MB by default) per file.

## Workflow
1. Filter `files.log` for executables, scripts, archives, Office docs with macros.
2. Join `uid` to `http.log` (host, uri, user_agent) or `smtp.log` (mailfrom, rcptto) for context.
3. Check `missing_bytes > 0` (incomplete capture) before relying on hashes.

## Gotchas
- Encrypted protocols (HTTPS, SMB3 encryption) hide files; only cleartext or decrypted traffic yields extractions.
- Extracting everything fills disks; filter by MIME type and size (`FileExtract::default_limit`).

## Verify
Extracted file hashes match files.log values and the source connection is identified.

## Checked

Checked 2026-10-25 against the Zeek sources (Zeek sources (zeek/zeek master, last pushed 2026-10-23: doc/frameworks, tools/zeek-cut, base and policy scripts, event definitions)). Confirmed: `@load base/files/extract`, `FileExtract::prefix` (default `./extract_files/`), `FileExtract::default_limit` (104857600 bytes), the `file_sniff` event with `meta$mime_type`, `Files::add_analyzer(f, Files::ANALYZER_EXTRACT)`, extracted file naming `extract-<last_active>-<source>-<id>`, `frameworks/files/hash-all-files` (MD5, SHA1, SHA256 on all files), MIME types `application/x-dosexec`, `application/zip`, `application/vnd.ms-cab-compressed`, `application/x-7z-compressed` in the shipped signatures, per-connection files.log entries since Zeek 5.1. Corrected: `application/x-msdownload` is not a Zeek signature MIME type and was replaced.

Method: documentation only; no commands were run.
