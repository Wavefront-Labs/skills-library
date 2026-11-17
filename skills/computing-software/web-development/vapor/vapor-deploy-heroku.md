---
id: computing-software.web-development.vapor.vapor-deploy-heroku
name: vapor-deploy-heroku
category: computing-software
field: web-development
product: vapor
tags: [vapor, vapor-heroku, heroku, buildpack, procfile, postgres, deployment, migrations]
level: practitioner
status: docs-checked
description: "Deploy a Vapor app to Heroku with the vapor buildpack, .swift-version, Procfile, git push, scaling, Heroku Postgres TLS config and remote migrations."
sources:
  - https://docs.vapor.codes/deploy/heroku/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get a Vapor app running on Heroku with a Postgres database.

## Prepare
1. Heroku account and CLI (`brew tap heroku/brew && brew install heroku`), then `heroku login` and `heroku auth:whoami`.
2. Create the app in dashboard.heroku.com (region, name).
3. Put the project in Git, deploying from one branch (main or master). Commit everything first; `git status --porcelain` printing output means uncommitted changes. Connect: `heroku git:remote -a your-apps-name-here`.

## Build files
```bash
heroku buildpacks:set vapor/vapor
echo "5.8.1" > .swift-version     # use the Swift version your project needs
```

The buildpack reads `.swift-version`. The Procfile tells Heroku how to run the app:

```
web: App serve --env production --hostname 0.0.0.0 --port $PORT
```

Commit these files before pushing, or Heroku will not find them.

## Deploy and scale
```bash
git push heroku main        # build may take a while
heroku ps:scale web=1       # at least one server; needs payment configured on Heroku
```

Later updates: get changes into main and push again.

## Postgres
Add the Heroku Postgres add-on (dashboard Add-ons section; the Essential 0 plan is the one the page picks). `heroku config` shows `DATABASE_URL`. Never hard-code its value because Heroku rotates it; read it at runtime. Heroku Postgres requires encrypted connections with Heroku-internal certificates, so use an unverified TLS connection:

```swift
if let databaseURL = Environment.get("DATABASE_URL") {
    var tlsConfig: TLSConfiguration = .makeClientConfiguration()
    tlsConfig.certificateVerification = .none
    let nioSSLContext = try NIOSSLContext(configuration: tlsConfig)

    var postgresConfig = try SQLPostgresConfiguration(url: databaseURL)
    postgresConfig.coreConfiguration.tls = .require(nioSSLContext)

    app.databases.use(.postgres(configuration: postgresConfig), as: .psql)
} else {
    // ...
}
```

Commit and push this change.

## Migrations
```bash
heroku run App -- migrate --env production
heroku run App -- migrate --revert --all --yes --env production
```

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) deploy/heroku, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
