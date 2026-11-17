---
id: computing-software.systems-network-administration.syncthing.versioning-external-command
name: versioning-external-command
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, versioning, external-versioning, command]
level: advanced
status: docs-checked
description: "Use Syncthing external versioning to run your own command with %FOLDER_PATH% and %FILE_PATH% before a file is replaced or deleted."
sources: ["https://docs.syncthing.net/users/versioning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External versioning command

## How it runs
With `folder.versioning.type` set to `external`, Syncthing runs `folder.versioning.params.command` just before a file is replaced or deleted by a remote change. The command must remove the file from the folder, otherwise Syncthing reports an error. `fsPath`, `fsType` and `cleanupIntervalS` are ignored for this strategy.

## Placeholders
- `%FOLDER_PATH%` is the folder root.
- `%FILE_PATH%` is the file path relative to the folder.
- Version 2.1.2 and later also exports `$FOLDER_PATH` and `$FILE_PATH` as environment variables.

Example command, with a script that moves the file into an archive tree:

```
/path/to/bin/onlylatest.sh %FOLDER_PATH% %FILE_PATH%
```
```sh
#!/bin/sh
set -eu
mkdir -p "$(dirname "/path/to/archive/$2")"
mv -f "$1/$2" "/path/to/archive/$2"
```

## Safety rules
- Treat paths as untrusted input. Do not assume they are free of special characters.
- Unquoted placeholders are passed as separate arguments. `%FOLDER_PATH%/%FILE_PATH%` joined is also valid.
- Shell wrapping such as `sh -c "..."` is invalid and may be rejected as unsafe.
- If the command path contains spaces, quote it.
- The script needs execute permission (the docs example uses `chmod 755`).

## Checked

2026-11-09. Confirmed against the Syncthing File Versioning page (users/versioning, raw rst from syncthing/docs): external strategy behaviour and the must-remove-the-file rule, %FOLDER_PATH% and %FILE_PATH% meanings, 2.1.2 environment variables, untrusted-path warning, unquoted-argument and shell-wrapping rules, quoting of paths with spaces, ignored fsPath/fsType/cleanupIntervalS, chmod 755 in the example. Removed: nothing (the script is an adapted version of the page example).

Method: documentation only; no commands were run.
