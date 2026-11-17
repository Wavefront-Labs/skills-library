---
id: computing-software.software-engineering.uv.uv-auth-cli-http
name: uv-auth-cli-http
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-auth, credential-store, netrc, keyring, basic-auth, authentication, package-registry]
level: practitioner
status: docs-checked
description: "Store, show and remove registry credentials with uv auth, and know the precedence of URL, netrc, credentials store and keyring authentication."
sources: [https://docs.astral.sh/uv/concepts/authentication/cli/, https://docs.astral.sh/uv/concepts/authentication/http/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv auth commands and HTTP credential sources

Goal: give uv credentials for a private registry and understand where it looks for them.

## Method

Log in (prompts for credentials; uv does not validate them, so a wrong secret still succeeds):

```console
$ uv auth login example.com
$ echo 'my-password' | uv auth login example.com --password -
```

Options: `--username`, `--password`, or `--token` (for services using `__token__` or an arbitrary username). The docs recommend giving the secret on stdin with `-`; the same works for `--token`.

Show and remove:

```console
$ uv auth token example.com
$ uv auth token --username foo example.com
$ uv auth logout example.com
```

If a username was used to log in, pass it to `uv auth token`. Logout only removes local storage; the credentials are not invalidated on the server.

Stored credentials are used for packaging operations against that service. Only HTTPS Basic authentication is supported and they are not yet used for Git requests.

### Precedence of sources

1. Credentials in the URL, `https://<user>:<password>@<hostname>/...`
2. A netrc file: always enabled, path from the `NETRC` environment variable, else `~/.netrc`
3. The uv credentials store (plaintext `credentials.toml` in uv's state directory, for example `~/.local/share/uv/credentials/credentials.toml` on Unix; not meant to be hand-edited)
4. A keyring provider, off by default

Applies to hosts in `[index]`, `index-url`, `extra-index-url`, `find-links` and `package @ https://...`.

Keyring: only the `subprocess` provider (runs the `keyring` command). Enable with `--keyring-provider subprocess`, `UV_KEYRING_PROVIDER=subprocess`, or `tool.uv.keyring-provider = "subprocess"`.

Preview: `UV_PREVIEW_FEATURES=native-auth` switches to the OS-native encrypted store (Keychain, Windows Credential Manager, Secret Service on Linux); it only finds credentials uv itself added.

### Credential helper (experimental)

`uv auth helper` answers external tools using the Bazel credential helper protocol, JSON on stdin and stdout:

```console
$ echo '{"uri": "https://example.com/path"}' | uv --preview-features auth-helper auth helper --protocol=bazel get
```

With no match it returns `{ "headers": {} }`.

## Gotchas

- Credentials found are cached only for the one command, per scheme/host/port.
- `uv add` does not write index credentials into `pyproject.toml` or `uv.lock`, so later operations may fail on an authenticated index. Direct URLs (`package @ https://user:pass...`) are persisted.

## Verify

`uv auth token example.com` prints the stored credential for that URL.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/authentication/cli; concepts/authentication/http). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
