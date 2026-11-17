---
id: computing-software.cloud-infrastructure-engineering.docker.stripping-binaries-and-upx-in-images
name: stripping-binaries-and-upx-in-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-slimming, strip-binaries, upx, ldflags, trimpath, rust-strip, image-size]
level: practitioner
status: docs-checked
description: "Shrink compiled binaries before COPY into the runtime image: Go -ldflags=-s -w, Rust strip/LTO/opt-level, and a caution on UPX."
sources: ["https://pkg.go.dev/cmd/link", "https://doc.rust-lang.org/cargo/reference/profiles.html", "https://upx.github.io/", "https://docs.docker.com/build/building/best-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stripping binaries and UPX

For static-binary images (scratch/distroless), the binary is most of the image, so shrink it in the build stage.

## Per toolchain
```dockerfile
# Go: -s omits the symbol table and debug info, -w omits DWARF
RUN CGO_ENABLED=0 go build -ldflags="-s -w -X main.version=${VERSION}" -o /out/app ./cmd/app
```
```toml
# Rust Cargo.toml
[profile.release]
strip = true          # same as "symbols"; "debuginfo" strips only debug info
lto = "fat"           # whole-dependency-graph LTO, slower link
codegen-units = 1
opt-level = "z"       # optimise for size, turns off loop vectorisation; benchmark
panic = "abort"       # terminate on panic instead of unwinding
```
Cargo's default for `strip` is `"none"`. Keep an unstripped build as a CI artifact so crashes can still be symbolised.

## UPX
UPX is an executable packer; its own site claims roughly half to two thirds size reduction and no runtime or memory
penalty for most formats. Verify that for your binary and platform: measure the compressed layer size and start-up
memory in your registry and runtime before adopting it, and check that your scanners can still read packed binaries.

## Verify
- [ ] Image size compared before and after (`docker image ls`), and the binary still starts.
- [ ] Debug build retained somewhere for post-mortems.

## Checked
2026-11-01. Confirmed: Go linker `-s` and `-w` (pkg.go.dev cmd/link); Cargo profile `strip`, `lto`, `opt-level = "z"`,
`panic`, `codegen-units` (Cargo profiles reference); UPX claims as stated on upx.github.io. Removed: `-trimpath`,
GNU `strip`/`objcopy` lines, the 25-40% symbol share, UPX options and the list of UPX drawbacks (contradicted by or
absent from the UPX page; left to measurement), `docker buildx imagetools` command.
Method: documentation only; no commands were run.
