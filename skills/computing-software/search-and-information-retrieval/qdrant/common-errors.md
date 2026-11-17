---
id: computing-software.search-and-information-retrieval.qdrant.common-errors
name: common-errors
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [errors, troubleshooting, open-files, ulimit, common-errors]
level: intro
status: docs-checked
description: "Fix common Qdrant errors such as too many open files by raising the file descriptor limit."
sources:
  - "https://qdrant.tech/documentation/common-errors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The troubleshooting page covers these recurring problems.

Too many files open (OS error 24): each collection segment needs open files, so raise the limit before starting the server. With Docker set both limits at launch; otherwise change the limit for the current session.

```bash
docker run --ulimit nofile=10000:10000 qdrant/qdrant:latest
ulimit -n 10000
```

Insufficient storage (HTTP 507, gRPC `ResourceExhausted`, from v1.19.0): a resource quota is tripped and no replica accepts writes. Delete points or drop collections (point deletes stay allowed under a quota; deleting single vectors or payload keys is rejected), add capacity, or raise the limit with `PUT /quotas`. Writes resume only once usage falls below the release margin, 5 percentage points under the limit by default.

Unauthorized and forbidden: with API keys enabled, 401 means the key is missing or unrecognised (for example a mistyped key, or a Qdrant Cloud Management Key instead of a Database API key), and 403 means the key is known but not allowed. 403 causes include an expired or wrong-cluster granular key, a key not covering the collection, read-only access on a write, and missing manage or global access. A Cloud key created moments ago can return 403; wait a few seconds and retry.

Incompatible file system: storage must be POSIX-compatible. From v1.15.0 Qdrant checks at start and warns about unknown file systems or errors on ones like FUSE. An error means it is not safe to continue and data may be lost (vector data can reset to zeros after a restart). A common cause is a Windows folder bind-mounted into a Docker container under WSL; use a named Docker volume instead.

Can't open Collections meta Wal (code 11, WouldBlock): another instance is using the same storage files. In a distributed deployment each node needs its own storage directory, volume or mount.

Python gRPC client with `multiprocessing` failing with "Socket operation on non-socket": forked children share the parent's channel socket. Use the `forkserver` or `spawn` start method, switch to REST or the async client, or use built-in parallelism such as `upload_points`.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant troubleshooting page (landing_page repo, common-errors.md), read in full. Removed the unconfirmed systemd `LimitNOFILE` tip, the symptom list (slow filtered search, strict mode, port 6335, no volume) and the `log_level` advice.
