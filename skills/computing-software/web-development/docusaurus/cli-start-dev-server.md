---
id: computing-software.web-development.docusaurus.cli-start-dev-server
name: cli-start-dev-server
category: computing-software
field: web-development
product: docusaurus
tags: [docusaurus-start, dev-server, https, host-flag, poll]
level: practitioner
status: docs-checked
description: "Run docusaurus start: port, host, locale, polling, HTTPS options with mkcert or a self-signed certificate, and what does not work in development."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`docusaurus start [siteDir]` serves a local preview using Webpack Dev Server.

| Option | Default | Use |
| --- | --- | --- |
| `--port` | `3000` | dev server port |
| `--host` | `localhost` | `--host 0.0.0.0` makes it reachable externally |
| `--locale` | | site locale to use |
| `--hot-only` | `false` | Hot Module Replacement without page refresh as a fallback on build failures |
| `--no-open` | `false` | do not open the browser |
| `--poll [ms]` | `false` | poll files where watching does not work |
| `--no-minify` | `false` | skip minifying JS/CSS |
| `--config` | | path to the config file |

Some functionality, for example anchor links, does not work in development but does in production.

Behind a forwarded port (such as GitHub Codespaces):

```sh
npm run start -- --host 0.0.0.0
```

HTTPS with a self-signed certificate:

```sh
npm run start -- --https
```

HTTPS with mkcert: run `mkcert localhost`, then `mkcert -install` and restart the browser, then:

```sh
npm run start -- --ssl-cert localhost.pem --ssl-key localhost-key.pem
```

Passing both `--ssl-cert` and `--ssl-key` implies HTTPS.

## Checked

2026-11-04: read the Docusaurus CLI page in full. Confirmed the start option table, the anchor-link caveat, the --host 0.0.0.0 example, the --https and mkcert steps and the implied HTTPS rule. Nothing removed.

Method: documentation only; no commands were run.
