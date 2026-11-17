---
id: computing-software.web-development.hugo.build-and-serve-commands
name: build-and-serve-commands
category: computing-software
field: web-development
product: hugo
tags: [hugo-build, hugo-server, livereload, drafts, clean-destination]
level: intro
status: docs-checked
description: "Use hugo build and hugo server, publish drafts, future and expired content with -D -E -F, clean stale files from public, and navigate to changed pages."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/getting-started/usage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
hugo help
hugo server --help
hugo build
hugo server
```

- `hugo build` publishes to `public`; change it with `--destination` or `publishDir`.
- Hugo does not clear `public`, so stale draft, future or expired output may linger. Use `--cleanDestinationDir` or the `cleanDestinationDir` setting.
- By default Hugo skips content when `draft` is true, `date` or `publishDate` is in the future, or `expiryDate` is in the past.
- Override with `-D` (`--buildDrafts`), `-E` (`--buildExpired`) and `-F` (`--buildFuture`). Setting these in project configuration can cause unwanted results.
- Descendants of draft, future or expired branch pages are still published. Use the `cascade` front matter field to pass build options to them.

`hugo server` serves at `http://localhost:1313/`, watches for changes and refreshes the browser with LiveReload (injected JavaScript over web sockets, no configuration).

```sh
hugo server --navigateToChanged
```

`--navigateToChanged` sends the browser to the page you last modified.

Most users deploy from CI/CD after a Git push, typically without `public` in the repository.

## Checked

2026-11-04: commands, public directory and cleanDestinationDir behaviour, draft/future/expired rules, -D -E -F flags, cascade note, LiveReload and --navigateToChanged confirmed against the Hugo docs Basic usage page. Nothing removed.

Method: documentation only; no commands were run.
