---
id: computing-software.software-engineering.elixir.hex-publish-package-metadata
name: hex-publish-package-metadata
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, hex-publish, package, licenses, hex-build, hex-owner, hex-retire, semver]
level: advanced
status: docs-checked
description: "Prepare package metadata in mix.exs, build and inspect the tarball, publish with mix hex.publish and retire bad releases."
sources: ["https://hex.pm/docs/publish"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing a package to Hex

**Goal:** release a library to Hex.pm correctly.

```elixir
def project do
  [app: :mylib, version: "0.1.0", description: "Short description", package: package(), docs: docs()]
end
defp package do
  [licenses: ["Apache-2.0"], links: %{"GitHub" => "https://github.com/me/mylib"},
   files: ~w(lib mix.exs README.md LICENSE CHANGELOG.md)]
end
```
```bash
mix hex.user auth
mix hex.publish               # lists included files, prompts for confirmation; also publishes docs
mix hex.publish --revert 0.1.0
```

## Rules
- Follow Semantic Versioning; dependencies must come from Hex (no git/path deps in published packages).
- You can publish again for up to one hour after first publication; a publication can also be reverted with `mix hex.publish --revert VERSION`.
- Include only needed files; read the `Included files` list before confirming. Published packages are scanned for leaked credentials, but rotating a leaked credential is the fix.
- In CI prefer Workload Identity (Trusted Publishing) on GitHub Actions; otherwise use a key limited to publish permissions in `HEX_API_KEY` and `--yes`.

## Self-check
Read the `Included files` list from `mix hex.publish` and confirm no credentials or test fixtures ship.

## Checked
2026-11-08: confirmed against the Hex publish guide (package fields, files, licenses, links, Hex-only dependencies, hex.publish prompt and docs, one-hour republish window, --revert, HEX_API_KEY, --yes, Workload Identity, secret scanning). Removed: hex.user register, hex.build, hex.publish --dry-run, hex.retire with its reason list, and --unpack.
Method: documentation only; no commands were run.
