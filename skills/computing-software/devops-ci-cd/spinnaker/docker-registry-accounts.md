---
id: computing-software.devops-ci-cd.spinnaker.docker-registry-accounts
name: docker-registry-accounts
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [docker-registry, dockerhub, gcr, ecr, provider, images, accounts]
level: practitioner
status: docs-checked
description: "Configure Docker Registry accounts as Spinnaker image sources: v2 or OCI registries, explicit repository lists where no catalog exists."
sources:
  - https://spinnaker.io/docs/setup/install/providers/docker-registry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Docker Registry provider **only acts as a source of images**; it does not include support for deploying them. An Account maps to a credential able to authenticate against a set of Docker repositories.

**Prerequisites:** the registry must already exist and support the v2 registry API; OCI registries are also supported.

**Catalog endpoint.** If a registry supports `/_catalog` you do not have to list repositories. The page's table gives: GAR (`location-docker.pkg.dev`) yes, DockerHub (`index.docker.io`) no, Quay (`quay.io`) yes, ECR yes, ghcr (`ghcr.io`) no, JFrog Artifactory unknown.

**DockerHub** has no catalog endpoint, so list the repositories to index explicitly, for example `library/nginx yourusername/app`: the name is typically prefixed `library/` for most public images or `<username>/` for user images. Supply username and password for private images.

**GitHub Container Registry** also has no catalog endpoint, so you must define the repositories to cache. Images you do not list can still be deployed, but Spinnaker will not cache, trigger on or show them in dropdowns.

**Google Artifact Registry:** the typical address is `[LOCATION]-docker.pkg.dev/[PROJECT-ID]/[REPOSITORY]`, with `location-docker.pkg.dev` used for API calls. A service account is the preferred authentication, and with catalog permissions you need not list repositories. GAR uses OCI-compliant APIs and behaves a little differently from standard registries.

**Amazon ECR:** addresses are specific to an AWS account and region. Clouddriver runs the queries, so attach the `AmazonEC2ContainerRegistryReadOnly` managed policy to the IAM role or user Spinnaker runs as. The page's account uses `username: AWS` and a `passwordCommand` built from `aws ecr get-authorization-token`.

Accounts are added under `dockerRegistry` (`enabled`, `primaryAccount`, `accounts`) in `clouddriver-local.yml`. Further settings are in the Docker account properties the page links to.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Docker Registry page. Confirmed the provider limitation, prerequisites, catalog table and the DockerHub, GitHub Container Registry, GAR and ECR guidance. Replaced the old GCR section and the Halyard remarks with the current page's content, and removed the claim that Halyard warns about registries with no tags, which the page does not state.
