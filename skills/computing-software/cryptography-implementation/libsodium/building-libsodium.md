---
id: computing-software.cryptography-implementation.libsodium.building-libsodium
name: building-libsodium
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium-build, libsodium, build, cross-compilation, minisign, wasm]
level: practitioner
status: gated
description: "Build libsodium from source: verifying release signatures, minimal builds, static linking, cross-compiling for mobile and WASM, and running the test suite."
sources: ["https://doc.libsodium.org/installation", "https://github.com/jedisct1/libsodium/releases", "https://jedisct1.github.io/minisign/", "https://download.libsodium.org/libsodium/releases/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Building libsodium

## Verify then build
```sh
curl -LO https://download.libsodium.org/libsodium/releases/libsodium-1.0.20-stable.tar.gz
curl -LO https://download.libsodium.org/libsodium/releases/libsodium-1.0.20-stable.tar.gz.minisig
minisign -VP RWQf6LRCGA9i53mlYecO4IzT51TGPpvWucNSCh1CBM0QTaLn73Y7GFO3 -m libsodium-1.0.20-stable.tar.gz
tar xzf libsodium-1.0.20-stable.tar.gz && cd libsodium-stable
./configure --prefix=/usr/local && make -j && make check && sudo make install
```
The public key and the `minisign -VP <key> -m <file>` form match the installation page (checked 2026-10-19); re-check it there rather than trusting a copy. The `-stable` tarball and its `.minisig` for 1.0.20 exist on download.libsodium.org (HTTP 200) and unpack to `libsodium-stable/`; 1.0.21 files are listed too and the changelog goes up to 1.0.22, so check the releases directory for the current version and adjust the file names. Not run on the review host (no C compiler, no minisign): `./configure && make && make check && make install` (gated: unconfirmed, source is paywalled or blocked) and the signature check (gated: unconfirmed, source is paywalled or blocked).
`-stable` tarballs include post-release fixes; versioned tarballs are fixed snapshots.

## Options
- `--enable-minimal` (not documented on the installation page; `./configure --help` says "Only compile the minimum set of functions required for the high-level API"): per `src/libsodium/Makefile.am` it leaves out the ed25519 core and ristretto255 functions, scrypt, the XChaCha20 box (`crypto_box_curve25519xchacha20poly1305_*`), `crypto_secretbox_xchacha20poly1305`, `crypto_stream_xchacha20`, the salsa20/12 and salsa20/8 streams and SipHash-x. Smaller binary.
- `--disable-shared` for static linking (`./configure --help` lists `--enable-shared` and `--enable-static`); `--enable-pic` is the PIC switch listed by 1.0.20-stable's `./configure --help`.
- Zig build (`zig build -Doptimize=ReleaseFast`) supports easy cross-compilation for many targets.
- Scripts in `dist-build/`: the installation page lists `android-aar.sh` (Android AAR), `apple-xcframework.sh`, `msys2-win32.sh`/`msys2-win64.sh`. The 1.0.20-stable tarball also contains `android-armv7-a.sh`, `android-armv8-a.sh`, `android-x86.sh`, `android-x86_64.sh`, `emscripten.sh`, `macos.sh` and `wasm32-wasi.sh`; `ls dist-build/` in your checkout. Zig also takes `-Dtarget=<target>` and `-Doptimize=ReleaseSmall`.

## Runtime checks
- Call `sodium_init()` once; returns 0 (initialised), 1 (already), -1 (failure).
- `sodium_version_string()` to log the version.

## Verify
- [ ] `make check` passes on the target; signature verified; version recorded in the SBOM.
