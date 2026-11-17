---
id: computing-software.software-engineering.git.generating-pull-requests-with-request-pull
name: generating-pull-requests-with-request-pull
category: computing-software
field: software-engineering
product: git
tags: [git, git-request-pull, pull-request-email, distributed-workflows, public-repository, signed-tags]
level: practitioner
status: verified
description: "Ask a maintainer to pull from your public repo with git request-pull: publish a branch or signed tag, generate the summary, and avoid the common wrong-start-point mistakes."
sources: ["https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project", "https://git-scm.com/docs/git-request-pull", "https://www.kernel.org/doc/html/latest/maintainer/pull-requests.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating pull requests with git request-pull

**Goal:** the host-independent pull request: an email telling an integrator exactly
what to fetch, from where, and what it contains (the Linux kernel's maintainer flow).

## Steps
1. Base your work on the maintainer's branch: `git fetch upstream && git switch -c topic upstream/main`.
2. Publish to a repo the maintainer can read:
   `git push myfork topic` (or better, a signed tag: `git tag -s topic-for-6.1 -m "..." && git push myfork topic-for-6.1`).
3. Generate the request:
```bash
git request-pull upstream/main https://git.example.org/me/project.git topic-for-6.1
```
   Arguments: `<start>` (what they already have), `<url>`, `[<end>]` (your ref there).
4. Paste output into an email (subject like `[GIT PULL] parser fixes for 6.1`), adding
   a human summary of *why* above the generated block.

## Output contains
- "The following changes since commit <start>" - the base they must already have.
- "are available in the Git repository at: <url> <ref>" - what to fetch.
- `git shortlog` of your commits and a `--stat` diffstat.
- For a signed tag, the tag message is included; maintainers verify it after `git pull`.

## Gotchas
- **Wrong start point** inflates the request with commits they already have. Use the exact
  upstream ref you based on (`git merge-base upstream/main topic` if unsure).
- **"warn: No match for commit ... found at <url>"** (followed by "Are you sure you pushed 'topic' there?"; reproduced before pushing) means the ref is not pushed (or the
  URL is a push-only SSH URL they cannot read). Push first; give a read URL.
- `<end>` defaults to HEAD; when the ref on the remote has a different name, use the
  `<local>:<remote>` form (e.g. `topic:for-linus`; per git-request-pull docs).
- `-p` appends the full patch; usually unwanted for big series.

## Maintainer side
```bash
git pull https://git.example.org/me/project.git topic-for-6.1   # signed tag: merge message includes tag text
git verify-tag topic-for-6.1   # signed tags only; or check the merge commit with git log --show-signature
```

## Verify
- [ ] Diffstat in the request matches `git diff --stat upstream/main...topic`.
- [ ] URL is readable anonymously (`git ls-remote <url>` from a clean shell).
