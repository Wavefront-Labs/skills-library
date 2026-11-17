---
id: computing-software.web-development.hugo.security-policy
name: security-policy
category: computing-software
field: web-development
product: hugo
tags: [security, allowlist, exec-allow, http-urls, node-permissions]
level: advanced
status: docs-checked
description: "Hugo's security policy: allowlists for exec, environment, remote URLs and Node permissions, allowContent, inline shortcodes, and ! negation rules."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hugo's built-in policy restricts `os/exec`, remote communication and similar operations through allowlists. Access is restricted by default; a build using something outside the list fails with a detailed message.

- `allowContent` (new in 0.162.0): regular expressions for media types allowed in `content`. Org Mode (`text/org`) and HTML (`text/html`) are denied by default.
- `enableInlineShortcodes`: default `false`.
- `exec.allow`: executables Hugo may run. `exec.osEnv`: OS environment variables Hugo may read.
- `funcs.getenv`: variables visible to `os.Getenv`.
- `http.methods`, `http.mediaTypes`, `http.urls`: what `resources.GetRemote` may do. The default `urls` denies IP addresses and `localhost` and rejects non-public resolved addresses; overriding `http.urls` disables that validation.
- `http.proxyFromEnvironment` (new in 0.166.0): default `false`.
- `node.permissions` (new in 0.161.0): Node tools run with `--permission` unless `disable` is true; `allowRead`, `allowWrite`, `allowAddons`, `allowChildProcess` and `allowWorker` open specific access.

Negation (new in 0.161.0): prefix a pattern with `!` and one space to deny. Deny rules win. A list of only deny rules allows everything else; an empty list rejects everything; `none` disables the feature.

```toml
[security.http]
urls = ['.*', '! ^https?://evil\.example\.org']
```

Environment override:

```sh
export HUGO_SECURITY_HTTP_URLS=none
```

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure security: every allowlist key listed (with the version notes 0.161.0, 0.162.0 and 0.166.0), the default-denied Org Mode and HTML media types, the `http.urls` default validation and its disabling on override, the Node permission flags, the negation rules and the `HUGO_SECURITY_HTTP_URLS` override. Nothing removed.

Method: documentation only; no commands were run.
