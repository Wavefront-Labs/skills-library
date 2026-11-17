---
id: computing-software.web-development.litestar.litestar-cli-autodiscovery
name: litestar-cli-autodiscovery
category: computing-software
field: web-development
product: litestar
tags: [litestar, cli, autodiscovery, litestar-app, litestar-run, click, cli-plugin]
level: practitioner
status: docs-checked
description: "Install the Litestar CLI, rely on its app autodiscovery order, point it at an app or factory with --app or LITESTAR_APP, and extend it with commands."
sources: [https://docs.litestar.dev/latest/usage/cli.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar CLI and app autodiscovery

Goal: run and manage a Litestar app from the command line.

## Method

- The CLI (click, rich, rich-click) is not installed by default. Its dependencies are in the `cli` extra, which adds uvicorn (needed by `litestar run`) and jsbeautifier. The docs recommend the `standard` extra:

```shell
pip install 'litestar[standard]'
```

- Autodiscovery looks in modules named `app` or `application` (files or directories), in this order: `app.py`, `app/__init__.py`, submodules of `app`, `application.py`, `application/__init__.py`, submodules of `application`.
- Within them it looks for, in order: an object named `app` that is a `Litestar` instance; an object named `application` that is a `Litestar` instance; any `Litestar` instance; a callable named `create_app`; a callable annotated to return a `Litestar` instance.
- Explicit app: `--app` or the `LITESTAR_APP` environment variable, format `<module name>.<submodule>:<app instance or factory>`. If both are set, the CLI option wins.

```bash
litestar --app=my_application.app:create_my_app run
LITESTAR_APP=my_application.app:create_my_app litestar run
```

## Extending the CLI

- Entry points: register a `click.Command` or `click.Group` under the `litestar.commands` entry point group, e.g. `[project.entry-points."litestar.commands"]` with `my_command = "my_litestar_plugin.cli:main"`.
- Plugin: subclass `CLIPlugin` (from `litestar.plugins`) and implement `on_cli_init(self, cli: Group)`, which receives the root click group to add or override commands. Pass it in `Litestar(plugins=[MyPlugin()])`.
- Add a parameter named `app` to a CLI function and the loaded `Litestar` instance is injected when called from a click context.
- `server_lifespan(self, app)` on a `CLIPlugin` (a `@contextmanager` generator) runs code once before the server starts and after it stops, unlike `lifespan`, which runs for each worker. Suited to one-off tasks such as initializing a database.

## Verify

`litestar --help` shows the up-to-date command reference; with the extra installed, `litestar run` is available.

## Checked

2026-11-07. Read the full cited page(s) (usage/cli.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
