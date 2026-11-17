---
id: computing-software.systems-network-administration.nix.eval-profiler-flamegraph
name: eval-profiler-flamegraph
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, eval-profiler, flamegraph, eval-profile-file]
level: advanced
status: docs-checked
description: "Profile Nix evaluation with --eval-profiler flamegraph, tune eval-profile-file and eval-profiler-frequency, and render the output with flamegraph.pl."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/advanced-topics/eval-profiler.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The evaluator samples the Nix function call stack at regular intervals; the output works with `flamegraph.pl`.

Enable with the `eval-profiler` setting:

```
nix-instantiate "<nixpkgs>" -A hello --eval-profiler flamegraph
```

Related settings:
- `eval-profile-file`: output file path.
- `eval-profiler-frequency`: stack sampling frequency.

By default the profile is written to `nix.profile` in the current directory.

Render:

```
flamegraph.pl nix.profile > flamegraph.svg
```

Profile lines give the call site location, then the called function name when available, for example `.../pkgs/top-level/default.nix:167:5:primop import`, meaning the `import` primop is called at line 167, column 5 of that file.

## Checked

2026-11-04. Confirmed against the Nix manual eval-profiler page: the `eval-profiler` setting and the `nix-instantiate` example, `eval-profile-file`, `eval-profiler-frequency`, the default `nix.profile` file in the working directory, the `flamegraph.pl` command, and the profile line format. Removed an unsourced verify line.

Method: documentation only; no commands were run.
