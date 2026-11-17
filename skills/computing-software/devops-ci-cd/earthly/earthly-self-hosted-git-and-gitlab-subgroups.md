---
id: computing-software.devops-ci-cd.earthly.earthly-self-hosted-git-and-gitlab-subgroups
name: earthly-self-hosted-git-and-gitlab-subgroups
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, git, self-hosted, gitlab, subgroups, pattern, substitute, port, prefix]
level: advanced
status: docs-checked
description: "Point earthly at self-hosted Git servers with port and prefix, or at GitLab subgroups with pattern and substitute regular expressions in the git config section."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/auth.md
  - https://github.com/earthly/earthly/blob/main/docs/earthly-config/earthly-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Self-hosted Git and GitLab subgroups

Goal: make remote references like `ghe.internal.mycompany.com/user/repo+some-target` resolve to the right clone URL.

Tested providers are github.com, gitlab.com and bitbucket.org. With no host config, earthly tries a clone over SSH on port 22, then HTTPS, then HTTP.

## port and prefix (preferred)
```yaml
git:
    ghe.internal.mycompany.com:
        auth: ssh
        user: git
        port: 2222
```
This clones `ssh://git@ghe.internal.mycompany.com:2222/user/repo.git`. The ssh scheme path is absolute on the server; if repos live elsewhere (for example `/var/git/`), set `prefix`.

## pattern and substitute
`pattern` is an RE2 regular expression matched against the reference, default `<site>/([^/]+)/([^/]+)`. `substitute` builds the cloned URL, replacing `$1`, `$2`, ... with matched groups; without it a URL is created from the SSH auth mode.
```yaml
git:
    ghe.internal.mycompany.com:
        pattern: 'ghe.internal.mycompany.com/([^/]+)/([^/]+)'
        substitute: 'ssh://git@ghe.internal.mycompany.com:22/$1/$2.git'
        auth: ssh
```

## GitLab subgroups
Earthly assumes two levels (`<org>/<path>.git`), so sub groups need a pattern:
```yaml
git:
    gitlab.com:
        pattern: 'gitlab.com/(example-org)/([^/]+)/([^/]+)'
        substitute: 'git@gitlab.com:$1/$2/$3.git'
        auth: ssh
```
With a mix of 2 and 3 level groupings, configure each separately:
```yaml
git:
    gitlab.com/example-org/projecta:
        pattern: 'gitlab.com/(example-org)/(project-a)/([^/]+)'
        substitute: 'git@gitlab.com:$1/$2/$3.git'
        auth: ssh
    gitlab.com example-org catch-all:
        pattern: 'gitlab.com/(example-org)/([^/]+)'
        substitute: 'git@gitlab.com:$1/$2.git'
        auth: ssh
```

## Gotchas
- The parentheses in the pattern are required; they assign matched values to `$1`, `$2`, ...
- When a `pattern` is used, the config key is only used by log messages, not for matching.
- Patterns are evaluated top to bottom, so list subgroup-specific entries first.

## Checked

2026-11-07. Read the self-hosted Git and GitLab Subgroups sections of docs/guides/auth.md (about lines 82-155) and the git configuration reference of earthly-config.md (about lines 228-302), not those pages in full. Fallback order, port, prefix, pattern default, substitute, subgroup examples and gotchas match. Nothing removed.
Method: documentation only; no commands were run.
