---
id: computing-software.cybersecurity-defensive.application-security.environment-secrets
name: environment-secrets
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [environment-secrets, environment-variables, twelve-factor, secrets-management, secret-leakage]
level: practitioner
status: docs-checked
description: "Use environment variables for app secrets safely: why they are a weak store, preferring mounted files or a secrets manager, and Kubernetes Secret handling."
sources: ["https://12factor.net/config", "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html", "https://kubernetes.io/docs/concepts/configuration/secret/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variable secrets

## Why people use them
The Twelve-Factor App stores config, including credentials to external services, in environment variables: they are
easy to change between deploys, are unlikely to be checked into the repo by accident, and are a language- and
OS-agnostic standard. Its litmus test: the codebase could be open-sourced at any moment without exposing
credentials.

## Why they are a weak secret store
The OWASP Secrets Management Cheat Sheet says environment variables are generally accessible to all processes and
may be included in logs or system dumps, so they are not recommended unless the other methods are not possible.
Never hardcode secrets with Docker `ENV` or `ARG`: they leak with the container definition.

## Safer patterns (container context, per the cheat sheet)
1. **Fetch from a secrets manager at runtime** (for example through a sidecar), which avoids exposing the secret in
   the file system or the container's environment variables. Short-lived sidecar containers can fetch secrets and
   store them on a shared volume (Vault Agent Sidecar Injector, Conjur Secrets Provider are examples).
2. **Mounted volumes (files)**: the orchestrator mounts the secret file when required; never build it into the
   image, as that leaks the secret with the container definition.
3. **Environment variables**: only when the others are not possible, and let the orchestrator inject the real value
   rather than hardcoding it.

Only expose secrets through the channel between the container and its deployment object (such as the Pod); never
through mechanisms shared among deployments (a shared volume).

## Kubernetes Secrets
- Secrets are by default stored unencrypted in etcd, and anyone with API access or etcd access can read them: enable
  encryption at rest and configure RBAC. The cheat sheet adds that the orchestrator's storage backend must be
  encrypted and its keys well managed.
- A Secret can be mounted as a volume or exposed as environment variables (`env[].valueFrom.secretKeyRef`); mounted
  Secret data is updated eventually when the Secret changes.
- Base64 in a Secret only obscures values; it is not encryption.

## Verify
No literal secret values in manifests, Dockerfiles or image layers; access to the secret store is monitored, with
alerts when a secret is read from an unexpected IP or user agent (cheat sheet section on event monitoring).

## Checked
Method: docs-checked 2026-11-09 against 12factor.net/config, the OWASP Secrets Management Cheat Sheet (containers
and orchestrators section read in full; other sections searched) and the Kubernetes Secrets concept page (security
notes, volume and `secretKeyRef` sections). Removed unconfirmed claims: `/proc/<pid>/environ` and `ps` leakage,
docker inspect, Sentry and framework debug-page specifics, `.env` and `.gitignore` practices, `/run/secrets` and the
CSI driver, and the `unset` and subprocess-environment hardening steps.
