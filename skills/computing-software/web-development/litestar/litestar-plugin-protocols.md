---
id: computing-software.web-development.litestar.litestar-plugin-protocols
name: litestar-plugin-protocols
category: computing-software
field: web-development
product: litestar
tags: [litestar, plugins, init-plugin, serialization-plugin, di-plugin, receive-route-plugin, app-config]
level: practitioner
status: docs-checked
description: "Write Litestar plugins by implementing InitPlugin, SerializationPlugin, DIPlugin or ReceiveRoutePlugin and passing them in the plugins argument."
sources: [https://docs.litestar.dev/latest/usage/plugins/index.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar plugin protocols

Goal: extend the framework with a class satisfying a plugin protocol, then list it in `Litestar(plugins=[...])`.

## Method

The four plugin base classes (`InitPlugin`, `SerializationPlugin`, `DIPlugin`, `ReceiveRoutePlugin`) come from `litestar.plugins`; `AppConfig` is in `litestar.config.app` and `BaseRoute` in `litestar.routes`.

**InitPlugin**: customize app initialization (dependencies, route handlers, middleware). Implement `on_app_init(self, app_config: AppConfig) -> AppConfig`. It runs after any `on_app_init` hooks, and plugins run in the order given in `plugins`, so document whether yours must come before or after others.

```python
class MyPlugin(InitPlugin):
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.dependencies["name"] = Provide(get_name, sync_to_thread=False)
        app_config.route_handlers.append(route_handler)
        return app_config

app = Litestar(plugins=[MyPlugin()])
```

**SerializationPlugin**: serialization for types the framework does not support. Implement `supports_type(self, field_definition: FieldDefinition) -> bool` and `create_dto_for_type(self, field_definition: FieldDefinition) -> type[AbstractDTO]`. At startup, if a data or return annotation is unsupported, the plugin supports it, and no `dto`/`return_dto` is defined, the plugin builds the DTO. The docs example unwraps `list[Company]` style collections, caches one DTO per model in `_type_dto_map`, and builds `DataclassDTO[annotation]`.

**DIPlugin**: injection for callables with unknown signatures (e.g. Pydantic `BaseModel` classes). Implement `has_typed_init(self, type_)` and `get_typed_init(self, type_)` returning `(Signature, annotations dict)`:

```python
class MyDIPlugin(DIPlugin):
    def has_typed_init(self, type_: Any) -> bool:
        return issubclass(type_, MyBaseType)

    def get_typed_init(self, type_: Any) -> tuple[Signature, dict[str, Any]]:
        signature = Signature([Parameter(name="param", kind=Parameter.POSITIONAL_OR_KEYWORD)])
        return signature, {"param": FromQuery[str]}
```

**ReceiveRoutePlugin**: implement `receive_route(self, route: BaseRoute) -> None`, called as routes are registered during app initialization, after routes are created and before the app starts (documentation, route validation, statistics).

```python
class RouteLoggerPlugin(ReceiveRoutePlugin):
    def receive_route(self, route: BaseRoute) -> None:
        print(f"Route registered: {route.path} [{', '.join(route.methods)}]")
```

## Verify

For the InitPlugin example, `GET /` returns `{"hello": "world"}`; for the DIPlugin example, `GET /?param=hello` returns `hello`.

## Checked

2026-11-07. Read the full cited page(s) (usage/plugins/index.html) and the example files they include, and confirmed the claims in this skill against that text. Replaced the claim that all imports come from litestar.plugins with the per-module locations (AppConfig, BaseRoute).

Method: documentation only; no commands were run.
