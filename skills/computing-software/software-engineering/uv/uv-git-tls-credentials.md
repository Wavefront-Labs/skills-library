---
id: computing-software.software-engineering.uv.uv-git-tls-credentials
name: uv-git-tls-credentials
category: computing-software
field: software-engineering
product: uv
tags: [uv, tls-certificates, native-tls, ssl-cert-file, git-credentials, ssh, hugging-face, mtls]
level: practitioner
status: docs-checked
description: "Authenticate uv to private Git repos over SSH or HTTP, configure system or custom CA certificates, and use Hugging Face token support."
sources: [https://docs.astral.sh/uv/concepts/authentication/git/, https://docs.astral.sh/uv/concepts/authentication/certificates/, https://docs.astral.sh/uv/concepts/authentication/third-party/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv Git credentials, TLS certificates and third-party auth

Goal: install from private Git repos and work behind corporate TLS.

## Method

### Git over SSH or HTTP

SSH needs the username `git`:

- `git+ssh://git@github.com/astral-sh/uv`

HTTP Basic with a password or token:

- `git+https://<user>:<token>@<hostname>/...`
- `git+https://<token>@<hostname>/...`
- `git+https://<user>@<hostname>/...`

For a GitHub personal access token the username is arbitrary. With no credentials in the URL, uv queries the Git credential helper. With GitHub, `gh auth login` sets one up; after `gh auth login --with-token` also run `gh auth setup-git`.

`uv add` does not persist Git credentials to `pyproject.toml` or `uv.lock`. `--raw` forces it, but a credential helper is strongly recommended.

### TLS

uv uses rustls with aws-lc-rs and, by default, bundled Mozilla root certificates. To use the OS store (for example a corporate proxy root), use any of:

- `--system-certs`
- `UV_SYSTEM_CERTS=true`
- `system-certs = true` in `uv.toml`

Custom CAs: set `SSL_CERT_FILE` to a PEM bundle or `SSL_CERT_DIR` to directories of PEM files (separator `:` on Unix, `;` on Windows). When non-empty these override the default certificate source entirely; a missing or empty target means no default certificates are trusted. DER files are not supported and unparseable files are ignored. For one `uv pip` call use `--cert /path/to/certs.pem`.

mTLS: `SSL_CLIENT_CERT` points to a PEM file holding the certificate followed by the private key.

Trust a specific host without verification (HTTPS only, hostname or host:port):

```toml
[tool.uv]
allow-insecure-host = ["example.com"]
```

### Third-party

Dedicated guides cover Azure Artifacts, Google Artifact Registry, AWS CodeArtifact and JFrog Artifactory. For Hugging Face, uv forwards `HF_TOKEN` to `huggingface.co`:

```console
$ HF_TOKEN=hf_... uv run https://huggingface.co/datasets/<user>/<name>/resolve/<branch>/main.py
```

Disable with `UV_NO_HF_TOKEN=1`.

## Gotchas

Use `allow-insecure-host` only in trusted environments.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/authentication/git; concepts/authentication/certificates; concepts/authentication/third-party). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
