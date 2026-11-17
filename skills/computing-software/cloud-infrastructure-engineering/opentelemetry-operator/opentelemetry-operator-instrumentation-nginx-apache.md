---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-nginx-apache
name: opentelemetry-operator-instrumentation-nginx-apache
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, nginx, apache-httpd, otel-webserver-module, configpath, webserver-attrs]
level: practitioner
status: docs-checked
description: "Configure web server auto-instrumentation for Nginx and Apache HTTPD, including supported versions, config paths, the conf.d include requirement and module attributes."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/nginx.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/apache-httpd.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nginx and Apache HTTPD instrumentation

Annotations: `instrumentation.opentelemetry.io/inject-nginx: "true"` and `instrumentation.opentelemetry.io/inject-apache-httpd: "true"`. Nginx is off by default in the operator (`enable-nginx-instrumentation`); Apache HTTPD is on.

Apache HTTPD. By default the instrumentation assumes httpd 2.4 and the configuration directory `/usr/local/apache2/conf`, as in the official httpd image. Override in the Instrumentation:

```yaml
spec:
  apacheHttpd:
    image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-apache-httpd:1.0.4-3
    version: "2.2"
    configPath: /your-custom-config-path
    attrs:
      - name: ApacheModuleOtelMaxQueueSize
        value: "4096"
```

Nginx. Supported versions at the time of the doc: 1.22.0, 1.23.0 and 1.23.1. The config file is expected at `/etc/nginx/nginx.conf`; change it with `configFile`. The instrumentation also expects a `conf.d` directory beside the config file and an `include <config-file-dir-path>/conf.d/*.conf;` directive inside the `http { ... }` block, as in the default Nginx configuration.

```yaml
spec:
  nginx:
    configFile: /my/custom-dir/custom-nginx.conf
    attrs:
      - name: NginxModuleOtelMaxQueueSize
        value: "4096"
```

The pages point to the `otel-webserver-module` project for the list of valid `attrs`. Neither server supports init containers, and in multi-instrumentation use the `apache-httpd-container-names` annotation and `inject-nginx-container-names` (as spelled in the docs).

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/languages/nginx.md and apache-httpd.md: the annotations, Nginx versions 1.22.0, 1.23.0 and 1.23.1, `/etc/nginx/nginx.conf` and `configFile`, the `conf.d` include requirement, Apache httpd 2.4 and `/usr/local/apache2/conf` defaults, `version`, `configPath`, `attrs`, and the `otel-webserver-module` pointer. Confirmed against feature-gates.md (Nginx off, Apache HTTPD on), init-containers.md (neither supported) and multi-instrumentation.md (container-names spellings). The Nginx page example shows an apache-httpd image name, which looks like a documentation slip, so the skill omits an image for Nginx. Removed the unconfirmed project owner name.

Method: documentation only; no commands were run.
