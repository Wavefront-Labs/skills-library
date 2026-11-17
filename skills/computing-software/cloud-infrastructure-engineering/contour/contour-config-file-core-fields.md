---
id: computing-software.cloud-infrastructure-engineering.contour.contour-config-file-core-fields
name: contour-config-file-core-fields
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [config-file, configmap, contour-yaml, accesslog, default-http-versions, enableexternalnameservice, disablepermitinsecure, featureflags]
level: practitioner
status: docs-checked
description: "Contour config file top-level fields and defaults: access log format/level, HTTP versions, ExternalName, permitInsecure, featureFlags, compression, server header."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour configuration file: core fields

The file is optional; without it Contour uses defaults. It is passed via `--config-path`, usually from a ConfigMap (`contour.yaml` key in `projectcontour/contour`).

Key top-level fields and defaults:
- `accesslog-format`: `envoy` (default) or `json`; `accesslog-format-string` supplies a custom Envoy format; `json-fields` picks JSON fields.
- `accesslog-level`: `info` (all requests), `error` (300+ only), `critical` (500+ only), `disabled`.
- `default-http-versions`: defaults to `HTTP/1.1` and `HTTP/2`.
- `disableAllowChunkedLength` (false): disables stripping Content-Length when Transfer-Encoding is chunked.
- `disableMergeSlashes` (false): turn off Envoy merge_slashes path normalisation.
- `serverHeaderTransformation`: `overwrite` (default), `append_if_absent`, `pass_through`.
- `disablePermitInsecure` (false): when true, `permitInsecure` in HTTPProxy is ignored.
- `enableExternalNameService` (false): ExternalName processing; has security implications (see the linked advisory).
- `ingress-status-address`, `envoy-service-name` (`envoy`), `envoy-service-namespace` (`projectcontour`) determine status addresses.
- `featureFlags`: list of toggles, e.g. `useEndpointSlices`.
- `compression.algorithms`: `gzip` default, also `brotli`, `zstd`; an empty list disables compression. The older single `algorithm` field is deprecated and mutually exclusive.
- `kubernetesClientQPS`, `kubernetesClientBurst`.

Sub-blocks (`tls`, `timeouts`, `cluster`, `network`, `listener`, `gateway`, `policy`, `rateLimitService`, `metrics`) have their own skills.

## Checked

2026-11-04. Confirmed against the Contour Configuration Reference (configuration.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
