---
id: computing-software.devops-ci-cd.dagger.third-party-packages
name: third-party-packages
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, packages, go-modules, python, typescript, composer, maven, goprivate, dependencies]
level: practitioner
status: docs-checked
description: "Add language-native third-party packages (Go, Python, TypeScript, PHP, Java) to a Dagger module, including private Go modules via goprivate."
sources: [https://docs.dagger.io/0.21/extending/packages, https://docs.dagger.io/0.21/extending/api-playground]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Third-party packages in Dagger modules

Goal: use your language's package ecosystem inside a module. Dagger Functions are ordinary code, so use the language's package manager. Dagger 0.21 docs.

## Go
`go get github.com/spf13/cobra`.
Private Go modules: add a `config.goprivate` key to the module's `dagger.json`:
```json
{
  "sdk": {
    "source": "go",
    "config": { "goprivate": "github.com/user/repository" }
  }
}
```
Multiple URLs are comma-separated; the repository name is optional (`github.com/username` covers every private module under that prefix). It also needs a `.gitconfig` entry so SSH is used instead of HTTPS: `git config --global url."git@github.com:".insteadOf "https://github.com/"`.

## Python
Add to `pyproject.toml` with your manager: `uv add requests` or `poetry add requests`. With plain pip or `uv pip`, add `"requirements>=2.32.3"` style entries under `[project] dependencies` manually, then install into the existing virtual environment: `uv pip install -e ./sdk -e .` (the venv must exist, no need to activate) or `python -m pip install -e ./sdk -e .`. Pinning limits: Dagger installs directly from a `uv.lock` file or a pip-tools compatible `requirements.lock` (note the `.lock` extension, not `.txt`).

## TypeScript
Use the runtime's manager: `npm install pm2` (Node.js), `bun install pm2` (Bun), `deno add jsr:@celusion/simple-validation` (Deno). Version pinning and local dependencies work as in any Node.js project.

## PHP
`composer require phpunit/phpunit`. The page says Dagger modules installed as Composer packages are not registered with Dagger, are not the intended use of a module and may lead to unexpected behaviour; use Composer for ordinary packages and `dagger install` for Dagger modules.

## Java
Add a dependency to `pom.xml`, e.g. groupId `org.slf4j`, artifactId `slf4j-simple`, scope `runtime`, version `2.0.16`.

## Aside: GraphQL playground
The in-browser API Playground has been decommissioned; use `dagger query` to send raw GraphQL. To explore locally from a module directory: `env DAGGER_SESSION_TOKEN=test dagger listen --allow-cors` (serves on `http://127.0.0.1:8080/query`), connect e.g. Altair, with Basic auth using the token value as username and password; the page's example header for `test` is `Authorization: Basic dGVzdDo=`, which decodes to `test:` (empty password), so check what your client sends.

Related: module-dependencies-install-update.

## Checked

2026-11-07

Read extending/modules/packages.mdx (live slug /extending/packages) and extending/modules/playground.mdx (live slug /extending/api-playground) in full; both cited URLs match the live slugs and neither embeds snippet files. Confirmed go get and the config.goprivate JSON, multiple URLs and the optional repository name, the .gitconfig insteadOf command, the Python uv/poetry/uv pip/pip instructions, the pip-tools requirements.lock note, the TypeScript Node/Bun/Deno commands, composer require and the Composer caveat, the Maven dependency example, the decommissioned playground, dagger query, and the dagger listen steps. Corrected the PHP wording to what the page says, and flagged that the page's example Basic header decodes to 'test:' although the text says username and password. The linked modules.mdx language-native packaging section was covered by module-layout-and-runtime.

Method: documentation only; no commands were run.
