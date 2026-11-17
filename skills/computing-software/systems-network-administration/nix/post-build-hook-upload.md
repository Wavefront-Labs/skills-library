---
id: computing-software.systems-network-administration.nix.post-build-hook-upload
name: post-build-hook-upload
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, post-build-hook, s3-cache, out-paths, nix-copy]
level: advanced
status: docs-checked
description: "Upload every local build to an S3 binary cache with a Nix post-build-hook script using OUT_PATHS, with the blocking-build-loop caveat and a test."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/advanced-topics/post-build-hook.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Caveat: the hook runs after each build and blocks the build loop; the loop exits if the hook fails, so Nix becomes slow or unusable on a slow or unreliable connection. Prerequisite: an S3-compatible binary cache as a substituter, with root's default AWS profile able to upload.

Script `/etc/nix/upload-to-cache.sh`:

```
#!/bin/sh

set -eu
set -f # disable globbing
export IFS=' '

echo "Uploading paths" $OUT_PATHS
exec nix copy --to "s3://example-nix-cache" $OUT_PATHS
```

Word splitting makes each output path its own argument; `set -f` stops store-path glob characters expanding. `$DRV_PATH` works the same for `.drv` files.

```
chmod +x /etc/nix/upload-to-cache.sh
```

End of `/etc/nix/nix.conf`:

```
post-build-hook = /etc/nix/upload-to-cache.sh
```

Restart `nix-daemon`.

Test:

```
nix-build --expr '(import <nixpkgs> {}).writeText "example" (builtins.toString builtins.currentTime)'
nix-store --delete /nix/store/<path>
nix-store --realise /nix/store/<path>
```

The last command should copy the path back from the S3 cache. The page also generates a signing key with `nix-store --generate-binary-cache-key`, lists the public key under `trusted-public-keys` and the private key file under `secret-key-files`.

## Checked

2026-11-04: caveats, prerequisites, script, word-splitting note, chmod, nix.conf line, daemon restart and the test sequence confirmed against the post-build-hook manual page. Replaced a reference to another skill with what the page says about signing keys.

Method: documentation only; no commands were run.
