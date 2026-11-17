---
id: computing-software.devops-ci-cd.jenkins.git-credentials-and-gitusernamepassword
name: git-credentials-and-gitusernamepassword
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, gitusernamepassword, credentials, withcredentials]
level: practitioner
status: docs-checked
description: "Authenticate git push, tag and submodule operations in Jenkins with the gitUsernamePassword and gitSshPrivateKey bindings instead of embedding tokens in URLs."
sources: ["https://plugins.jenkins.io/git/", "https://github.com/jenkinsci/ssh-agent-plugin", "https://github.com/jenkinsci/github-branch-source-plugin/blob/master/docs/github-app.adoc", "https://github.com/jenkinsci/git-client-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Git credentials and the gitUsernamePassword binding

`checkout scm` uses the job's configured credential, but later `git push`/`git tag` in `sh` do not.
The git plugin provides a `gitUsernamePassword` binding (Snippet Generator: `withCredentials`, Git
Username and Password). It sets `GIT_USERNAME` and `GIT_PASSWORD` for `sh`, `bat` and `powershell` steps in
the block, and also works with the JGit implementations.

```groovy
withCredentials([gitUsernamePassword(credentialsId: 'github-app-or-pat', gitToolName: 'Default')]) {
  sh '''
    git tag -a "v$VERSION" -m "release $VERSION"
    git push origin "v$VERSION"
  '''
}
```
SSH: use the SSH Agent plugin's `sshagent` step from a Pipeline job:
```groovy
sshagent(credentials: ['deploy-key']) {
  sh 'git push git@github.com:org/repo.git HEAD:main'
}
```

## Why not URL tokens
`git push https://user:${TOKEN}@github.com/...` puts the token on the command line (process lists,
possibly logs) and can be stored in the repository configuration. Use the binding instead.

## GitHub App credentials
A "GitHub App" credential (github-branch-source) is preferred over a personal access token for scanning:
its rate limit scales with organisation size (a user token is limited to 5000 requests). Avoid personal
access tokens tied to people where an App fits.

## Gotchas
- Detached HEAD after `checkout scm`: push with explicit refspec `HEAD:refs/heads/main`.
- Pushing from CI re-triggers the job; skip with a commit message filter or by ignoring the bot user.
- Submodule updates do not use credentials by default; the git plugin's "Advanced sub-modules
  behaviours" extension can pass the parent repository's credentials to submodules, which must accept
  the same credentials.
- Host key verification: the Git Client plugin defaults to the "Known hosts file" strategy; configure
  the strategy deliberately rather than disabling verification.

## Verify
- [ ] Tag appears on the remote; no token appears in the log or the workspace configuration.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: `gitUsernamePassword(credentialsId, gitToolName)`, `GIT_USERNAME`/`GIT_PASSWORD`, supported step types and JGit support (git plugin README); `sshagent(credentials: [...])` (ssh-agent plugin README); submodule credential behaviour (git plugin); Git Client default host-key strategy; GitHub App rate-limit statement (github-branch-source docs). Removed the `gitSshPrivateKey` binding, which does not exist in the git plugin source, and the `GIT_ASKPASS` claim.
Method: documentation only; no commands were run.
