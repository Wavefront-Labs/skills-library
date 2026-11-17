---
id: computing-software.systems-network-administration.rclone.rclone-remote-path-syntax-and-connection-strings
name: rclone-remote-path-syntax-and-connection-strings
category: computing-software
field: systems-network-administration
product: rclone
tags: [remote-paths, connection-strings, on-the-fly-remotes, quoting, remote-names]
level: practitioner
status: docs-checked
description: "Rclone path forms (local, remote:path, :backend:path), connection-string parameters, quoting rules and valid remote names."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Path forms

- `/path/to/dir` is the local filesystem. Relative paths are relative to the current directory. On Windows only, local paths may use `\`.
- `remote:path/to/dir` is a directory on a configured remote.
- `remote:/path/to/dir` is the same on most backends and the form without the leading slash is preferred. On FTP, SFTP and Dropbox for business the leading `/` means the server root instead of the home directory.
- `:backend:path/to/dir` builds a remote on the fly. All options come from flags or environment, for example `rclone lsd --http-url https://pub.rclone.org :http:`.

## Connection strings

Options can be attached to the remote itself:

```text
remote,parameter=value,parameter2=value2:path/to/dir
:backend,parameter=value:path/to/dir
```

Quote a value containing `:` or `,` with `"` or `'`, and double the quote character to include it. A parameter with no `=value` becomes `=true`, so `:s3,env_auth:` equals `:s3,env_auth=true:`. Use `rclone config string` to convert a remote into a connection string.

The advantage over flags is scoping. `rclone copy --drive-shared-with-me gdrive:file gdrive:` fails because the flag applies to source and destination; `rclone copy "gdrive,shared_with_me:file" gdrive:` works. The parameters only affect the immediate backend, so `shared_with_me` is ignored if you put it on a crypt remote layered over gdrive; address the underlying remote instead.

When flags, environment or connection strings change a remote, rclone adds a hash suffix to its name in logs, such as `s3: detected overridden config - adding "{Srj1p}" suffix`. This keeps cached backends distinct and only shows in logs.

## Remote names

Names are case sensitive; may contain letters, digits, `_`, `-`, `.`, `+`, `@` and space; cannot start with `-` or space or end with space. Since 1.61 any Unicode letters or digits are allowed. Avoid single-letter names on Windows, where `C` is always treated as a drive. If you configure through environment variables the name becomes part of the variable name, which limits usable characters.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
