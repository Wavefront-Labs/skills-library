---
id: computing-software.devops-ci-cd.skaffold.google-cloud-build
name: google-cloud-build
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [googlecloudbuild, gcb, cloud-build, gcs]
level: advanced
status: docs-checked
description: "Run builds on Google Cloud Build, understand what it uploads and ignores, and configure the project, machine and builder images."
sources:
  - "https://skaffold.dev/docs/builders/build-environments/cloud-build/"
  - "https://skaffold.dev/docs/builders/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`build.googleCloudBuild` sends builds to Google Cloud Build. After the build, artifacts are saved to the specified remote registry.

```yaml
build:
  googleCloudBuild:
    projectId: my-project
    diskSizeGb: 100
    timeout: 1200s
    logging: LEGACY
    concurrency: 2
```

How it works, per the docs: Skaffold creates a list of dependent files, uploads a tar file of them to Google Cloud Storage, submits it to Cloud Build, generates a single-step `cloudbuild.yaml` and starts the build. This differs from `gcloud builds submit`.

Gotchas:

- It does not honour `.gitignore` or `.gcloudignore`. Use `.dockerignore` to exclude files.
- Any `cloudbuild.yaml` you already have is not used.
- By default all artifacts build in parallel; set `concurrency` to a non-zero value to cap it (for example if you hit a quota). Logs still print in sequence.

Options (schema `GoogleCloudBuild`): `projectId` (if omitted, guessed from an image name such as `gcr.io/myproject/image`), `bucket` (Cloud Storage bucket for staged sources), `diskSizeGb`, `machineType`, `timeout`, `region`, `workerPool`, `serviceAccount`, `logging`, `logStreamingOption`, `concurrency`, and builder images `dockerImage`, `kanikoImage`, `mavenImage`, `gradleImage`, `packImage` and `koImage`. `logging` accepts `LOGGING_UNSPECIFIED` and `LEGACY` (legacy is the schema default), among other documented modes. The logged-in user needs permission to trigger builds.

Supported builders: the Cloud Build page's Restrictions section lists Docker and Jib only. The Build overview matrix also marks Cloud Native Buildpacks and ko as supported on Cloud Build, and the schema has `packImage` and `koImage`, so the pages disagree; treat Docker and Jib as certain and test buildpacks or ko before relying on them.

Because the upload is a tar of dependency files, a large build context is slow. Keep the context small, list exclusions in `.dockerignore`, and keep local secrets out of the uploaded directory.

## Checked

2026-11-04. Read the Skaffold Google Cloud Build page, the Build overview support matrix and the `GoogleCloudBuild` definition in the v4beta14 schema. Confirmed the upload flow, ignore behaviour, concurrency, option names and defaults. Removed: the example machine type value (not on the pages), the claim about a default bucket, the claim that credentials and bucket permissions are required in those words, and "pin builder images". Conflict: supported builders differ between the Restrictions section and the overview matrix, as noted above.
Method: documentation only; no commands were run.
