---
id: computing-software.cloud-infrastructure-engineering.docker.pr-builds-load-and-test-without-push
name: pr-builds-load-and-test-without-push
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, pr-build, load-and-test, pull-request-ci, build-push-action, buildx-load, fork-pull-requests, image-scan, github-actions, ci-builds]
level: practitioner
status: docs-checked
description: "Validate images on pull requests without pushing: buildx --load then run tests, test stages, handling multi-platform, fork PRs without secrets, caches, and scans of the local image."
sources: ["https://docs.docker.com/build/ci/github-actions/test-before-push/", "https://docs.docker.com/build/ci/github-actions/share-image-jobs/", "https://github.com/docker/build-push-action", "https://github.com/docker/setup-docker-action", "https://github.com/aquasecurity/trivy-action", "https://docs.docker.com/reference/cli/docker/scout/cves/", "https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PR builds: load and test without push

**Goal:** every pull request builds the exact image that would ship, runs tests against it,
scans it, and never pushes anything or needs registry credentials.

## Build → load → test (GitHub Actions)
```yaml
on: pull_request
jobs:
  image:
    runs-on: ubuntu-latest
    permissions: { contents: read }
    steps:
      - uses: actions/checkout@v7
      - uses: docker/setup-buildx-action@v4
      - uses: docker/build-push-action@v7
        with:
          context: .
          load: true                     # into the runner's docker image store
          push: false
          tags: app:pr-${{ github.event.pull_request.number }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      - name: Smoke test
        run: |
          docker run -d --name app -p 8080:8080 app:pr-${{ github.event.pull_request.number }}
          for i in $(seq 30); do curl -fs localhost:8080/healthz && break; sleep 1; done
          curl -fs localhost:8080/healthz
      - name: Integration tests
        run: docker compose -f compose.ci.yaml up --exit-code-from tests --abort-on-container-exit
        env: { APP_IMAGE: "app:pr-${{ github.event.pull_request.number }}" }
```
- `--exit-code-from tests` returns the exit code of the selected service container (and implies
  `--abort-on-container-exit`).
- Reference the loaded tag in `compose.ci.yaml` via `image: ${APP_IMAGE}` and no `build:`,
  so Compose does not rebuild.

## Multi-platform PRs
`load: true` needs an image store that supports manifest lists; Docker's docs say the Docker
exporter does not support manifest lists, so multi-platform results cannot be loaded into a
classic store. Options:
- Load and test one platform; additionally run a build-only job for the full platform list
  (`push: false`, no load) to catch failures on the other platforms.
- Enable the containerd image store on the runner (`docker/setup-docker-action` accepts a
  `daemon-config` input with `"features": {"containerd-snapshotter": true}`).

## Tests inside the build
A `test` stage (`FROM build AS test` + `RUN npm test`) built with `target: test` fails the
build on test failure, using the build cache. Good for unit tests; integration tests that
need other services belong after `--load`.

## Fork PRs
A PR build should not need registry credentials. Do not switch to `pull_request_target` to
get secrets while building fork code: GitHub's events documentation warns about the security
risks of that trigger, and the fork's Dockerfile `RUN` steps would run with your secrets.

## Scan the local image
```yaml
      - uses: aquasecurity/trivy-action@v0.36.0
        with: { image-ref: "app:pr-${{ github.event.pull_request.number }}", exit-code: "1", severity: "CRITICAL,HIGH", ignore-unfixed: true }
```
or `docker scout cves local://app:pr-N --exit-code --only-severity critical,high`
(`local://` uses an image from the local store; `--exit-code` and `--only-severity` are
documented options of `docker scout cves`).

## Sharing the image across jobs
```yaml
          outputs: type=docker,dest=${{ runner.temp }}/app.tar
      - uses: actions/upload-artifact@v7
        with: { name: app-image, path: "${{ runner.temp }}/app.tar" }
# next job: download-artifact, then docker load -i app.tar (single-platform images only)
```

## Verify
Open a PR that breaks a test: the image job fails at "Integration tests" and nothing is pushed.

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), docker/cli system events reference, Compose and Scout CLI reference data, dive, uv and distroless READMEs, action repositories at their latest releases. Confirmed: current majors of build-push-action (v7), setup-buildx-action (v4), checkout (v7), upload-artifact (v7) and trivy-action (v0.36.0, per its README); build-push-action load/push inputs; Docker docs note that the Docker exporter does not support manifest lists (share-image-jobs page) and the multi-platform image-store prerequisites; setup-docker-action daemon-config input; docker compose up --exit-code-from; docker scout cves local:// scheme, --exit-code and --only-severity options. Removed the exact exporter error string, fork-PR cache and token claims and the registry-tag verification wording.

Method: documentation only; no commands were run.
