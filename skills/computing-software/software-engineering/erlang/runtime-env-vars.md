---
id: computing-software.software-engineering.erlang.runtime-env-vars
name: runtime-env-vars
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-config, runtime-env-vars]
level: advanced
status: docs-checked
description: "Erlang releases and 12-factor config: sys.config.src and vm.args.src with ${VAR} substitution and defaults at start."
sources:
  - https://rebar3.org/docs/deployment/releases/
  - https://www.erlang.org/doc/apps/kernel/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variables in release config
**Goal:** take deploy-time settings from the environment.

- With OTP 21+ and rebar3 3.6+, `sys_config_src` and `vm_args_src` templates are rendered at runtime, substituting `${VARIABLE}` from the shell environment. Since rebar3 3.14.0 a default can be given as `${VARIABLE:-DEFAULT}`, and `config/sys.config.src` and `config/vm.args.src` are included automatically if they exist.
```erlang
%% config/sys.config.src
[{appname, [{port, ${PORT:-8080}},
            {log_level, ${LOG_LEVEL:-info}},
            {log_root, "${LOG_ROOT:-/var/log/appname}"}]}].
```
```
## config/vm.args.src
-name ${NODE_NAME}
```
- Unquoted `${PORT:-8080}` yields a term (an integer here); quoted `"${LOG_ROOT:-...}"` yields a string. Pick quoting to match the type the code expects.
- For `.src` files `RELX_REPLACE_OS_VARS=true` is not needed. That variable is the older mechanism (before OTP 21 / rebar3 3.6) for plain `vm.args` and `sys.config`, where values are written as `"${PORT}"`.
- Precedence reminder: command-line flags override config-file values, which override the `.app` file.

## Gotchas
- Give every variable a `:-DEFAULT` or validate on boot and crash early; the docs do not describe what an unset variable without a default renders as.
- Secrets in `ps`: prefer files or an environment injected by the orchestrator.

## Self-check
Boot the release with and without the variable and print `application:get_env(appname, port)`.

## Checked
Method: docs-checked 2026-11-09 against the rebar3 Releases page (Environment Variable Replacement section) and the Erlang kernel `config` page (precedence). Dropped the `config_providers` claim, the unset-variable-becomes-empty-string claim and the os:getenv advice, which the pages do not state.
