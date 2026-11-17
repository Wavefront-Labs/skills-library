---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-clone-troubleshooting
name: woodpecker-clone-troubleshooting
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [troubleshooting, clone-errors, netrc]
level: practitioner
status: docs-checked
description: "Debug Woodpecker clone failures such as could not read Username by testing from a held container."
sources: ["https://woodpecker-ci.org/docs/usage/troubleshooting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debugging Woodpecker clone issues

An error like `fatal: could not read Username for 'https://<url>': No such device or address` has several possible causes.

Step 1: for internal repositories, enable authenticated cloning on the server:

```ini
WOODPECKER_AUTHENTICATE_PUBLIC_REPOS=true
```

Step 2: check the container can reach your Git server. Disable the clone and make a container hang:

```yaml
skip_clone: true
steps:
  build:
    image: debian:stable-backports
    commands:
      - apt update
      - apt install -y inetutils-ping wget
      - ping -c 4 git.example.com
      - wget git.example.com
      - sleep 9999999
```

Find the container with `docker ps` and enter it with `docker exec -it <container-id> bash`. Then repeat the clone commands from the failing pipeline:

```bash
git init
git remote add origin https://git.example.com/username/repo.git
git fetch --no-tags origin +refs/heads/branch:
```

Replace the URL and branch, and use your own credentials to log in.

## Checked

2026-11-08. Read the Woodpecker troubleshooting page in full (raw markdown) and confirmed the error text, WOODPECKER_AUTHENTICATE_PUBLIC_REPOS, the skip_clone hang pipeline, docker ps and docker exec steps, and the manual git commands. Removed: the Gitea/Forgejo same-host Docker network paragraph and WOODPECKER_BACKEND_DOCKER_NETWORK, which the page does not state.

Method: documentation only; no commands were run.
