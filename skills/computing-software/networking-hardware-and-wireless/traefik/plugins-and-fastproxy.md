---
id: computing-software.networking-hardware-and-wireless.traefik.plugins-and-fastproxy
name: plugins-and-fastproxy
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, plugins, experimental, modulename, yaegi, fastproxy]
level: practitioner
status: docs-checked
description: "Load Traefik plugins from the experimental plugins block and understand the experimental fastProxy switch."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/experimental/plugins.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/experimental/fastproxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# plugins and fastproxy
Experimental features are declared in the install config under `experimental`. Plugins use `experimental.plugins.<name>` with the required `moduleName` and `version`; plugins can add custom middlewares and providers. `experimental.fastProxy` enables a high-performance reverse proxy, with `fastProxy.debug` (default false) for debug mode.

```yaml
experimental:
  plugins:
    rewritebody:
      moduleName: github.com/example/rewritebody
      version: vX.Y.Z
```
Gotchas: the docs mark `plugins` as experimental and subject to change in future releases. `experimental.localPlugins.<name>.moduleName` uses plugins from a local directory without publishing them to the Traefik plugin catalog. The fastProxy page lists limitations, including that tracing and OTEL semconv metrics are not supported for the moment.

## Checked
2026-11-03. Confirmed against the Traefik experimental plugins and fastProxy reference pages: `moduleName` and `version`, `localPlugins`, the plugin catalog mention, `fastProxy.debug` and the experimental and limitation warnings. Removed: the claim that plugins are downloaded at startup, the claim that plugin middleware config uses the same name, the version-hedge text and the startup-log Verify step.
Method: documentation only; no commands were run.


