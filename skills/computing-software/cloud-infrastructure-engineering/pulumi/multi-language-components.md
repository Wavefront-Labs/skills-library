---
id: computing-software.cloud-infrastructure-engineering.pulumi.multi-language-components
name: multi-language-components
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, multi-language-component, mlc, component-provider, pulumi-package-add]
level: practitioner
status: docs-checked
description: "Consume a Pulumi component from any language with pulumi package add (Git URL or local folder) or pre-published SDKs; runtime requirements."
sources:
  - https://www.pulumi.com/docs/iac/concepts/resources/components/
  - https://www.pulumi.com/docs/iac/guides/building-extending/packages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-language components

A component distributed as a Pulumi package carries a plugin, so it can be consumed from any Pulumi language. Two routes:

1. **Generated on demand** (source-based package): from your program's directory
```bash
pulumi package add github.com/my-org/my-component@v1.0.0
pulumi package add /path/to/local/secure-s3-component    # monorepo / rapid iteration; reads the schema from disk
```
Pulumi fetches the package source, generates a local SDK from the component's schema in your language, and makes it importable. This is how components from a source-based plugin package are consumed across languages, common for internal components published via Git or the Pulumi IDP Private Registry.

2. **Pre-published SDKs**: installed with the native package manager (for example `npm install @pulumi/awsx`), no `package add` and no extra runtime beyond your toolchain. Executable-based packages (needed for the public Pulumi Registry) are typically published this way.

## Gotchas
- SDK generation runs a live plugin, so it must be executable on the machine: the requirements are the same as for a Pulumi program written in the component's authoring language.
- Native language packages (plain npm/PyPI/etc. libraries, no plugin) work only in their authoring language.
- Authoring and packaging details are in the "Build a Component" and "Packaging Components" guides; the guides page used by the earlier draft was not available, so provider-host code, `PulumiPlugin.yaml`, argument restrictions and gen-sdk are not covered here.

## Checked
2026-11-03. Confirmed on the Component resources concept page and the Packages guide (source-based vs executable-based models). Removed: the TypeScript `componentProviderHost` example, `PulumiPlugin.yaml`, `package gen-sdk`, `@v1.2.0` example, `sdks/` directory claim, argument serialization rules and the Verify paragraph.
Method: documentation only; no commands were run.
