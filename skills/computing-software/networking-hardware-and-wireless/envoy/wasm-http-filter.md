---
id: computing-software.networking-hardware-and-wireless.envoy.wasm-http-filter
name: wasm-http-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, wasm, proxy-wasm, wasm-filter, wasm-service, vm, plugin]
level: practitioner
status: docs-checked
description: "Run an HTTP filter as a Wasm plugin in Envoy, with the experimental status, Windows limit and a local-binary configuration."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/wasm_filter.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/advanced/wasm.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/other_features/wasm.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wasm http filter
The HTTP Wasm filter implements an HTTP filter with a Wasm plugin. The docs mark it experimental ("configuration structures are likely to change") and it is not supported on Windows. A plugin can also run as an upstream filter. The docs' example loads the Wasm binary from local disk; remote fetching and a Wasm service (for background tasks) are covered in the related pages.

Typical shape (the docs include the full sandbox example in `start/sandboxes`):
```yaml
http_filters:
- name: envoy.filters.http.wasm
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.wasm.v3.Wasm
    config:
      name: my_plugin
      vm_config:
        runtime: envoy.wasm.runtime.v8
        code: { local: { filename: /etc/envoy/plugin.wasm } }
- name: envoy.filters.http.router
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```
The docs list `envoy.wasm.runtime.v8` and `envoy.wasm.runtime.wamr` among the runtimes.

Gotchas: place it before the router filter. On a fatal VM error the plugin fails closed by default (for example an HTTP 503) or fails open by bypassing the filter; `fail_open` is deprecated in favour of `failure_policy`. Verify with the plugin's own log output.

## Checked

2026-11-03. Confirmed against: wasm_filter.rst, wasm.rst and wasm.proto (experimental, Windows, runtimes, failure policy). Removed or corrected: the latency claim, the extension list advice and the stats filter step; fail_open is now noted as deprecated.

Method: documentation only; no commands were run.
