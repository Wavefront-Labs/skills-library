---
id: computing-software.devops-ci-cd.gitlab-ci.troubleshooting-agentk-and-kas
name: troubleshooting-agentk-and-kas
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, kas-troubleshooting, agentk-logs, gitlab-agent, agentk]
level: advanced
status: docs-checked
description: "Troubleshoot the GitLab agent for Kubernetes: agentk logs, KAS address and trailing slash, scheme mismatch, custom CA, version mismatch and dashboard Unauthorized errors."
sources: ["https://docs.gitlab.com/user/clusters/agent/troubleshooting/", "https://docs.gitlab.com/administration/clusters/kas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting agentk and KAS connectivity

## First look
```bash
kubectl logs -f -l=app.kubernetes.io/name=gitlab-agent -n gitlab-agent
```
Administrators can also read the KAS (agent server) logs on the GitLab side.

## Common errors
| Log line | Cause | Fix |
|---|---|---|
| `failed to WebSocket dial ... no such host` | `kas-address` wrong or unreachable | correct the KAS address; on GitLab.com KAS is `wss://kas.gitlab.com` (also `grpcs://kas.gitlab.com`) |
| `expected handshake response status code 101 but got 301` | `ws`/`wss` address lacks a trailing slash | end it with a slash, e.g. `wss://gitlab.example.com:443/-/kubernetes-agent/` |
| `malformed HTTP response` on handshake | agent set to `wss` but the server is not serving `wss` | use the same scheme on both sides |
| `Decompressor is not installed for grpc-encoding "gzip"` | agentk is newer than KAS | run the same version of agentk and KAS |
| `x509: certificate signed by unknown authority` | internal CA unknown to the agent | Helm `--set-file config.kasCaCert=my-custom-ca.pem` (PEM or DER) |
| same x509 error in the KAS log | KAS does not trust the GitLab certificate | install the CA in `/etc/gitlab/trusted-certs` (or set `gitlab_kas['env']` `SSL_CERT_DIR`), then `gitlab-ctl reconfigure` and `gitlab-ctl restart gitlab-kas` |
| `Failed to register agent pod. Please make sure the agent version matches the server version.` | version skew | match the agent version to the GitLab version; check `gitlab-ctl status gitlab-kas` and its logs |
| `GitLab Agent Server: Unauthorized` on the dashboard | missing or wrong `user_access` in the agent config; duplicate `_gitlab_kas` cookies; GitLab and KAS on different sites (unsupported) | fix `user_access`, clear the duplicate cookie |

Self-managed default KAS address changed to `grpcs://gitlab.example.com` in GitLab 19.5 (earlier
versions used `ws(s)://.../-/kubernetes-agent/`); check the KAS admin page for your version.

## Version mismatch warning
"Agent version mismatch" on the Kubernetes clusters page can be a stale cached agent version in KAS, which
periodically deletes outdated versions: wait at least 20 minutes, then update the agent if it persists.

## Verify
- [ ] The agent pod log shows no dial, handshake or certificate errors.

## Checked

2026-10-31. Confirmed against the GitLab agent for Kubernetes troubleshooting page (log command, WebSocket dial and 301 trailing-slash errors, scheme mismatch, grpc Decompressor error, kasCaCert Helm flag and PEM or DER format, KAS trusted-certs directory and SSL_CERT_DIR, register-agent-pod error, dashboard Unauthorized causes, 20 minute version-mismatch wait) and the KAS administration page (kas.gitlab.com wss and grpcs addresses, gitlab_kas settings, 19.5 default address change).
Removed: the 401 token row, the load balancer idle-timeout row, the CI access and RBAC rows, the debug-logging settings, the UI connection-status labels and the kubecontext verify step, none of which appear in the fetched pages.

Method: documentation only; no commands were run.
