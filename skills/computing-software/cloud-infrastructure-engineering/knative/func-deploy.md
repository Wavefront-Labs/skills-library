---
id: computing-software.cloud-infrastructure-engineering.knative.func-deploy
name: func-deploy
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [func-deploy, raw-deployer, registry, func-username, knative-service]
level: practitioner
status: docs-checked
description: "Deploy a function as a Knative Service with func deploy, or as a raw Deployment with the raw deployer."
sources:
  - https://knative.dev/docs/functions/deploying-functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: publish a function image and run it on the cluster.

Deploying a function creates an OCI container image, pushes it to your image registry, and deploys the function to the cluster as a Knative Service. Redeploying updates the container image and the resulting Service.

Prerequisites:
- A Docker daemon on your local machine.
- A container registry you can push images to. Some registries make newly pushed images private by default, so for a first-time deploy you may need to make sure the images are public.

Procedure, run inside the project directory:

```bash
func deploy --registry <registry>
```

The `kn func deploy` form is identical. The project name becomes the Knative Service name. The project name and registry name are used to build the fully qualified image name. Expected output ends with the function deployed in its namespace and exposed at a URL such as `http://hello.default.127.0.0.1.sslip.io`.

To deploy as a plain Kubernetes Deployment and Service rather than a Knative Service, add `--deployer raw`.

For private registries, export `FUNC_USERNAME` and `FUNC_PASSWORD`. This works with the `host`, `s2i` and `pack` builders and is more secure than the `--password` flag, since command-line arguments are visible to all users through `ps`.

Verify the deployment with `func invoke` and observe its output.

## Checked

2026-11-04. Confirmed against the Deploying functions page and its included snippets (knative/docs source): deploy builds an OCI image, pushes it to the registry and deploys a Knative Service, redeploy updates the image and Service, the Docker daemon and registry prerequisites, `func deploy --registry <registry>` and the `kn func` form, the project name used as the Service name, the `--deployer raw` option, the sslip.io example URL, the `FUNC_USERNAME` and `FUNC_PASSWORD` note, and `func invoke` verification. Replaced the 'or a pull secret' suggestion, which the page does not make, with the page's advice to make sure images are public.

Method: documentation only; no commands were run.
