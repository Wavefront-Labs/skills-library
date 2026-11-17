---
id: computing-software.cloud-infrastructure-engineering.docker.dockerfile-variable-substitution
name: dockerfile-variable-substitution
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, arg, env, dockerfile-variable-substitution, arg-default-value, parameter-expansion]
level: practitioner
description: "Use Dockerfile ${VAR:-default}, ${VAR:+alt} and the newer prefix/suffix/replace forms, know which instructions expand them and how to escape $."
sources: ["https://docs.docker.com/reference/dockerfile/#environment-replacement", "https://docs.docker.com/reference/dockerfile/#arg", "https://docs.docker.com/reference/build-checks/undefined-var/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dockerfile variable substitution

The Dockerfile parser (not the shell) expands `$VAR` / `${VAR}` in a fixed set of
instructions using ARG and ENV values in scope.

## Forms
| Form | Result |
|---|---|
| `${VAR}` / `$VAR` | value, or empty string if unset |
| `${VAR:-word}` | `word` if VAR unset **or empty** |
| `${VAR:+word}` | `word` if VAR set and non-empty, else empty |
| `${VAR#pattern}` / `${VAR##pattern}` | strip shortest/longest prefix |
| `${VAR%pattern}` / `${VAR%%pattern}` | strip suffix |
| `${VAR/pat/repl}` / `${VAR//pat/repl}` | replace first / all |

`word` can be any string, including other variables: `${TAG:-${VERSION}-dev}`.
In the reference the `#`, `##`, `%`, `%%`, `/` and `//` forms are documented as supported in a
pre-release version of the Dockerfile syntax (`# syntax=docker/dockerfile-upstream:master`), so
treat them as unstable and avoid them in builds that must parse the same everywhere. `pattern`
is a glob where `?` matches one character and `*` any number; escape a literal one with a backslash.

```dockerfile
# syntax=docker/dockerfile:1
ARG PY_VERSION=3.12
FROM python:${PY_VERSION}-slim
ARG APP_ENV
ENV APP_ENV=${APP_ENV:-production}
ARG MODE
RUN : "${MODE:?set --build-arg MODE}"     # RUN is shell-expanded: POSIX :? works here
```

## Where it applies
Parser expansion works in: `ADD COPY ENV EXPOSE FROM LABEL STOPSIGNAL USER VOLUME WORKDIR` and
`ONBUILD` (when combined with one of those). In `RUN`, `CMD` and `ENTRYPOINT` the
**command shell** substitutes variables, not the builder, and exec form does not invoke a shell,
so `CMD ["echo", "$HOME"]` prints `$HOME` literally.

## Escaping
- `\$VAR` or `\${VAR}` in a parser-expanded instruction yields the literal `$VAR` or `${VAR}`,
  for example `COPY \$FOO /quux` stays `COPY $FOO /quux`.
- In `RUN`, quote for the shell as usual: `RUN echo '$NOT_EXPANDED'`.

## Gotchas
- `ENV A=1 B=$A` on one line: `B` is computed from the value of A **before** this instruction
  (the same value is used for the whole instruction). Split into two ENV lines.
- An undeclared variable silently expands to empty, so `FROM node:${NODE_VERION}` becomes `node:`.
  `docker build --check` reports undefined variables with the `UndefinedVar` and
  `UndefinedArgInFrom` rules.
- An `ARG` declared before the first `FROM` is outside any stage; to use its default inside a stage,
  redeclare it there with `ARG NAME` and no value.

## Verify
`docker build --check .` shows no `UndefinedVar` or `UndefinedArgInFrom` warnings.

## Checked

Checked 2026-10-23 against the Dockerfile reference ("Environment replacement", ARG scope; moby/buildkit docs, main) and the BuildKit rule page UndefinedVar.
Confirmed: the `:-` and `:+` forms; the prefix, suffix and replace forms are listed as pre-release (`dockerfile-upstream:master`); the instruction list that supports replacement; shell-versus-parser expansion for RUN, CMD and ENTRYPOINT; `\$` escaping; same-instruction ENV ordering; redeclaring a pre-FROM ARG; `docker build --check`. Removed the claim that the prefix/suffix forms work on a stable frontend, the ARG-default expansion claim and the backtick escape example.

Method: documentation only; no commands were run.
