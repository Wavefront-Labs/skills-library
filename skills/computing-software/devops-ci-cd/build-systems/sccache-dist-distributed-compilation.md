---
id: computing-software.devops-ci-cd.build-systems.sccache-dist-distributed-compilation
name: sccache-dist-distributed-compilation
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, sccache-dist, sccache, distributed-compilation, icecream, distcc, rust-builds]
level: practitioner
status: docs-checked
description: "Distribute C, C++ and Rust compilation with sccache-dist: scheduler and build servers, toolchain packaging, auth, client config, and when distcc or icecream fit better."
sources: ["https://github.com/mozilla/sccache/blob/main/docs/Distributed.md", "https://github.com/mozilla/sccache/blob/main/docs/DistributedQuickstart.md", "https://github.com/mozilla/sccache/blob/main/docs/Configuration.md", "https://github.com/mozilla/sccache/blob/main/docs/Rust.md", "https://github.com/icecc/icecream"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sccache-dist distributed compilation

sccache caches compiler outputs locally or in cloud storage; **sccache-dist** additionally ships cache misses to a pool of build servers, using icecream-style automatic packaging of the local toolchain. It supports the compilers sccache supports, including Rust.

## Components
- **Scheduler** (`sccache-dist scheduler`): assigns jobs; one per cluster.
- **Build servers** (`sccache-dist server`): Linux machines that run jobs in a sandbox (bubblewrap with the `overlay` builder, or the `docker` builder); they must run as root because of bubblewrap.
- **Clients**: normal `sccache` with a `[dist]` config. Linux clients package their compiler automatically; Windows and macOS clients must specify a toolchain for cross-compilation ahead of time.

## Scheduler and server config
```toml
# scheduler.conf
public_addr = "0.0.0.0:10600"
[client_auth]
type = "token"
token = "<client token>"
[server_auth]
type = "jwt_hs256"
secret_key = "<generated with: sccache-dist auth generate-jwt-hs256-key>"
```
```toml
# server.conf
cache_dir = "/var/cache/sccache-dist"
public_addr = "10.0.0.21:10501"
scheduler_url = "https://sccache-sched.example.com"
[builder]
type = "overlay"                       # or "docker"
build_dir = "/var/lib/sccache-dist/build"
bwrap_path = "/usr/bin/bwrap"          # bubblewrap 0.3.0 or newer
[scheduler_auth]
type = "jwt_token"
token = "<from: sccache-dist auth generate-jwt-hs256-server-token --server 10.0.0.21:10501 ...>"
```
Isolate build servers on a build network; the documentation discusses trust between scheduler, servers and clients (tokens, JWT) and shows an HTTPS `scheduler_url`.

## Client config
```toml
# ~/.config/sccache/config   (Linux; override with SCCACHE_CONF)
[dist]
scheduler_url = "https://sccache-sched.example.com"
toolchains = []
toolchain_cache_size = 5368709120
[dist.auth]
type = "token"
token = "<client token>"
```
```bash
export RUSTC_WRAPPER=sccache            # Rust
cmake -DCMAKE_C_COMPILER_LAUNCHER=sccache -DCMAKE_CXX_COMPILER_LAUNCHER=sccache ...
sccache --dist-status                    # JSON: scheduler address, number of servers and CPUs, jobs in progress
sccache --show-stats                     # cache hits and misses
```
The client packages its compiler toolchain and uploads it to servers, which cache it under `cache_dir`. After changing the configuration, run `sccache --stop-server` and `sccache --start-server`.

## Caveats
- sccache cannot cache steps that invoke the system linker (for Rust: `bin`, `dylib`, `cdylib`, `proc-macro` crates), and Rust incremental compilation must be disabled (`CARGO_INCREMENTAL=0`).
- High-latency links can make distribution slower than compiling locally; measure.

## Alternatives
- **icecream (icecc)**: the project sccache's distributed mode is modelled on, lacking authentication and sandboxing features that sccache-dist adds.
- Remote execution (Bazel/Buck2 with a remote execution service): hermetic, cache plus execution, larger setup.

## Verify
- [ ] `sccache --dist-status` lists servers.
- [ ] A clean build is measurably faster than with local-only sccache.

## Checked
Date: 2026-10-25. Documentation: mozilla/sccache `README.md`, `docs/Distributed.md`, `docs/DistributedQuickstart.md`, `docs/Configuration.md`, `docs/Rust.md` (default branch).
Confirmed: scheduler, server and client roles; scheduler, server and client config keys and values (`public_addr`, `client_auth`, `server_auth` `jwt_hs256`, `cache_dir`, `scheduler_url`, `[builder]` `overlay`/`docker`, `bwrap_path`, `scheduler_auth`, `[dist]`, `toolchains`, `toolchain_cache_size`, `[dist.auth]`); `generate-jwt-hs256-key` and `generate-jwt-hs256-server-token --server`; servers must run as root; Windows/macOS clients need predeclared cross-compilation toolchains; client config path and `SCCACHE_CONF`; `--dist-status` output; restart after config change; Rust incremental and linker limitations; icecream-style description.
Removed: "sandboxed with bubblewrap or Docker" for all server modes beyond the documented builders, `[[dist.toolchains]]`/`path_override`/`no_dist` details, "Successful distributed compiles" stat wording, distcc and "icecream has no Rust" alternatives, "TLS in front of scheduler" as a requirement, and the claim that preprocessing and linking always run locally.
Method: documentation only; no commands were run.
