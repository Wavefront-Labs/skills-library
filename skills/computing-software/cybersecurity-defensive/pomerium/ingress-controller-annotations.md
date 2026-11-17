---
id: computing-software.cybersecurity-defensive.pomerium.ingress-controller-annotations
name: ingress-controller-annotations
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [ingress-controller, ingress-annotations, ingress-class, secure-upstream, kubernetes-ingress]
level: practitioner
status: docs-checked
description: "Protect Kubernetes services with the Pomerium Ingress Controller: ingress class, ingress.pomerium.io annotations, policy, upstream TLS and troubleshooting."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/deploy/k8s/ingress.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: Ingress resources are watched in all namespaces by default; only those with matching `spec.ingressClassName` (`pomerium`) are served; TLS is required. Default backend and resource backend are unsupported.

Annotations use `ingress.pomerium.io/<OPTION_NAME>` with string values (objects as JSON or multi-line YAML). Most standard route options work, including `policy` (PPL in YAML or JSON), `allow_any_authenticated_user`, `allow_websockets`, `pass_identity_headers`, `timeout`, `set_request_headers`.

Controller-specific: `secure_upstream` (HTTPS upstream), `h2c_upstream` (cannot combine with `secure_upstream`, `ssh_upstream`, `tcp_upstream`, `udp_upstream`), `kubernetes_service_account_token_secret`, `name`, `path_regex`, `service_proxy_upstream` (for meshes such as Istio), `ssh_upstream`, `tcp_upstream`, `udp_upstream`, `tls_client_secret`, `tls_custom_ca_secret`, `tls_downstream_client_ca_secret`, `identity_provider_secret`, and MCP options.

Secrets: must be in the Ingress namespace; the client secret is a TLS Secret; CA secrets need a `ca.crt` key. File paths are not supported. `set_*_headers_secret` keys must not overlap with the matching annotation.

Regex paths: `path_regex: "true"`, `pathType: ImplementationSpecific`, an RE2 path starting `^/` and ending `$`.

Certificates: from `spec.tls`, global `certificates`, or cert-manager (HTTP01 solver `ingress.class: pomerium`).

Troubleshoot: `kubectl describe` on the Ingress or `pomerium/global`; errors appear as `UpdateError` warnings in the events (the page's example is an invalid policy). Logs filter `"service":"authorize"`. The source mentions both `lb_policy` and `load_balancing_policy`; verify which your version accepts.

## Checked

2026-11-04. Confirmed against the Ingress Configuration page: requirements, annotation format, controller-specific annotations, secret rules, regex paths, certificates, troubleshooting. Reworded the UpdateError note to match the page example.

Method: documentation only; no commands were run.
