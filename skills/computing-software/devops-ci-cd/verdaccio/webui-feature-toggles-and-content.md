---
id: computing-software.devops-ci-cd.verdaccio.webui-feature-toggles-and-content
name: webui-feature-toggles-and-content
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [web-ui-options, footer, search, showsearch, pkgmanagers, custom-scripts]
level: practitioner
status: docs-checked
description: "Control web UI buttons and content: showSearch, showUplinks, showRaw, pkgManagers, login, footer, poweredBy, help welcome card, and injected scripts."
sources:
  - https://verdaccio.org/docs/webui/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
web:
  login: true
  showSearch: true
  showInfo: true
  showSettings: true
  showFooter: true
  showDownloadTarball: true
  showUplinks: true
  showRaw: true
  hideDeprecatedVersions: false
  showPackageListToolbar: true
  pkgManagers: [npm, yarn, pnpm, bun]
  footer: 'Run by the platform team · [Status](https://status.my.company.com)'
  poweredBy: false
  help: |
    ## Platform registry
    Run `npm config set registry {{registryUrl}}` before publishing.
```
Notes:
- `showSearch: false` also disables `/-/verdaccio/data/search` (404); the npm search API is unaffected.
- `login: false` also disables the web login endpoints.
- `pkgManagers` defaults to yarn, pnpm, npm, bun; a registry that sets it keeps exactly that list.
- `footer` and `poweredBy` take markdown (images max 32px high; raw HTML not rendered). `showFooter: false` hides everything.
- `help` replaces the empty-registry welcome card; `{{registryUrl}}` is substituted.
- `showPackageListToolbar` is on by default in 7.x, off in 6.x.
- Inject tags with `metaScripts`, `scriptsBodyBefore` (misspelled `scriptsbodyBefore` also accepted) and `scriptsBodyAfter`.
- `html_cache` defaults to true.

## Checked

Confirmed against the Web Configuration page: each show* toggle and login, the showSearch 404 on the web search endpoint with npm search unaffected, pkgManagers defaults and exact-list behaviour, markdown footer and poweredBy with the 32px image limit and no raw HTML, showFooter hiding everything, help welcome card with registryUrl substitution, showPackageListToolbar defaults on 7.x and 6.x, metaScripts and scriptsBodyBefore or After injection with the misspelled variant accepted, and html_cache default. No changes needed.

Method: docs-checked 2026-11-09 against website/docs/web.md in verdaccio/website (source of verdaccio.org/docs/webui/), read in full.
