---
id: computing-software.devops-ci-cd.build-systems.bazel-remote-cache-backends
name: bazel-remote-cache-backends
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [bazel, build-systems, remote-cache, bazel-remote-cache, bazel-remote, buildbarn, buildbuddy, engflow, nativelink, remote-execution, remote-apis, grpc-cache, gcs-cache, cache-hit-rate, remote-upload-local-results]
level: advanced
status: docs-checked
description: "Set up a Bazel remote cache: bazel-remote, Buildbarn, BuildBuddy and other REAPI backends, read-only for laptops vs write for CI, auth, and diagnosing poor hit rates."
sources: ["https://bazel.build/remote/caching", "https://bazel.build/remote/cache-remote", "https://bazel.build/community/remote-execution-services", "https://github.com/buchgr/bazel-remote", "https://github.com/buildbarn/bb-deployments"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel remote cache backends

The remote cache stores the **action cache** (action digest -> result) and the **CAS**
(content-addressed blobs). Bazel talks to it over HTTP/1.1 (`http`, `https`) or gRPC (`grpc`, `grpcs`) via `--remote_cache`.

## Backends
| Backend | Notes |
|---|---|
| **bazel-remote** | open source (not supported by the Bazel project); disk cache with LRU eviction and optional S3, GCS and (experimental) Azure blob proxy backends; HTTP and gRPC |
| **Buildbarn** | open-source remote cache and execution server (bb-storage, scheduler, workers); example deployments in the bb-deployments repository |
| BuildBuddy, EngFlow, NativeLink, Aspect Build | listed on Bazel's Remote Execution Services page (remote execution and/or caching) |
| Google Cloud Storage | HTTP API compatible with the protocol: `--remote_cache=https://storage.googleapis.com/<bucket>` with a service-account key (`--google_credentials`) |

bazel-remote quick start (default ports: HTTP 8080, gRPC 9092):
```bash
docker run -d -p 9092:9092 -p 8080:8080 -v /data/bazel-remote:/data \
  buchgr/bazel-remote-cache --max_size=500        # GiB; --max_size is required
```

## Client config
```
# .bazelrc
build:remote-cache --remote_cache=grpcs://cache.example.com:443
build:remote-cache --remote_header=x-api-key=...        # or --google_credentials / mTLS (--tls_client_certificate, --tls_client_key)
build:remote-cache --remote_timeout=60                  # seconds; this is the default
build:remote-cache --remote_download_minimal            # don't download intermediate outputs
build:remote-cache --remote_cache_compression           # older name: --experimental_remote_cache_compression

# laptops read, only CI writes (prevents poisoning by unhermetic local envs)
build:remote-cache --noremote_upload_local_results
build:ci --remote_upload_local_results
```
Run CI with `--config=remote-cache --config=ci`. Keep secrets out of `.bazelrc` in git:
put the header in `~/.bazelrc` or a CI-provided `--bazelrc` file. To exclude a target from the remote cache, tag it `no-remote-cache`.

## Why hit rates are low
- Action keys include the command line, environment and input digests. Different absolute paths, `PATH`, compilers or OS versions between machines give different keys. Bazel's documentation notes that only variables passed with `--action_env` enter the action definition; `--incompatible_strict_action_env` (default true) gives a static `PATH`.
- Stamped targets (`--stamp`) change with the stamping info: stamp only release builds.
- Compare two builds' execution logs (`--execution_log_compact_file`) to find which input differs.
- Build Event Service results (`--bes_backend`, `--bes_results_url`) are available from BES servers such as BuildBuddy for per-invocation analysis.

## Operations
- Size the cache for the working set of CI outputs; LRU eviction is fine (it is a cache, not storage).
- Never let untrusted PR builds write to the cache shared with release builds: poisoned outputs would be reused. Use separate instances or `--noremote_upload_local_results` for forks.
- Watch hit rate (the build summary reports `remote cache hit` counts) and latency; `--remote_local_fallback` lets the build fall back to local execution if the remote is unavailable.

## Verify
`bazel clean && bazel build //... --config=remote-cache` on a second machine reports a high `remote cache hit` count and finishes much faster than the cold build.

## Checked
Date: 2026-10-25. Documentation: Bazel `docs/remote/caching.mdx`, `docs/community/remote-execution-services.mdx`, option definitions (`RemoteOptions.java`, `AuthAndTLSOptions.java`, `BuildEventServiceOptions.java`) in bazelbuild/bazel; buchgr/bazel-remote README.
Confirmed: supported protocols; bazel-remote description, ports, required `--max_size` in GiB, S3/GCS/Azure proxies, image name; GCS URL form; flags `--remote_cache`, `--remote_header`, `--remote_timeout`, `--remote_download_minimal`, `--remote_cache_compression` (renamed from `--experimental_remote_cache_compression`), `--remote_upload_local_results`, `--remote_local_fallback`, `--google_credentials`, `--tls_client_certificate`, `--tls_client_key`, `--bes_backend`, `--bes_results_url`; `no-remote-cache` tag; `--action_env` and strict action env; vendor names on the Remote Execution Services page.
Removed: "sharded, mirrored storage" and Kubernetes claims for Buildbarn, "no gRPC batching / no CAS presence checks" for plain HTTP, "per-action cache miss reasons" for BuildBuddy, the 60-second timeout as a tuning claim (kept only as the default), and the "1-2 weeks of outputs" sizing rule.
Method: documentation only; no commands were run.
