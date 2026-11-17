---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-containerized-python-components
name: kubeflow-pipelines-containerized-python-components
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [containerized-python-components, target-image, kfp-component-build, non-hermetic]
level: practitioner
status: docs-checked
description: "Build Containerized Python Components with base_image, target_image and kfp component build, so code can import local modules without being hermetic."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/user-guides/components/containerized-python-components.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines containerized python components

Containerized Python Components remove the hermetic constraint of lightweight components: source files are baked into an image. Prefer them in production, especially when a component would otherwise use `packages_to_install`.

Layout:

```text
src/
  my_component.py
  math_utils.py
```

`src/math_utils.py` holds the helper (`add_numbers`). `src/my_component.py` imports it inside the function:

```python
@dsl.component(base_image='python:3.11',
               target_image='gcr.io/my-project/my-component:v1')
def add(a: int, b: int) -> int:
    from math_utils import add_numbers
    return add_numbers(a, b)
```

- `target_image` is both the tag of the image KFP builds and the image the component runs in.
- `base_image` is used for the `FROM` instruction of the Dockerfile KFP builds from (the page says it defaults to `python:3.11` if omitted).

Build the image:

```sh
kfp component build src/ --component-filepattern my_component.py --no-push-image
```

Replace `--no-push-image` with `--push-image` once Docker is logged in to your private registry. Then import the component from `src.my_component` and compile the pipeline normally. The docs example's `gcr.io` image assumes the image was pushed to Google Cloud Artifact Registry and the pipeline runs on Vertex AI Pipelines with IAM permissions to pull it; whatever runs your pipeline needs pull access to the image.

## Checked

2026-11-09: confirmed against the Kubeflow website page "Containerized Python Components" (content/en/docs/components/pipelines/user-guides/components/containerized-python-components.md, read in full). Reworded the registry note to match the page.

Method: docs-checked 2026-11-09 against the Kubeflow website containerized-python-components page (raw markdown, read in full).
