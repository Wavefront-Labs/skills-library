---
id: computing-software.devops-ci-cd.earthly.earthly-interactive-debugging
name: earthly-interactive-debugging
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, interactive, debugging, with-docker, root-shell, run-false, privileged]
level: practitioner
status: docs-checked
description: "Drop into a root shell inside a failed Earthly RUN with earthly -i, including inside WITH DOCKER (add -P), then fix the Earthfile since changes made in the shell are not saved."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/debugging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debug a failing Earthly build interactively

Goal: inspect the container state at the point a `RUN` fails instead of sprinkling print statements.

## Steps

1. Re-run the target with `--interactive` (short form `-i`):

   ```bash
   earthly -i +test
   ```

2. On failure Earthly does not exit; it prints `Entering interactive debugger` and gives a root shell in the build container (prompt like `root@buildkitsandbox:/code#`). Run any commands: `ls`, `find / | grep sherlock.txt`, try a manual `mv`, re-run the failing command.
3. Leave with `exit` or ctrl-D.
4. Edit the Earthfile. The docs are explicit: even if you fixed things inside the shell, the image is not saved, so the fix must be made in the Earthfile.

## Inside WITH DOCKER

The page debugs a `WITH DOCKER` integration test by running it with `-P` as well:

```bash
earthly -P -i +test
```

You land in the environment around the embedded Docker daemon, so `docker ps -a` and `curl -s localhost:8000` work from the shell to look at the running containers.

## Break at any point

To get a shell at an arbitrary place in an Earthfile, add a command that fails:

```
  RUN false
```

and run with `-i`.

## Gotchas stated by the docs

- The prompt warns: only a single debugger per host is supported.
- Without `-i` a failing `RUN` just prints the failure and exits with the error.

## Checked

2026-11-07. Read docs/guides/debugging.md in full. The -i flag, debugger message, root shell, unsaved-changes note, WITH DOCKER example, RUN false tip and single-debugger warning match. Corrected: the -P flag is described as used in the page's WITH DOCKER example rather than stated as a requirement.
Method: documentation only; no commands were run.
