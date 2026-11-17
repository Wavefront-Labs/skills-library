---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-php
name: opentelemetry-operator-instrumentation-php
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, php, otel-php-api-version, zts, inject-php, php-platform]
level: practitioner
status: docs-checked
description: "Inject PHP auto-instrumentation by setting the PHP API version, glibc or musl platform and ZTS thread safety annotations to match the runtime image."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/php.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PHP auto-instrumentation annotations

PHP injection requires matching the instrumentation to the PHP runtime. The annotations:

- `instrumentation.opentelemetry.io/inject-php`: `true` or `false`.
- `instrumentation.opentelemetry.io/otel-php-api-version`: one of `20250925`, `20240924`, `20230831`, `20220829`, `20210902`. No default is listed, so set it.
- `instrumentation.opentelemetry.io/otel-php-platform`: `glibc` (default) or `musl`.
- `instrumentation.opentelemetry.io/otel-php-thread-safety`: `non-zts` (default) or `zts` (Zend Thread Safety).

The API version maps to the PHP release of the application:
- `20250925` for PHP 8.5.x
- `20240924` for PHP 8.4.x
- `20230831` for PHP 8.3.x
- `20220829` for PHP 8.2.x
- `20210902` for PHP 8.1.x

Example:

```
instrumentation.opentelemetry.io/inject-php: "true"
instrumentation.opentelemetry.io/otel-php-api-version: "20240924"
instrumentation.opentelemetry.io/otel-php-platform: "musl"
instrumentation.opentelemetry.io/otel-php-thread-safety: "zts"
```

The platform and thread-safety annotations are optional and can be omitted for glibc, non-ZTS PHP. Choose values that match the PHP runtime in your image.

Operator side: the configuration reference lists `enable-php-instrumentation` / `ENABLE_PHP_AUTO_INSTRUMENTATION` with default false, so enable it before using these annotations.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/languages/php.md: the four annotations and their valid values and defaults, the API version to PHP release mapping (8.1 to 8.5), and optional platform and thread-safety annotations. Confirmed against docs/reference/configuration.md: `enable-php-instrumentation` default false. Removed the unconfirmed remark about wrong extension builds and image tag conventions.

Method: documentation only; no commands were run.
