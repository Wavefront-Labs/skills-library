---
id: computing-software.devops-ci-cd.jenkins.jenkins-cli-and-ssh-interface
name: jenkins-cli-and-ssh-interface
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jenkins-cli, jenkins-ssh-cli, cli-jar, websocket-cli, api-token, ssh-server, build-command, automation, http-mode]
level: practitioner
status: docs-checked
description: "Automate Jenkins with jenkins-cli.jar (WebSocket, HTTP or SSH mode) and the built-in SSH CLI: API token or SSH key auth, build and console commands, and the 2024 CLI advisory."
sources: ["https://www.jenkins.io/doc/book/managing/cli/", "https://www.jenkins.io/security/advisory/2024-01-24/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jenkins-cli and the SSH interface

## Client jar
```bash
curl -sO "$JENKINS_URL/jnlpJars/jenkins-cli.jar"
echo "alice:$API_TOKEN" > ~/.jenkins-cli-creds && chmod 600 ~/.jenkins-cli-creds
alias jcli='java -jar jenkins-cli.jar -s "$JENKINS_URL" -auth @$HOME/.jenkins-cli-creds'
jcli who-am-i
jcli help                       # commands available on THIS controller (plugins add more)
```
Modes, chosen by global option: `-webSocket`, `-http` and `-ssh`. Since Jenkins 2.391 the default is `-webSocket`; pass
`-http` explicitly for HTTP mode (WebSocket needs server and client 2.217 or newer). `-auth` takes `username:apitoken`
or `@file`; get the token from `/me/configure`. Alternatively set `JENKINS_USER_ID` and `JENKINS_API_TOKEN`; `-auth` takes
precedence. SSH mode: `-ssh -user alice`.

## SSH CLI (no jar)
The SSH service is disabled on a new installation. Set a fixed port (or ask for a random one) on the Security page, add your
public key under the user's Security settings (Manage Jenkins -> Users), then:
```bash
ssh -l alice -p 2222 jenkins.example.com help
ssh -l alice -p 2222 jenkins.example.com build my-job -s -v
```
A random port shows in the `X-SSH-Endpoint` header of `$JENKINS_URL/login`. Behind a reverse proxy the client's default SSH
host is wrong; set the system property `org.jenkinsci.main.modules.sshd.SSHD.hostName` on the controller.

## Useful commands
| Command | Use |
|---|---|
| `build JOB` with `-s`, `-f`, `-v`, `-p` | trigger; `-s` waits and changes the exit code with the result, `-f` follows progress, `-v` prints the console (use with `-s`) |
| `console JOB [BUILD] [-f] [-n N]` | build log; last completed build if no number; `-f` stays on a running build |
| `who-am-i` | your credentials and permissions; useful when commands are missing |
| `list-jobs` | built-in, one of many; run `help` for the list |

## Security
- The CLI runs with the authenticated user's permissions.
- CVE-2024-23897: the args4j parser expanded `@` plus a file path into the file's contents. Fixed in Jenkins 2.442, LTS 2.426.3
  and LTS 2.440.1; disabling CLI access prevents exploitation for unpatched controllers. The same advisory fixed missing origin
  validation on the CLI WebSocket endpoint.
- The CLI document assumes Jenkins 2.54 or newer; older CLI clients are considered insecure.

## Checked
2026-11-01. Confirmed on the Jenkins "Jenkins CLI" page and security advisory 2024-01-24: modes and the 2.391 default, `-auth`
forms, environment variables, SSH setup, `X-SSH-Endpoint`, `build`/`console`/`who-am-i`/`help` options, CVE fix versions.
Corrected: the default mode is WebSocket, not HTTP. Removed unconfirmed commands (plugin, node, Groovy, JCasC, linter, job XML),
the `jenkins.CLI.disabled` property and the build-exit-code script example.
Method: documentation only; no commands were run.
