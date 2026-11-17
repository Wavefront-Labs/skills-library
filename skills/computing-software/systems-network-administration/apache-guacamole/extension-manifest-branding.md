---
id: computing-software.systems-network-administration.apache-guacamole.extension-manifest-branding
name: extension-manifest-branding
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, extensions, guac-manifest-json, branding, themes, css, translations, html-patch, guacamole-ext, event-listeners]
level: advanced
status: docs-checked
description: "Package a Guacamole extension and brand the UI: guac-manifest.json fields, CSS/JS/HTML patch/translations/resources, listeners, load order and the extensions directory."
sources:
  - https://guacamole.apache.org/doc/gug/guacamole-ext.html
  - https://guacamole.apache.org/doc/gug/event-listeners.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extension manifest and branding

An extension is a `.jar` with `guac-manifest.json` at its root (other library jars either in `GUACAMOLE_HOME/lib/` or at the archive root). Install into `GUACAMOLE_HOME/extensions/` and restart Tomcat.

Manifest fields: `guacamoleVersion` (required; `"*"` bypasses version checks and should only be used for basic theming or branding), `name` (required; logged when the extension loads), `namespace` (required, unique; static resources served under it), `authProviders`, `listeners`, `js` (key is `js`), `css`, `html`, `translations`, `resources` (path to MIME type, served at `app/ext/<namespace>/<path>`).

Branding example:
```json
{
  "guacamoleVersion": "1.6.0",
  "name": "Acme Branding",
  "namespace": "acme-branding",
  "css": ["theme.css"],
  "html": ["loginNotice.html"],
  "translations": ["translations/en.json"],
  "resources": {"images/logo.png": "image/png"}
}
```
- Strings: a translation for an existing language code overrides its strings.
- HTML patches use `<meta name="NAME" content="SELECTOR">` with NAME one of `before`, `after`, `replace`, `before-children`, `after-children`, `replace-children`.
- Reference example: `doc/guacamole-branding-example` in guacamole-client.

Event listeners: implement `org.apache.guacamole.net.event.listener.Listener.handleEvent(Object)`, filter with `instanceof` (e.g. `AuthenticationSuccessEvent`), and register class names in `listeners`. Throwing a `GuacamoleException` on a vetoable event cancels the action. Build with Maven using guacamole-ext as `provided`.

Authentication providers from all extensions are polled in filename order (set `extension-priority` to change).

Verify: the log shows `Extension "NAME" loaded.` after a Tomcat restart and the UI shows the change.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages guacamole-ext and event-listeners: manifest location at the archive root, all manifest properties and the three required ones, relative paths, translation override behaviour, resources served at app/ext/NAMESPACE/PATH, the six HTML patch meta names, the doc/guacamole-branding-example directory, Listener.handleEvent with instanceof checks, vetoing by throwing GuacamoleException, Maven with guacamole-ext as provided, installation into GUACAMOLE_HOME/extensions with a Tomcat restart, the extension-loaded log line, and lexicographic filename polling of authentication providers. Changed: stated that name is required and when the version wildcard is appropriate.

Method: documentation only; no commands were run.
