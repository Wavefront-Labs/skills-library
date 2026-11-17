---
id: computing-software.devops-ci-cd.earthly.earthly-secrets
name: earthly-secrets
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, secret, run-secret, earthly-secrets, secret-file, mount, caching, cloud-secrets]
level: practitioner
status: docs-checked
description: "Use secrets in Earthly with RUN --secret and --mount type=secret, supply values via --secret, EARTHLY_SECRETS or a .secret file, and know why secrets do not affect the cache."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/secrets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Secrets in Earthly

Goal: give a `RUN` command a sensitive value without writing it in the Earthfile or the image.

## Declare in the command

Expose secret `passwd` as environment variable `mypassword`:

```dockerfile
FROM alpine:latest
hush:
    RUN --secret mypassword=passwd echo "my password is $mypassword"
```

Shorthand when the variable name equals the secret ID:

```dockerfile
    RUN --secret passwd echo "my password is $passwd"
```

Mount it as a temporary file instead (not saved to the image snapshot):

```dockerfile
RUN --mount type=secret,target=/root/mypassword,id=passwd echo "my password is $(cat /root/mypassword)"
```

## Supply the value

1. Command line: `earthly --secret passwd=itsasecret +hush`
2. From an env var of the same name (omit the value):
   ```bash
   export passwd=itsasecret
   earthly --secret passwd +hush
   ```
3. `EARTHLY_SECRETS`, comma-separated for several:
   ```bash
   export EARTHLY_SECRETS="passwd=itsasecret"
   earthly +hush
   ```
4. A `.secret` file in the directory you run `earthly` from, containing `passwd=itsasecret`.
5. Cloud-based secrets, to share within a team (set with `earthly secrets set ...` after creating an Earthly account).

## Caching gotcha

Command hashes include the command text and the args of the target, but not secret contents. If a secret changes, Earthly cannot detect it and the command is not re-evaluated.

## Storage

Command-line secrets are held in memory on the local host until `earthly` exits. BuildKit requests them from the earthly process when evaluating the `RUN` and mounts them temporarily in the runc container, unmounting afterwards; they are not persisted in the snapshot. Secrets reach the cloud only if you explicitly run `earthly secrets set ...`.

## Checked

2026-11-07. Read docs/guides/secrets.md in full. RUN --secret forms, mount form, the five ways to supply values, the caching note and storage description match. Nothing removed.
Method: documentation only; no commands were run.
