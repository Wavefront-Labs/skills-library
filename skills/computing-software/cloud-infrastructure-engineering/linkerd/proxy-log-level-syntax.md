---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-log-level-syntax
name: proxy-log-level-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, proxy, logging, directives, reference]
level: practitioner
status: docs-checked
description: "Write proxy log directives and know the four places the proxy log level can be configured."
sources:
  - https://linkerd.io/2.19/reference/proxy-log-level/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The proxy log level can be set in four ways:

- the `LINKERD_PROXY_LOG` environment variable
- the `--proxy-log-level` flag of `linkerd install`, `inject` and `upgrade`
- the `config.linkerd.io/proxy-log-level` annotation, which sets `LINKERD_PROXY_LOG` on the injected sidecar
- the endpoint on the admin port of a running proxy

The value is a comma-separated list of directives, following the `env_logger` crate syntax. Each directive is one of:

- a level, which sets the global level: `trace`, `debug`, `info`, `warn` or `error`
- a module path such as `foo` or `foo::bar::baz`
- a module path, an equals sign and a level, such as `foo=warn` or `foo::bar::baz=debug`, which sets the level for that module only

A module path is one or more module names separated by `::`. A module name starts with a letter and contains alphanumeric characters and `_`.

Combine directives to keep noise down. For example, a global `warn` with one noisier module:

```yaml
annotations:
  config.linkerd.io/proxy-log-level: warn,linkerd=debug
```

The same string is accepted by the admin endpoint:

```bash
curl -v --data 'warn,linkerd=debug' -X PUT localhost:4191/proxy-log-level
```

Prefer the narrowest module that explains the problem, because every enabled level costs proxy throughput.

## Checked

2026-11-08. Read in full against the Linkerd 2.19 docs source (markdown in linkerd/website) of https://linkerd.io/2.19/reference/proxy-log-level/. Confirmed the four configuration routes and the directive syntax. Nothing was removed.

Method: documentation only; no commands were run.
