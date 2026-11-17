---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.custom-authenticator-extension
name: custom-authenticator-extension
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, custom-component, extension, authenticator, go]
level: sme
status: docs-checked
description: "Write an authenticator extension for the Collector in Go and attach it to receivers through the auth setting."
sources:
  - https://opentelemetry.io/docs/collector/extend/custom-component/extension/authenticator/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An authenticator is an ordinary extension that also implements one or more authentication interfaces. Server authenticators are used with receivers to intercept HTTP and gRPC requests; client authenticators are used with exporters to add authentication data to outgoing requests. One extension may implement both. The API reference is the configauth package on pkg.go.dev.

For a server authenticator in Go:

- implement an `Authenticate` method, called for every incoming request, which checks the request's headers and returns a nil error if the request is valid, or an error explaining why not
- set up resources such as keys, clients or caches in `Start` and release them in `Shutdown`
- avoid slow or blocking work in `Authenticate`, because the pipeline cannot proceed until it finishes, and honour any deadline set on the context
- add metrics and traces so users can alert on rising errors

Client authenticators receive an object to inject auth data: the HTTP one provides an `http.RoundTripper`, the gRPC one can produce `credentials.PerRPCCredentials`.

Configuration then names it:

```yaml
extensions:
  myauth:
receivers:
  otlp:
    protocols:
      http:
        auth:
          authenticator: myauth
service:
  extensions: [myauth]
```

Points to follow:

- An authenticator is effective only when a consuming component references it; it must also be listed under `service::extensions`.
- Several instances need distinct names, such as `oidc/some-provider` and `oidc/another-provider`.
- A custom authenticator must be part of the same binary as the Collector: build a custom distribution with the OpenTelemetry Collector Builder, or publish a Go module for others to add to their distributions.

## Checked

Method: docs-checked 2026-11-09 against the Build an authenticator extension page (raw markdown, read in full). Dropped from the draft: the extension.NewFactory detail and the claim that Authenticate returns a context, neither stated on the page.
