---
id: computing-software.software-engineering.nim.private-and-vcs-packages
name: private-and-vcs-packages
category: computing-software
field: software-engineering
product: nim
tags: [private-and-vcs-packages, nimble-publishing, private-package, fork, git-url, nimble-develop, nimble-path, vendor, local-override, nim]
level: advanced
status: docs-checked
description: "Depend on VCS, local and private Nimble packages: requires with URLs, commit pins, file:// paths, develop mode, nimble.ini PackageList, cloneUsingHttps."
sources:
  - https://github.com/nim-lang/nimble
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/create-packages.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/use-packages.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private and VCS packages

Goal: depend on code outside the public list.

- Direct URL requirement: `requires "https://github.com/user/pkg#5a54b5e"` (a commit), `requires "https://github.com/user/pkg >= 2.0.0"`, or `requires "foobar#head"`. Git and Mercurial are supported; versions come from tags; `?subdir=` selects a subdirectory.
- Local: `requires "file://./libs/myutil"`.
- Develop mode: `nimble develop -a <path>` (`--add`) links a local checkout; state lives in `nimble.develop`, which is user specific and not committed.
- Custom registries: `nimble.ini` (under `~/.config/nimble/`) with `[PackageList]` entries having `name` and `url` or `path`. The `cloneUsingHttps` option controls clone protocol.

Gotchas:
- Use placeholder URLs in docs, never real private ones.

Verify: `nimble install` resolves the dependency.

## Checked

2026-11-03. Confirmed in the Nimble README and guide (requires forms, file://, develop, nimble.ini, cloneUsingHttps). Removed: token/ssh advice, `vendor/` and `--path:vendor/lib` recipes, the `develop -a:path` syntax, and a real-looking private URL.
Method: documentation only; no commands were run.
