---
id: computing-software.software-engineering.uv.uv-private-registry-integrations
name: uv-private-registry-integrations
category: computing-software
field: software-engineering
product: uv
tags: [uv, azure-artifacts, artifactory, codeartifact, google-artifact-registry, private-index, keyring, uv-publish]
level: practitioner
status: docs-checked
description: "Set up uv indexes, usernames, tokens and keyring plugins for Azure Artifacts, Google Artifact Registry, AWS CodeArtifact and JFrog Artifactory, plus publishing."
sources: [https://docs.astral.sh/uv/guides/integration/azure/, https://docs.astral.sh/uv/guides/integration/google/, https://docs.astral.sh/uv/guides/integration/aws/, https://docs.astral.sh/uv/guides/integration/jfrog/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv with private registries

Goal: install from and publish to a private index. All four use a named index in `pyproject.toml`:

```toml
[[tool.uv.index]]
name = "private-registry"
url = "<registry simple URL>"
publish-url = "<registry upload URL>"
```

## Method

Credentials come from `UV_INDEX_<NAME>_USERNAME` and `UV_INDEX_<NAME>_PASSWORD`, where the name is the index name uppercased (`private-registry` becomes `PRIVATE_REGISTRY`). Index URLs:

| Registry | url | Username |
|---|---|---|
| Azure Artifacts | `https://pkgs.dev.azure.com/<ORGANIZATION>/<PROJECT>/_packaging/<FEED>/pypi/simple/` | any string (PAT as password); `VssSessionToken` for keyring |
| Google Artifact Registry | `https://<REGION>-python.pkg.dev/<PROJECT>/<REPOSITORY>/simple/` | `oauth2accesstoken` |
| AWS CodeArtifact | `https://<DOMAIN>-<ACCOUNT_ID>.d.codeartifact.<REGION>.amazonaws.com/pypi/<REPOSITORY>/simple/` | `aws` |
| JFrog Artifactory | `https://<organization>.jfrog.io/artifactory/api/pypi/<repository>/simple` | your username, or empty string with a JWT as password |

Tokens: Google `gcloud auth application-default print-access-token`; AWS `aws codeartifact get-authorization-token --domain <DOMAIN> --domain-owner <ACCOUNT_ID> --query authorizationToken --output text` (may need `--region`).

### Keyring alternative (Azure, Google, AWS)

uv supports only keyring subprocess mode: the `keyring` executable must be on PATH and the URL username must be the value above. Install the plugin from public PyPI (not the private index):

```bash
uv tool install keyring --with artifacts-keyring          # Azure
uv tool install keyring --with keyrings.google-artifactregistry-auth
uv tool install keyring --with keyrings.codeartifact
export UV_KEYRING_PROVIDER=subprocess
export UV_INDEX_PRIVATE_REGISTRY_USERNAME=<username above>
```

`tool.uv.keyring-provider` can enable it in config, and the username can sit in the index URL.

### Publishing

Set `publish-url`: Azure `.../pypi/upload/`, Google `https://<REGION>-python.pkg.dev/<PROJECT>/<REPOSITORY>/`, CodeArtifact `.../pypi/<REPOSITORY>/`, JFrog `.../api/pypi/<repository>`. Credentials via `UV_PUBLISH_USERNAME` and `UV_PUBLISH_PASSWORD` (not index-named), then:

```console
$ uv publish --index private-registry
```

Setting only `UV_PUBLISH_URL` also works but is less preferable: uv cannot check whether the package is already published.

## Gotchas

- JFrog: `--token` or `UV_PUBLISH_TOKEN` gives 401 Unauthorized because uv sends `__token__` as the username and JFrog requires an empty one. Use `uv publish --index <index_name> -u "" -p "$JFROG_TOKEN"`.
- Wrong Google or AWS username makes authentication fail.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/azure; guides/integration/google; guides/integration/aws; guides/integration/jfrog). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
