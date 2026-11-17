---
id: computing-software.cybersecurity-defensive.trivy.run-trivy-plugins-and-output-mode
name: run-trivy-plugins-and-output-mode
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [plugin-run, run-as-plugin, output-plugin, output-plugin-arg, kubectl-plugin, stdin]
level: advanced
status: docs-checked
description: "Invoke installed plugins as subcommands, run them on the fly, and pipe scan results into an output-mode plugin using --output plugin= and --output-plugin-arg."
sources:
  - https://trivy.dev/latest/docs/guide/plugin/user-guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Using plugins: Trivy loads all plugins in the cache at start. Each appears as a CLI subcommand named after the plugin, listed under Plugin Commands in `trivy --help`. Example with the kubectl plugin, passing Trivy flags after `--`:

```
trivy kubectl deployment <deployment-id> -- --ignore-unfixed --severity CRITICAL
```

Internally it calls the kubectl binary to fetch the deployment and passes its images to Trivy. To omit the subcommand, set `TRIVY_RUN_AS_PLUGIN`:

```bash
TRIVY_RUN_AS_PLUGIN=kubectl trivy job your-job -- --format json
```

`trivy plugin run` installs a plugin and runs it on the fly, skipping installation if it is already cached:

```bash
trivy plugin run kubectl pod your-pod -- --exit-code 1
```

Output mode (experimental): plugins that support it, marked in the OUTPUT column of `trivy plugin search` or `trivy plugin list`, process Trivy's output as part of a built-in command.

```bash
trivy image --format json --output plugin=<plugin_name> [--output-plugin-arg <plugin_flags>] <image_name>
```

Results arrive on standard input, so plugins must handle stdin and must read all data from it before exiting, or Trivy can hang. Other formats such as `--format cyclonedx` also work. `--output-plugin-arg` is forwarded as arguments: `--output plugin=myplugin --output-plugin-arg "--foo --bar=baz"` runs `myplugin --foo --bar=baz`. The `count` plugin example uses `--output-plugin-arg "--published-after 2023-10-01"` on `debian:12`.

## Checked

2026-11-03. Read and confirmed against the Plugins User Guide on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
