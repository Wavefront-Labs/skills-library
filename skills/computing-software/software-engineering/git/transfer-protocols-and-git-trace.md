---
id: computing-software.software-engineering.git.transfer-protocols-and-git-trace
name: transfer-protocols-and-git-trace
category: computing-software
field: software-engineering
product: git
tags: [git, git-trace, git-protocol-v2, smart-http, git-curl-verbose, clone-debugging, git-internals]
level: advanced
status: docs-checked
description: "Debug slow or failing clone/fetch/push: smart HTTP vs SSH, protocol v2, GIT_TRACE/GIT_TRACE_PACKET/GIT_CURL_VERBOSE, proxies, TLS and RPC failures."
sources:
  - https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols
  - https://git-scm.com/docs/gitprotocol-v2
  - https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables
  - https://git-scm.com/docs/git
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/docs/git-clone
  - https://git-scm.com/docs/git-fetch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transfer protocols and GIT_TRACE

**Goal:** see what Git says on the wire when clone/fetch/push hang or fail, and fix
the usual network causes.

## Protocols
| URL | Transport | Notes |
|---|---|---|
| `https://host/org/repo.git` | smart HTTP | auth via credential helper; proxies and TLS inspection apply |
| `git@host:org/repo.git` / `ssh://` | SSH | key auth; port 22 often blocked on corporate networks |
| `git://` | git daemon | does no authentication; the manual says to use it with caution on unsecured networks |
| `file://` / path | local | a plain local path clones by copying (hardlinking) object files; a `file://` URL uses the normal Git transport instead |

Protocol v2 (default since Git 2.26) lets the client ask only for refs it needs
(`ls-refs` with prefixes) instead of the server advertising every ref - big win on repos
with many refs. Force or check: `git -c protocol.version=2 ls-remote origin`.

## Trace variables
```bash
GIT_TRACE=1 git fetch                 # commands, aliases, child processes
GIT_TRACE_PACKET=1 git ls-remote origin 2>&1 | head -50    # pkt-line conversation
GIT_TRACE_CURL=1 GIT_TRACE_CURL_NO_DATA=1 git fetch        # curl trace without the data payload
GIT_TRACE_PERFORMANCE=1 git status    # timing per phase
GIT_SSH_COMMAND="ssh -vvv" git fetch  # SSH negotiation
GIT_TRACE2_PERF=<absolute-path> git fetch   # structured timing (trace2)
```
By default tracing redacts cookie values and the `Authorization:` / `Proxy-Authorization:` headers and packfile URIs; `GIT_TRACE_REDACT=false` turns that off, so leave it on when sharing traces.

## Classic failures
- **"RPC failed" or disconnects on big pushes over HTTP**: suspect a proxy or server limit
  and capture a curl trace. Raising `http.postBuffer` (default 1 MiB) is only effective for
  disabling chunked transfer encoding, which matters only for servers or proxies that do
  not support HTTP/1.1 chunking; the manual says it is not in general a solution and
  increases memory use. Pushing over SSH avoids the HTTP path.
  Per the manual, a proxy must be completely transparent (no modifying or buffering of
  requests or responses) or Git can break.
- **TLS certificate errors** (for example behind corporate TLS inspection): point Git at the
  corporate CA bundle with `http.sslCAInfo` (`http.sslBackend` selects the TLS backend),
  and avoid disabling `http.sslVerify` globally.
- **Proxy**: `git config --global http.proxy <[protocol://][user[:password]@]proxyhost[:port]>`;
  `remote.<name>.proxy` overrides it per remote (see git-config).
- **SSH works, HTTPS asks for password repeatedly**: credential helper missing or token
  lacks scope (see credential helpers skill).

## Speeding up big transfers
`git clone --filter=blob:none` (partial clone), `--depth=1`, `--single-branch` and
`fetch.parallel` (maximum parallel fetch operations: submodules, or remotes with `--multiple`; default 1).

## Verify
- [ ] `GIT_TRACE_PACKET=1 git ls-remote` shows `version 2` in the first packets.
- [ ] The failure reproduces with traces captured before changing any setting.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22) and the Git 2.26 release notes. Confirmed: `protocol.version` defaults to 2 (config/protocol) and `ls-refs` exists in gitprotocol-v2; `GIT_TRACE`, `GIT_TRACE_PACKET`, `GIT_TRACE_CURL`, `GIT_TRACE_CURL_NO_DATA`, `GIT_TRACE_PERFORMANCE`, `GIT_SSH_COMMAND`, `GIT_TRACE2_PERF`, `GIT_TRACE_REDACT` behaviour (git); `git://` does no authentication (urls); local-path clone versus URL clone behaviour (git-clone); `http.postBuffer` semantics and default, `http.sslCAInfo`, `http.sslBackend`, `http.sslVerify`, `http.proxy` and `remote.<name>.proxy`; `fetch.parallel`. Corrected: `GIT_CURL_VERBOSE` is not documented in the Git manual, so the curl trace variable is now `GIT_TRACE_CURL`. Removed as unconfirmed: exact curl and RPC error strings, the push-in-chunks workaround, the per-host empty-proxy bypass, the CPU-bound remark about resolving deltas and the bitmap and commit-graph remark.

Method: documentation only; no commands were run.
