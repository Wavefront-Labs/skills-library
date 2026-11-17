---
id: computing-software.web-development.vapor.vapor-environments-dotenv
name: vapor-environments-dotenv
category: computing-software
field: web-development
product: vapor
tags: [vapor,environment,dotenv,env-files,configuration,staging,swift]
level: practitioner
status: docs-checked
description: "Choose Vapor environments with --env, read variables via Environment.get, load .env and .env.name files, and define custom environments."
sources:
  - https://docs.vapor.codes/basics/environment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure a Vapor app per environment and from process variables or dotenv files.

Default environment is `development`. Switch on `app.environment` in `configure(_:)` (e.g. `case .production:` vs `default:`).

## Choose environment
```sh
swift run App serve --env production   # or -e prod
```
Built in: production (prod), development (dev), testing (test). Production defaults to `notice` logging; others `info`.

## Process variables
```swift
let foo = Environment.get("FOO")        // String?
let bar = Environment.process.FOO       // String?
```
Set in a terminal with `export FOO=BAR` or in Xcode via the `App` scheme.

## .env files
Vapor looks in the current working directory (set it in the Xcode `App` scheme). `FOO=BAR` in `.env` becomes readable through `Environment.get`. Variables in `.env` do not overwrite ones already in the process environment. Vapor also loads `.env.<environment>` (e.g. `.env.development`), whose values take precedence over `.env`.

Pattern: commit `.env` as a template, ignore specific files with `.env.*` in `.gitignore`, then on a new machine `cp .env .env.development` and edit. Never commit dotenv files with secrets. If files do not load, run with `--log debug`.

## Custom environment
```swift
extension Environment {
    static var staging: Environment { .custom(name: "staging") }
}
```
The environment is usually set in `entrypoint.swift` with `Environment.detect()`, which parses `--env`. Override by building one: `Environment(name: "testing", arguments: ["vapor"])` (at least one argument, the executable name; extra args simulate CLI flags, handy for tests).

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) basics/environment, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
