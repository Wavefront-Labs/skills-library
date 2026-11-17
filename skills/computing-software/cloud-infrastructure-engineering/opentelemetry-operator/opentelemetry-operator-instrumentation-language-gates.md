---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-language-gates
name: opentelemetry-operator-instrumentation-language-gates
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, instrumentation-gates, enable-go-instrumentation, enable-nginx-instrumentation, enable-multi-instrumentation, cli-flags]
level: practitioner
status: docs-checked
description: "Turn language auto-instrumentation on or off with enable-*-instrumentation flags; Go, Nginx and Ruby are off by default and PHP appears only in the configuration reference."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/feature-gates.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/configuration.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/ruby.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable or disable languages for auto-instrumentation

The operator decides which languages an `Instrumentation` resource may instrument through CLI flags. A default-on language only needs its flag when you want to disable it (pass `=false`). Defaults per the feature-gates page:

- Java `enable-java-instrumentation`: true
- NodeJS `enable-nodejs-instrumentation`: true
- Python `enable-python-instrumentation`: true
- DotNet `enable-dotnet-instrumentation`: true
- ApacheHttpD `enable-apache-httpd-instrumentation`: true
- Go `enable-go-instrumentation`: false
- Nginx `enable-nginx-instrumentation`: false
- Ruby `enable-ruby-instrumentation`: false

The configuration reference adds environment variables (for example `ENABLE_GO_AUTO_INSTRUMENTATION`, `ENABLE_NGINX_AUTO_INSTRUMENTATION`, `ENABLE_RUBY_AUTO_INSTRUMENTATION`) and lists `enable-php-instrumentation` / `ENABLE_PHP_AUTO_INSTRUMENTATION` with default false. The Ruby page confirms: start the operator with `--enable-ruby-instrumentation=true` or `ENABLE_RUBY_AUTO_INSTRUMENTATION=true`.

`enable-multi-instrumentation` (default true) governs multi-container, multi-language injection; set it to false to disable.

Important distinction from the page itself: these are CLI flags for instrumentation languages, a separate mechanism from the operator's general feature gates registered in `pkg/featuregate` and toggled with `--feature-gates`.

If an annotation for a disabled language does nothing, check these flags first.

## Checked

2026-11-04. Confirmed against docs/reference/feature-gates.md: the eight language flags and their defaults (Java, NodeJS, Python, DotNet and ApacheHttpD true; Go, Nginx and Ruby false), the disable-with-false rule, `enable-multi-instrumentation` default true, and the note that these flags are separate from the collector-style feature gates in `pkg/featuregate`. Confirmed against docs/reference/configuration.md: the matching environment variables and `enable-php-instrumentation` with default false (PHP is not in the feature-gates table, so the two pages do not list the same languages). Confirmed against languages/ruby.md: Ruby is disabled by default. Nothing removed.

Method: documentation only; no commands were run.
