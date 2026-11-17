---
id: computing-software.devops-ci-cd.bazel.bazel-remote-cache-setup
name: bazel-remote-cache-setup
category: computing-software
field: devops-ci-cd
product: bazel
tags: [remote-cache, remote-cache-flag, bazel-remote, http-caching-protocol, upload-local-results, no-remote-cache]
level: practitioner
status: docs-checked
description: "Point Bazel at an HTTP or gRPC remote cache, make CI the only writer, exclude targets, and know the /ac and /cas paths."
sources: ["https://bazel.build/remote/caching"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel remote cache setup

A remote cache lets a team and CI share action outputs. It stores two things: the action cache (action hash to result metadata) and a content-addressable store (CAS) of output files. Stdout and stderr of every action are stored too, so Bazel console output is not a reliable hit-rate signal.

Backends: any HTTP/1.1 server that supports PUT and GET (nginx with WebDAV, Apache httpd, S3), bazel-remote (open source, REST and gRPC, disk storage with garbage collection; not supported by the Bazel project), or Google Cloud Storage. Over HTTP, metadata lives under `/ac/<sha256>` and files under `/cas/<sha256>`.

```
# .bazelrc
build --remote_cache=https://cache.example.com:8080/cache
# only read from the remote cache:
build --remote_upload_local_results=false
```

Supported schemes: http, https, grpc, grpcs. Basic auth can be embedded as `https://user:pass@host:port/path`; it is plaintext, so only ever use it over HTTPS. Unix sockets: `--remote_proxy=unix:/path/to/socket` (not on Windows).

Opt a target out with `tags = ["no-remote-cache"]`. Deleting content is done in the server (whole cache or old entries); you cannot tell which blobs belong to which build. Wipe after cache poisoning.

Few hits across machines? Check for environment variables leaking into actions (only `--action_env` vars should count; an old `/etc/bazel.bazelrc` from the Debian/Ubuntu package whitelisted `$PATH`), and remember Bazel does not track tools outside the workspace such as `/usr/bin` compilers.

## Checked

2026-11-04. Read against the Bazel docs page(s): Remote Caching (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the claim that CI keeps write access and the closing Verify line.
Method: documentation only; no commands were run.
