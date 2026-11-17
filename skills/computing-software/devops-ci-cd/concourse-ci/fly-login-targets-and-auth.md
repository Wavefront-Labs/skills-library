---
id: computing-software.devops-ci-cd.concourse-ci.fly-login-targets-and-auth
name: fly-login-targets-and-auth
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [fly, login, targets, flyrc, ca-cert, client-cert, sync, userinfo, logout]
level: intro
status: docs-checked
description: "Set up the fly CLI: login to a team, save a target alias in ~/.flyrc, custom CA and client certs, one-day tokens, status, userinfo, edit and delete targets, sync, completion."
sources:
  - https://concourse-ci.org/docs/fly/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`fly login` authenticates to a Concourse and saves the endpoint under an alias. The alias and token are stored in `~/.flyrc` (not meant to be edited by hand), and the token expires after one day.

```shell
fly --target example login --team-name my-team --concourse-url https://ci.example.com
```

The team defaults to `main`. Login lists the team's auth methods: basic auth prompts for username and password, OAuth prints a link and then a token to paste, and if none is configured a token is acquired without prompting. For a certificate not signed by a trusted CA use `--ca-cert ./ca.crt` (its contents are saved to `.flyrc`). For a proxy needing client certificates use `--client-cert` and `--client-key`; their paths are stored and attached to every request.

The `-t` flag is intentionally stateless and must be on every command, which reduces the chance of running against the wrong environment.

Other commands: `fly targets` (name, URL, token expiry), `fly -t example status` (has the token expired), `fly -t example userinfo` (user, teams and roles), `fly -t example logout` or `fly logout -a` for all (the two are mutually exclusive), `fly -t example edit-target` with optional `--target-name`, `--concourse-url`, `--team-name`, and `fly -t example delete-target` or `-a`. `fly -t example sync` updates your local fly to match the server, and fly warns when out of sync. `source <(fly completion --shell bash)` enables autocompletion and needs no target.

## Checked

2026-11-04. Commands and flags confirmed on The fly CLI page.

Method: documentation only; no commands were run.
