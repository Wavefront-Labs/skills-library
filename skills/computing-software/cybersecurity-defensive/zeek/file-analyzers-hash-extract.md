---
id: computing-software.cybersecurity-defensive.zeek.file-analyzers-hash-extract
name: file-analyzers-hash-extract
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, file-analyzers, file-extraction, file-hash, file-data-event]
level: practitioner
status: docs-checked
description: "Attach file analyzers with Files::add_analyzer: MD5 hashing, extraction to disk, FileDataEvent streaming, auto-attach by MIME type, and enabling or removing analyzers."
sources: ["https://docs.zeek.org/en/current/frameworks/file-analysis.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# file analyzers: hash, extract, stream

Built-in analyzers: `Zeek::FileDataEvent` (content via events), `Zeek::FileEntropy`, `Zeek::FileExtract` (to disk), `Zeek::FileHash`, `Zeek::PE` and `Zeek::X509`.

Attach per file with `Files::add_analyzer(f, Files::ANALYZER_MD5)`, optionally with a `Files::AnalyzerArgs` record. The same analyzer can be added several times with different args. `Files::remove_analyzer` removes one; `Files::enable_analyzer` and `Files::disable_analyzer` act globally.

Hashing plain text files:

```
event file_sniff(f: fa_file, meta: fa_metadata)
    {
    if ( ! meta?$mime_type ) return;
    if ( meta$mime_type == "text/plain" )
        Files::add_analyzer(f, Files::ANALYZER_MD5);
    }
event file_hash(f: fa_file, kind: string, hash: string)
    { print "file_hash", f$id, kind, hash; }
```

Extraction:

```
event file_new(f: fa_file)
    {
    Files::add_analyzer(f, Files::ANALYZER_EXTRACT, [$extract_filename=fmt("file-%04d", ++idx)]);
    }
```

Output goes to `FileExtract::prefix` (normally `./extract_files/`) plus the name. For production see `policy/frameworks/files/extract-all-files.zeek` and the file-extraction package.

Script-level content: files may be huge, so `ANALYZER_DATA_EVENT` with `$stream_event` delivers content incrementally (a `chunk_event` serves protocols without stream semantics). Build running state, such as `sha256_hash_init()` and `sha256_hash_update`, and print in `file_state_remove`.

Auto-attach: `Files::register_for_mime_types` attaches an analyzer to all files of a MIME type; `Files::register_analyzer_add_callback` allows custom logic.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
