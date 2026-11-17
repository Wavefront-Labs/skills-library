---
id: computing-software.cloud-infrastructure-engineering.pulumi.component-resources
name: component-resources
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, component-resource, componentresource, registeroutputs, pulumi-component]
level: practitioner
status: docs-checked
description: "Pulumi component resources: logical groupings exposed as one resource, how they are distributed and consumed, parent trees, and options that differ."
sources:
  - https://www.pulumi.com/docs/iac/concepts/resources/components/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/parent/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Component resources

A component is a logical grouping of Pulumi resources exposed as a single resource, hiding implementation behind a defined interface (analogous to Terraform modules and AWS CDK Constructs). You author one by extending the `ComponentResource` class. It can be defined inline, shared through a language library, or shipped in a Pulumi package; a package can hold several components next to custom resources and functions. Examples: `awsx.ec2.Vpc`, `awsx.ecs.FargateService`, `awsx.ecr.Repository`, or your own `SecureS3Bucket` that bakes in encryption.

**Consuming** depends on distribution:
- Local (same repo): import the class with the language's normal mechanism.
- Native language package (npm, PyPI, NuGet, Maven, Go modules): install with the language's package manager; usable only in the authoring language.
- Pulumi package without published SDKs: `pulumi package add github.com/my-org/my-component@v1.0.0` or `pulumi package add /path/to/local/component`. Pulumi fetches the source (or reads the local folder), generates an SDK from the component's schema, and wires it into the project. The plugin must be executable on your machine.
- Pulumi package with pre-published SDKs (such as AWSx): install the per-language SDK, e.g. `npm install @pulumi/awsx` or `pip install pulumi-awsx`.

Instantiate like any resource: a name, arguments defined by the author, and resource options such as `protect`.

**Parent tree.** Children created with the `parent` resource option show nested under the component in `pulumi up` output, and inherit additional resource options from the parent. `parent` applies to both custom and component resources.

## Gotchas
- Options do not always behave the same on a component: the `provider` option has no effect on a component; use `providers` to pass explicit provider configuration to its children.
- Program-first (bulk) import can generate an import file for a component and all its children.
- The "Build a Component" guide covers argument structure, child resources, `registerOutputs` and provider inheritance; this skill does not reproduce its code.

## Checked
2026-11-03. Confirmed on the Component resources concept page and the `parent` option page. The Build a Component guide URL returned 404, so the TypeScript/Python class samples, the type token format, `registerOutputs` ordering, naming and alias claims and the `pulumi stack --show-urns` Verify were removed.
Method: documentation only; no commands were run.
