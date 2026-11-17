---
id: computing-software.devops-ci-cd.tilt.tilt-api-os-sys-shlex
name: tilt-api-os-sys-shlex
category: computing-software
field: devops-ci-cd
product: tilt
tags: [api-os-sys-shlex]
level: practitioner
status: docs-checked
description: "Tiltfile os, os.path, sys and shlex modules: environment variables, path helpers, argv, and shell-quoting values for local commands."
sources:
  - "https://docs.tilt.dev/api.html#api.os"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# os, sys and shlex in the Tiltfile

Goal: read the environment, handle paths and quote shell arguments safely.

## os

- `os.name`: "posix" (Linux and MacOS) or "nt" (Windows).
- `os.environ`: dict of environment variables, captured each time the Tiltfile begins execution. Supports `dict.get(key, default)` and `dict.items()`.
- `os.getcwd()`: directory of the currently executing Tiltfile; commands the Tiltfile runs use this directory. During `load` or `include`, it is the directory of the loaded Tiltfile.
- `os.getenv(key, default=None)`: value of the variable, or default.
- `os.putenv(key, value)`: takes effect immediately in the Tilt process; new subprocesses inherit it.
- `os.unsetenv(key, value)` (signature as listed on the page; only `key` is documented): deletes the variable for the Tilt process and new subprocesses.

## os.path

- `abspath(path)`: normalized absolute path, relative to the current working directory.
- `relpath(targpath, basepath='')`: path relative to `basepath` (default CWD); raises an error if it cannot be made relative. For a Tiltfile at /code/Tiltfile: `relpath('/code/foo/bar')` is `foo/bar`; `relpath('/code/foo/bar', '/code/foo')` is `bar`; `relpath('/code/foo', '/code/baz')` is `../foo`; `relpath('/code/foo', 'other/path')` is an error.
- `basename(path)`, `dirname(path)`, `join(path, *paths)` (OS-specific separator), `realpath(path)` (resolves symlinks).
- `exists(path)`: true if a file or directory exists; false for a broken symlink or when stat is not permitted. On Tilt v0.18.3 and below it watches the path and reloads the Tiltfile on change; on v0.18.4 and up it does no watching.

## sys

- `sys.argv`: command line arguments passed to Tilt on start; `argv[0]` is the Tilt binary name.
- `sys.executable`: absolute path of the Tilt binary, based on how it was invoked. It may no longer point to a valid binary.

## shlex

`shlex.quote(s)` returns a shell-escaped string safe to interpolate as a single token:

```
mystring = "foo's bar"
# bad - invalid shell, unmatched '
local('docker run -e foo=%s myimage' % mystring)
# good
local('docker run -e foo=%s myimage' % shlex.quote(mystring))
```

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/api.html#api.os (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Changed the `os.unsetenv` entry to the signature the page lists.

Method: documentation only; no commands were run.
