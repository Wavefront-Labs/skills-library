---
id: computing-software.collaboration-platform-administration.matrix-synapse.writing-a-synapse-module
name: writing-a-synapse-module
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, modules, module-api, parse-config, web-resource, callbacks, caching, python]
level: advanced
status: docs-checked
description: "Structure of a Synapse Python module: ModuleApi, parse_config, registering callbacks and web resources under /_synapse/client, multi-module ordering, and the cached decorator."
sources:
  - https://element-hq.github.io/synapse/latest/modules/writing_a_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A module is a Python class that uses `synapse.module_api.ModuleApi` to interact with the homeserver. When instantiated it receives its parsed configuration (a dictionary) and a `ModuleApi` instance. It can register callbacks Synapse calls on specific operations, and web resources attached to Synapse's web server.

**Configuration.** An optional static `parse_config(config: dict)` method receives the YAML dictionary, may convert values (for example a duration string such as "5d" into milliseconds), and returns what is passed to `__init__`. Raise `synapse.module_api.errors.ConfigError` for invalid settings.

**Web resources.** `ModuleApi.register_web_resource(path, resource)` takes the full absolute path and a Twisted `IResource`. Synapse does not allow resources on several sub-paths of `/_matrix` (anything under `/_matrix/client`, for example), so register under `/_synapse/client`, such as `/_synapse/client/my_super_module/say_hello`. Only one resource per path; if several modules claim the same path, the one earlier in the config wins. Modules must register web resources in `__init__`.

**Callbacks.** Each category has a `register_[...]_callbacks` method, and callbacks are passed as keyword arguments named after the callback. They must be asynchronous unless the docs say otherwise. A module need not implement every callback in a category. With several modules, order in the `modules` section can limit what each registers. If a callback returns a value that makes the operation fail (an event denied, say), Synapse fails the operation and skips later callbacks.

**Caching** (Synapse 1.74.0 and later). Decorate a function with `@cached()` from `synapse.module_api`, register it with `ModuleApi.register_cached_function` at init, and invalidate entries via `ModuleApi.invalidate_cache(function, (key,))`.

## Checked

2026-11-09. Confirmed against the Synapse writing-a-module page: ModuleApi, parse_config and ConfigError, web resource rules under /_synapse/client, callback registration and ordering, and the caching decorator (added in 1.74.0). Nothing removed.

Method: docs-checked 2026-11-09 against element-hq.github.io/synapse/latest/modules/writing_a_module.html (whole page).

