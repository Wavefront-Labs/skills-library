---
id: computing-software.cloud-infrastructure-engineering.aws.cdk-construct-library-publishing
name: cdk-construct-library-publishing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cdk, aws-cdk, construct-library, jsii, projen, construct-hub, npm, pypi, maven, nuget, l2-construct, l3-construct, semantic-versioning]
level: advanced
status: docs-checked
description: "Build and publish a reusable CDK construct library with projen and jsii to npm, PyPI, Maven and NuGet: API rules jsii enforces, testing, versioning and peer dependency pinning."
sources: ["https://projen.io/docs/project-types/aws-cdk-construct-library/", "https://github.com/projen/projen/blob/main/docs/project-types/aws-cdk-construct-library.md", "https://aws.github.io/jsii/user-guides/lib-author/typescript-restrictions/", "https://docs.aws.amazon.com/cdk/v2/guide/constructs.html", "https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing a CDK construct library (projen + jsii)

**Goal:** the platform team's `SecureBucket`, `StandardService` and `VpcBaseline` constructs
are installed by app teams in TypeScript, Python, Java or .NET from your package registry,
versioned, tested and with a stable API.

## 1. Scaffold with projen
```bash
mkdir platform-constructs && cd platform-constructs
npx projen new awscdk-construct --name @acme/platform-constructs \
  --author "Platform Team" --author-address platform@example.com \
  --repository-url https://github.com/acme/platform-constructs --cdk-version 2.89.0
```
projen owns `package.json`, `tsconfig`, `.github/workflows`, `.gitignore`; you edit
`.projenrc.ts` and run `npx projen` to regenerate. Do not hand-edit generated files.
```ts
// .projenrc.ts (excerpt)
const project = new awscdk.AwsCdkConstructLibrary({
  name: '@acme/platform-constructs', cdkVersion: '2.89.0', defaultReleaseBranch: 'main',
  publishToPypi: { distName: 'acme.platform-constructs', module: 'acme.platform_constructs' },
  publishToMaven: { javaPackage: 'com.acme.platform', mavenGroupId: 'com.acme', mavenArtifactId: 'platform-constructs' },
  publishToNuget: { dotNetNamespace: 'Acme.Platform', packageId: 'Acme.PlatformConstructs' },
});
project.synth();
```
`cdkVersion` is the minimum CDK version your library supports (`2.89.0` is only an example); keep it as low as your
code allows so consumers are not forced to upgrade. `cdkVersionPinning: true` pins an exact version, which projen does not recommend because every consumer must then use that exact CDK version.
If your library's public API exposes types from another jsii module, declare it in `peerDeps`; use `deps` only for implementation details.

## 2. Write jsii-compatible APIs
jsii compiles TypeScript into other languages, so the public API must be expressible in
all of them:
- Structs (interfaces whose names do not start with `I`) may only declare `readonly` properties; behavioural interfaces must start with `I`.
- jsii does not support declaring parameterized (generic) types; the built-in `Array<T>`, `Record<string, T>` and `Promise<T>` are allowed.
- Declarations named after a reserved word of a target language produce warnings, because they must be renamed in that language.
- Class members cannot share the PascalCased name of their declaring class.
- Constructs are exported from `src/index.ts`; keep internals un-exported.
```ts
export interface SecureBucketProps { readonly retentionDays?: number; readonly kmsKey?: kms.IKey; }
export class SecureBucket extends Construct {
  public readonly bucket: s3.Bucket;
  constructor(scope: Construct, id: string, props: SecureBucketProps = {}) {
    super(scope, id);
    this.bucket = new s3.Bucket(this, 'Bucket', {
      encryption: props.kmsKey ? s3.BucketEncryption.KMS : s3.BucketEncryption.S3_MANAGED,
      encryptionKey: props.kmsKey, enforceSSL: true, blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      lifecycleRules: props.retentionDays ? [{ expiration: Duration.days(props.retentionDays) }] : undefined });
  }
}
```

## 3. Test
`npx projen test` compiles and runs the automated tests; use `Template.fromStack(stack)` assertions
(`hasResourceProperties`, `resourceCountIs`) and snapshot tests sparingly.

## 4. Release
- By default every commit to the default branch releases a new version. The next minor or patch version is derived from conventional commits; **major versions must be bumped explicitly** to protect consumers.
- The release workflow builds, bumps the version with a commit, and publishes via publib. It needs repository secrets: `NPM_TOKEN` (npm), `NUGET_API_KEY` (.NET), `TWINE_USERNAME` and `TWINE_PASSWORD` (PyPI), and for Maven `MAVEN_GPG_PRIVATE_KEY`, `MAVEN_GPG_PRIVATE_KEY_PASSPHRASE`, `MAVEN_PASSWORD`, `MAVEN_USERNAME`, `MAVEN_STAGING_PROFILE_ID`.
- `npx projen package` runs jsii-pacmak to package the library; omit a `publishTo*` option to skip that language.

## Gotchas
- Changing a construct's internal logical IDs (the `id` passed to children) **replaces
  resources** in every consumer stack. Treat construct IDs as API; add tests that pin them.
- Do not bundle `aws-cdk-lib` or `constructs`; consumers should supply them so only one copy is loaded (projen configures them as peer dependencies).
- jsii errors appear at compile (`npx projen compile`); fix the API rather than casting around it.

## Verify
- [ ] `npx projen build` passes jsii compile and tests, and `npx projen package` produces every configured language target.
- [ ] A sample Python CDK app installs the package and synthesises using the construct.
- [ ] A `fix:` commit on main produces a patch release in all configured registries.
- [ ] Logical-ID pin test fails if a child id is renamed.

## Checked
Date: 2026-10-24. Sources: projen docs source for the AWS CDK construct library project type (main), jsii TypeScript restrictions page, CDK Developer Guide source.
Confirmed: awscdk-construct project type, cdkVersion as minimum version and cdkVersionPinning, deps versus peerDeps rule, publishToNuget/Maven/Pypi option names, publib secret names, release-on-every-commit with explicit major bumps, package task, jsii struct/generic/reserved-word rules.
Corrected: conventional commits do not produce major releases automatically (major bumps are explicit); the task is package, not package-all; jsii does not forbid unions or overloads per the restrictions page, so those claims were removed.
Removed as unconfirmed: npmRegistryUrl/twineRegistryUrl, Construct Hub auto-listing, pinned jsii and CDK versions, cdk-nag in tests.
Method: documentation only; no commands were run.
