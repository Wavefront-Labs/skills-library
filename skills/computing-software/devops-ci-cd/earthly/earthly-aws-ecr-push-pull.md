---
id: computing-software.devops-ci-cd.earthly.earthly-aws-ecr-push-pull
name: earthly-aws-ecr-push-pull
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, aws-ecr, ecr-login, credhelpers, save-image, push, aws-sdk-load-config, with-docker]
level: practitioner
status: docs-checked
description: "Push and pull images with AWS ECR from Earthly using SAVE IMAGE --push, the ecr-login credential helper, minimal IAM actions, and fixes for basic credentials not found and 401."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/registries/aws-ecr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Push and pull AWS ECR images with Earthly

Goal: build an image and push it to ECR without hand-rolled login glue.

## Earthfile

No special handling; use `SAVE IMAGE --push`:

```
FROM alpine:3.18

build:
    RUN echo "Hello from Earthly!" > motd
    ENTRYPOINT cat motd
    SAVE IMAGE --push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/hello-earthly:with-love
```

## Credentials

ECR does not issue permanent credentials; manual docker login tokens expire after 12 hours. Use the AWS ECR credential helper (included with Docker Desktop since 2.4.0.0). In the docker config file under `.docker/config.json`:

```
{
        "credHelpers": {
                "<aws_account_id>.dkr.ecr.<region>.amazonaws.com": "ecr-login"
        }
}
```

The helper honours `AWS_PROFILE` and works under an assumed role.

## IAM actions needed to push

`ecr:GetAuthorizationToken`, `ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage`, `ecr:BatchCheckLayerAvailability`, `ecr:PutImage`, `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload` (allowed for the push-pull user in the repository policy).

## Run

```bash
earthly --push +build
```

Pulling needs no special handling either:

```
FROM earthly/dind:alpine-3.19-docker-25.0.5-r0

run:
    WITH DOCKER --pull <aws_account_id>.dkr.ecr.<region>.amazonaws.com/hello-earthly:with-love
        RUN docker run <aws_account_id>.dkr.ecr.<region>.amazonaws.com/hello-earthly:with-love
    END
```

run with `earthly -P +run`.

## Troubleshooting

- `basic credentials not found`: your helper version may be old. Prepend `AWS_SDK_LOAD_CONFIG=true` to the earthly command to make the helper use the SDK over built-in config.
- 401 Unauthorized: check credentials (`aws configure`), IAM permissions, and that the correct assumed role is active in your shell; the same `AWS_SDK_LOAD_CONFIG=true` fix may help.
- With a pull-through-cache the helper may cause 401s when fetching metadata from the mirrored registry. Log in manually instead:
  ```
  aws ecr get-login-password | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
  ```

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: guides/registries/aws-ecr.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
