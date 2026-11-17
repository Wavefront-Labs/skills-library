---
id: computing-software.web-development.jekyll.git-post-receive-deploy
name: git-post-receive-deploy
category: computing-software
field: web-development
product: jekyll
tags: [post-receive-hook, git-deploy, bare-repo, server-side-build, ci-providers]
level: advanced
status: docs-checked
description: "Deploy Jekyll by git push using a bare repo and a post-receive hook that clones, bundles and builds into the web root; plus the listed CI providers."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/deployment/automated.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CI is the easiest automated flow: a script runs on each commit to build, test and deploy. Guides exist for GitHub Actions, Travis CI, CircleCI, Buddy and Razorops CI/CD.

Alternative: a Git post-receive hook on your server. Create a user whose `authorized_keys` holds the deployers' public keys, then:

```sh
laptop$ ssh deployer@example.com
server$ mkdir myrepo.git
server$ cd myrepo.git
server$ git --bare init
server$ cp hooks/post-receive.sample hooks/post-receive
server$ mkdir /var/www/myrepo
```

With Jekyll installed on the server, put this in `hooks/post-receive`:

```bash
#!/bin/bash -l
export GEM_HOME=$HOME/gems
export PATH=$GEM_HOME/bin:$PATH

TMP_GIT_CLONE=$HOME/tmp/myrepo
GEMFILE=$TMP_GIT_CLONE/Gemfile
PUBLIC_WWW=/var/www/myrepo

git clone $GIT_DIR $TMP_GIT_CLONE
BUNDLE_GEMFILE=$GEMFILE bundle install
BUNDLE_GEMFILE=$GEMFILE bundle exec jekyll build -s $TMP_GIT_CLONE -d $PUBLIC_WWW
rm -Rf $TMP_GIT_CLONE
exit
```

On each deploying laptop:

```sh
laptops$ git remote add deploy deployer@example.com:~/myrepo.git
```

Point nginx or Apache at `/var/www/myrepo`, then deploy with `git push deploy master`.

## Checked

2026-11-04. Confirmed against the Jekyll Automated Deployment page: CI provider list, bare repo steps, the post-receive script, deploy remote and git push. Nothing removed.

Method: documentation only; no commands were run.
