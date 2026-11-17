---
id: computing-software.devops-ci-cd.dagger.agent-in-project-github
name: agent-in-project-github
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, agent, llm, workspace, github-actions, pull-request, workflow, prompt-file]
level: practitioner
status: docs-checked
description: "Add a Dagger coding agent to an existing project with a workspace submodule, a develop function and a GitHub Actions workflow that opens PRs from labeled issues."
sources: [https://docs.dagger.io/0.21/getting-started/quickstarts/agent/inproject]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent in an existing Dagger project, deployed on GitHub

Goal: an agent that implements an assignment against your repo, validated by your own `test` function, then run from GitHub issues (Dagger 0.21 docs).

Prerequisites: the Daggerized hello-dagger project from the CI quickstart, an LLM provider configured, a GitHub repo.

## 1. Workspace submodule (limited tools)

```shell
dagger init --sdk=go .dagger/workspace
dagger -m .dagger/workspace functions
dagger install ./.dagger/workspace
```
The module holds a `Source` Directory (constructor argument) and functions `read-file`, `write-file`, `list-files` and `test`. A narrow toolset leaves the agent less room for error.

## 2. The develop function (Go)

Installed dependencies are exposed on `Env` automatically; the workspace gives `WithWorkspaceInput` / `WithWorkspaceOutput`:
```go
environment := dag.Env().
	WithStringInput("assignment", assignment, "the assignment to complete").
	WithWorkspaceInput("workspace", dag.Workspace(source), "the workspace with tools to edit and test code").
	WithWorkspaceOutput("completed", "the workspace with the completed assignment")
promptFile := dag.CurrentModule().Source().File("develop_prompt.md")
work := dag.LLM().WithEnv(environment).WithPromptFile(promptFile)
completed := work.Env().Output("completed").AsWorkspace()
completedDirectory := completed.Source().WithoutDirectory("node_modules")
_, err := m.Test(ctx, completedDirectory)   // re-verify; return error if tests fail
```
Keep the prompt in `.dagger/develop_prompt.md` using `$assignment`, with constraints: analyze the workspace first, no unnecessary changes, always run tests, do not stop until tests pass.

Run: `develop "make the main page blue"`; then `completed=$(develop "...")`, `build --source $completed | as-service | up --ports 8080:80`, `$completed | export .`.

## 3. develop-issue and Actions

`dagger install github.com/kpenfound/dag/github-issue@<commit>` provides `dag.GithubIssue`. `DevelopIssue(githubToken *Secret, issueID, repository, source)` reads the issue body as the assignment, runs `Develop`, then `CreatePullRequest`.

Add repository secrets for the LLM variables (and optionally `DAGGER_CLOUD_TOKEN`), enable "Allow GitHub Actions to create and approve pull requests", and add `.github/workflows/develop.yml`: trigger `issues: labeled`, `if: github.event.label.name == 'develop'`, permissions `contents: write`, `issues: read`, `pull-requests: write`, steps `actions/checkout@v4`, `dagger/dagger-for-github@v8.3.0`, then:
```shell
dagger call develop-issue \
  --github-token env://GH_TOKEN \
  --issue-id ${{ github.event.issue.number }} \
  --repository https://github.com/${{ github.repository }}
```
with env `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` and the LLM key. Labeling an issue "develop" produces a PR.

Related: `computing-software.devops-ci-cd.dagger.llm-agent-environments`.

## Checked

2026-11-07

Read in full from the Dagger docs source (versioned_docs/version-0.21): getting-started/quickstarts/agent/inproject.mdx, plus its embedded snippet files (part2 workspace main.go, part2 agent.go.snippet, part3 agent.go.snippet, part3 develop.yml). Confirmed the workspace functions, constructor Source argument, Env workspace bindings, develop_prompt.md constraints, develop-issue signature, the workflow trigger, permissions, action versions and command. No corrections needed.

Method: documentation only; no commands were run.
