---
id: computing-software.systems-network-administration.nix.diff-hook-setup
name: diff-hook-setup
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, diff-hook, run-diff-hook, reproducibility]
level: advanced
status: docs-checked
description: "Configure the Nix diff-hook so a script shows how two build outputs differ, and know the user, write and trigger rules for the hook."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/advanced-topics/diff-hook.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `diff-hook` setting compares build results. It runs only when outputs differ; it does not decide whether they match.

`nix.conf`:

```
diff-hook = /etc/nix/my-diff-hook
run-diff-hook = true
```

`/etc/nix/my-diff-hook` must be executable:

```
#!/bin/sh
exec >&2
echo "For derivation $3:"
/run/current-system/sw/bin/diff -r "$1" "$2"
```

In the manual's example the script uses `$1` and `$2` as the two outputs to compare and `$3` as the derivation. Adjust the path to `diff` for your system.

The hook runs as the same user and group that performed the build and cannot write to the store path just built.

With the hook configured, the Nix daemon log shows the diff between the two outputs when a `--check` rebuild differs.

See the check-determinism skill for a `--check` build that triggers the hook.

## Checked

2026-11-04. Confirmed against the Nix manual Verifying Build Reproducibility page: `diff-hook` and `run-diff-hook` in `nix.conf`, the example hook script, that the hook only runs when results differ, the same user and group, no write access to the built path, and the daemon log output. Softened the claim about `$1`, `$2` and `$3` to what the example shows.

Method: documentation only; no commands were run.
