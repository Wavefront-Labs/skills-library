---
id: computing-software.data-engineering.kestra.namespace-files
name: namespace-files
category: computing-software
field: data-engineering
product: kestra
tags: [namespace-files, read-function, include-exclude, downloadfiles, kestractl]
level: practitioner
status: docs-checked
description: "Store scripts and configs as Kestra namespace files and use them via read(), the namespaceFiles property with include and exclude, and the upload tasks."
sources:
  - https://kestra.io/docs/concepts/namespace-files
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Namespace files are scripts, queries and configs attached to a namespace, usable by any flow in it. Add them from the editor's Files tab, Git tasks (`PushNamespaceFiles`, `SyncNamespaceFiles`), the GitHub `deploy-namespace-files` action, Terraform `kestra_namespace_file`, or:

```bash
kestractl nsfiles upload prod ./scripts --override
```

Use in flows:

- `read('example.txt')` returns contents as a string. Use for script or SQL properties, not for `Commands` tasks needing a path on disk. It works without `namespaceFiles.enabled`.
- `namespaceFiles` mounts files into the working directory.

```yaml
namespaceFiles:
  enabled: true
  include:
    - file1.txt
    - file3.json
```

Also `exclude`, `namespaces` (last listed wins), `ifExists` (`OVERWRITE` default, `FAIL`, `WARN`, `IGNORE`), `folderPerNamespace`.

Patterns: no leading `/` means prefixed with `**/` (recursive); leading `/` matches from the namespace root; `glob:` and `regex:` force a type. A pattern already containing `**` gets doubled; use `/my_dir/**`.

Tasks `UploadFiles`, `DownloadFiles`, `DeleteFiles` move files; `DownloadFiles` output is read as `outputs.namespace.files['/example.ion']`.

Revisions: the first upload is version 0; later ones add suffixes such as `.v1`.

## Checked

2026-11-04. Confirmed against the Kestra Namespace Files docs page: the ways to add files, read() versus namespaceFiles, the namespaceFiles attributes and ifExists values, the pattern rules, the namespace tasks and the revision numbering. Nothing removed.

Method: documentation only; no commands were run.
