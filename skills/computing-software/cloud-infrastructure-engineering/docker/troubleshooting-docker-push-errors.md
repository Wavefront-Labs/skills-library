---
id: computing-software.cloud-infrastructure-engineering.docker.troubleshooting-docker-push-errors
name: troubleshooting-docker-push-errors
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, push, push-errors, denied-requested-access, registry, docker-login, blob-upload]
level: practitioner
status: docs-checked
description: "Diagnose docker push failures: denied/requested access, unauthorized, blob unknown, manifest invalid, 413 entity too large, retrying uploads and x509 errors, with fixes."
sources: ["https://docs.docker.com/reference/cli/docker/image/push/", "https://github.com/opencontainers/distribution-spec/blob/main/spec.md#error-codes", "https://docs.docker.com/engine/security/certificates/", "https://docs.docker.com/reference/cli/dockerd/", "https://docs.docker.com/reference/cli/docker/login/", "https://docs.docker.com/build/buildkit/configure/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting docker push errors

| Error | Usual cause | Fix |
|---|---|---|
| `denied: requested access to the resource is denied` (distribution-spec code `DENIED`) | Repo path not yours (missing registry host or namespace), not logged in, or credentials lack push permission | Tag with full `host/namespace/repo`; `docker login host`; check the token's permissions at the registry |
| `unauthorized: authentication required` (`UNAUTHORIZED`) | Expired credentials, credential helper returning nothing | `docker logout host && docker login host`; check `credsStore` / `credHelpers` in `config.json` |
| `name unknown: repository name not known to registry` (`NAME_UNKNOWN`) | Some registries need the repository created first | Create the repository or project in the registry |
| `blob unknown` (`BLOB_UNKNOWN`) / `manifest blob unknown` (`MANIFEST_BLOB_UNKNOWN`) | A layer the registry expected is missing | Re-push; check registry storage and garbage collection |
| `manifest invalid` (`MANIFEST_INVALID`) | Registry rejects the manifest, for example attestation or index media types | Try `docker buildx build --provenance=false`; upgrade the registry |
| `413 Request Entity Too Large` | Body-size limit in a proxy in front of the registry | Raise the proxy or ingress body limit |
| `Retrying in N seconds` loops | Proxy timeouts or an unstable link | Raise proxy timeouts; lower `max-concurrent-uploads` (daemon default 5) |
| `x509: certificate signed by unknown authority` | Private CA not trusted by the daemon | Put the CA at `/etc/docker/certs.d/<host:port>/ca.crt` (see the Engine certificates page for rootless, Windows and Desktop locations) |
| `server gave HTTP response to HTTPS client` | Plain HTTP registry | Use TLS, or add to `insecure-registries` (lab only) |
| `toomanyrequests` (`TOOMANYREQUESTS`) | Registry rate limit | Authenticate, back off, use a mirror |
| `invalid reference format` | Uppercase or invalid characters in the name | Sanitise names |

## Debug steps
```bash
docker push reg.example.com/team/app:1.2
# credentials live in $HOME/.docker/config.json (auths, credsStore, credHelpers)
```
For buildx pushes (`--push`), credentials come from the same config file but the push is
done by BuildKit: with a `docker-container` builder, CA trust must be configured in
`buildkitd.toml` (`[registry."reg.example.com"] ca=[...]`), not `/etc/docker/certs.d`.

## Daemon tuning for flaky links
```json
{ "max-concurrent-uploads": 2 }
```
`max-concurrent-uploads` is the documented per-push limit (default 5).

## Checked
Date: 2026-10-26. Documentation: opencontainers/distribution-spec (error codes table), docker/docs main (last commit 2026-10-23) dockerd reference, Engine certificates page, `docker login` reference, BuildKit configuration page. Confirmed: error code names and messages, `max-concurrent-uploads` default 5, `insecure-registries`, certs.d locations, `credsStore`/`credHelpers` in config.json, `--provenance` flag, buildkitd.toml `[registry."host"] ca=[...]`. Removed as unconfirmed: `max-upload-attempts` (not in the dockerd reference), `oci-mediatypes=false` advice, ECR and GitHub token scope names, nginx directive, jq/curl/journalctl debugging lines, the sudo and Desktop keychain gotchas, the MTU and `tag invalid` rows.
Method: documentation only; no commands were run.
