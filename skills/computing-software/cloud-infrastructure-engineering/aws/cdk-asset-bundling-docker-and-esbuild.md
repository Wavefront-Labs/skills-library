---
id: computing-software.cloud-infrastructure-engineering.aws.cdk-asset-bundling-docker-and-esbuild
name: cdk-asset-bundling-docker-and-esbuild
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cdk, asset-bundling, docker-assets, esbuild, nodejsfunction, container-assets, cdk-assets]
level: practitioner
status: docs-checked
description: "Bundle CDK assets reliably: NodejsFunction with local esbuild, Docker bundling images for Python and Go, DockerImageAsset platforms, asset hashing and CI caching."
sources: ["https://docs.aws.amazon.com/cdk/v2/guide/assets.html", "https://docs.aws.amazon.com/cdk/v2/guide/build-containers.html", "https://docs.aws.amazon.com/cdk/v2/guide/customize-synth.html", "https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/aws-lambda-nodejs/README.md", "https://github.com/aws/aws-cdk/blob/main/packages/%40aws-cdk/aws-lambda-python-alpha/README.md", "https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/aws-ecr-assets/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDK asset bundling with Docker and esbuild

## How assets work
`cdk synth` stages files into `cdk.out/asset.<hash>`; `cdk deploy` uploads file assets to the
bootstrap bucket (`cdk-hnb659fds-assets-<acct>-<region>`) and image assets to the bootstrap ECR
repo (`cdk-hnb659fds-container-assets-...`). The hash decides whether a re-upload happens.

## Node.js: NodejsFunction
```ts
new NodejsFunction(this, 'Api', {
  entry: 'src/api.ts', runtime: Runtime.NODEJS_22_X, architecture: Architecture.ARM_64,
  bundling: { minify: true, sourceMap: true, nodeModules: ['sharp'] },   // installed, not bundled (native deps)
});
```
- Uses **esbuild locally** if it is available; otherwise bundles in a Lambda-compatible Docker container. Installing esbuild (`npm i -D esbuild`) avoids the Docker dependency in CI.
- For Node.js 18 and later runtimes all `@aws-sdk/*` packages are excluded from the bundle by default (the runtime provides SDK v3). Override with `bundling.externalModules` if you need to bundle a specific SDK version.
- Modules listed in `nodeModules` are not bundled but installed into the package's `node_modules`; they must be in `package.json` dependencies. For modules with native dependencies set `bundling.forceDockerBundling: true` so they install in a Lambda-compatible environment.

## Python / Go: Docker bundling
```ts
Code.fromAsset('src/py', { bundling: {
  image: Runtime.PYTHON_3_12.bundlingImage,
  command: ['bash', '-c', 'pip install -r requirements.txt -t /asset-output && cp -au . /asset-output'],
  platform: 'linux/arm64',
}});
```
- Optional `local: { tryBundle(outputDir) {...; return true;} }` to skip Docker on dev machines.
- `@aws-cdk/aws-lambda-python-alpha` `PythonFunction` wraps this: it installs dependencies when it finds `requirements.txt`, `Pipfile`, `uv.lock` or `poetry.lock` at the entry path.
- Set the `CDK_DOCKER` environment variable to the path of the binary (for example Finch) if Docker is not the container engine. Aliases and symlinks are not supported.

## Container images
```ts
const img = new DockerImageAsset(this, 'Img', { directory: 'svc', platform: Platform.LINUX_ARM64,
  buildArgs: { VERSION: '1.2' }, exclude: ['node_modules', '.git'] });
ContainerImage.fromDockerImageAsset(img);
```
- `.dockerignore` and/or the `exclude` property keep unneeded files out of the build context (patterns in `exclude` are appended to `.dockerignore`); the recommended `ignoreMode` for Docker image assets is `IgnoreMode.DOCKER`.

## CI tips
- `cdk deploy --exclusively Stack` deploys only the named stacks without dependencies; `--asset-parallelism` builds and publishes assets in parallel.
- `NodejsFunction` hashes the bundled output by default (`AssetHashType.OUTPUT`), so non-deterministic bundle output changes the hash on every build. You can pass a custom `assetHash`, but you must then change it whenever the asset changes or deployments may not be invalidated.

## Verify
- [ ] `cdk synth` works without Docker for Node functions when esbuild is installed locally.
- [ ] Two consecutive synths produce the same asset hashes.
- [ ] Deployed function size and architecture match expectations.

## Checked
Date: 2026-10-24. Sources: AWS CDK Developer Guide source (awsdocs/aws-cdk-guide, main), and the aws-cdk repository READMEs and runtime.ts (main branch).
Confirmed: default bootstrap bucket and ECR repository names and the hnb659fds qualifier; CDK_DOCKER takes the binary path and aliases are unsupported; NodejsFunction uses local esbuild else Docker, forceDockerBundling and nodeModules semantics, @aws-sdk/* excluded by default for Node 18+, output-based asset hash; PythonFunction lockfile detection; DockerImageAsset platform, exclude and .dockerignore behaviour; Runtime.NODEJS_22_X and PYTHON_3_12 exist; deploy flags --exclusively and --asset-parallelism.
Removed as unconfirmed: CI caching advice, cross-arch buildx/QEMU claim, cdk-assets publish pipeline claim.
Method: documentation only; no commands were run.
