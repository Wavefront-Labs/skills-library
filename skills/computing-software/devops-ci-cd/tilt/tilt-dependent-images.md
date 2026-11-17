---
id: computing-software.devops-ci-cd.tilt.tilt-dependent-images
name: tilt-dependent-images
category: computing-software
field: devops-ci-cd
product: tilt
tags: [dependent-images, tilt, docker-build, live-update]
level: practitioner
status: docs-checked
description: "Move from one docker_build to several in Tilt: image selectors, tag matching, chaining a base image into an app image, and live_update placement."
sources:
  - "https://docs.tilt.dev/dependent_images.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependent images in Tilt

Goal: build several images, where one builds on another.

## One image

```python
docker_build('my-image', '.')
```

`my-image` is an image selector: Tilt matches any workload image containing that name regardless of tag. `.` is the build context, watched for changes. Unchanged image means containers do not restart; a changed image restarts them with the fresh image.

With a tag, only that exact tag matches (one mega image, several services):

```python
docker_build('my-mega-image:service-a', '.', entrypoint='/service-a')
docker_build('my-mega-image:service-b', '.', entrypoint='/service-b')
```

For custom resources see the custom resource guide.

## Base image plus app image

Base `base.dockerfile` includes `ADD package.json package.json` and `RUN npm install`; the app Dockerfile starts `FROM nodejs-express-base-image` then `ADD . .`.

```python
k8s_yaml('app.yml')
docker_build('nodejs-express-base-image',
             './package',
             dockerfile='base.dockerfile',
             build_args={'node_env': 'development'})
docker_build('nodejs-express-app-image',
             '.',
             dockerfile='app.dockerfile')
k8s_resource('nodejs-express-app', port_forwards=3000)
```

The base build uses `./package`, so it rebuilds only when files there change. On `tilt up`, Tilt builds both and injects the first image into the second (the FROM line is rewritten to a `tilt-` tagged reference). A change to `server.js` skips the base build.

## Live update

```
docker_build('nodejs-express-app-image',
             '.',
             dockerfile='app.dockerfile',
             live_update=[
               sync('.', '/var/www/app')
             ],
             entrypoint='yarn run nodemon /var/www/app/server.js')
```

Every app needs a sync step and a reload step; reload is language- and framework-specific (here nodemon via entrypoint). Attach `live_update` to the deployed image, never the base image, because Tilt matches the image in the container.

For unexpected rebuilds, see the file changes and live update reference guides.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/dependent_images.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Fixed the base.dockerfile description (the page shows it ends with ENTRYPOINT, not RUN npm install).

Method: documentation only; no commands were run.
