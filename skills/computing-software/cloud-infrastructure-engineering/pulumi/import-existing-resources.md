---
id: computing-software.cloud-infrastructure-engineering.pulumi.import-existing-resources
name: import-existing-resources
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-import, import-resource-option, generate-code, adopt-resources]
level: practitioner
status: docs-checked
description: "Adopt existing cloud resources into Pulumi with pulumi import, bulk JSON files, the import resource option, and generated code."
sources:
  - https://www.pulumi.com/docs/iac/guides/migration/import/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_import/
  - https://www.pulumi.com/docs/iac/concepts/resources/options/import/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing existing resources

```bash
# type token, name in your program, cloud ID
pulumi import aws:s3/bucket:Bucket site my-existing-bucket
pulumi import aws:ec2/vpc:Vpc main vpc-0abc123 --out imported.ts   # write generated code to a file
pulumi import --file resources.json --yes                           # bulk
```
```json
{"resources":[{"type":"aws:s3/bucket:Bucket","name":"site","id":"my-existing-bucket"}]}
```

Code-based alternative (declarative, reviewable in a PR):
```typescript
new aws.s3.Bucket("site", { bucket: "my-existing-bucket" }, { import: "my-existing-bucket" });
```
With the `import` option, specify all required arguments so the resource exactly matches the existing one. Remove the `import` option once the import succeeds.

## Gotchas
- Paste the generated code into the program, then run `pulumi preview` before changing anything else: it should report no changes, and any proposed change is a difference the import did not resolve.
- Find the type token and the lookup property (the ID) in the Import section of each resource's page in the Pulumi Registry; the name you give becomes the resource's logical name and must be unique among resources of that type in the program.
- `pulumi import` marks imported resources as protected by default (the generated code has `protect: true`); to destroy them, remove `protect` and run an update first, or pass `--protect=false`.
- Use `--parent` and `--provider` (`name=urn`) to import under a parent or a non-default provider.

## Verify
`pulumi preview --diff` reports no changes for the imported resource; `pulumi stack --show-urns` lists its URN.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Importing resources guide (type token, lookup property, name, protected output, preview should show no changes), the `pulumi import` CLI reference (`--file`, `--out`, `--yes`, `--protect`, `--parent`, `--provider`, JSON format) and the import resource option page. Fixed: the skill said imported resources are not protected, but the CLI protects them by default. Removed: the invented composite ID example and the `pulumi state rename` duplicate-URN advice; replaced the dead `guides/adopting/import` source with `guides/migration/import`.
Method: documentation only; no commands were run.
