---
id: computing-software.web-development.vapor.vapor-custom-console-commands
name: vapor-custom-console-commands
category: computing-software
field: web-development
product: vapor
tags: [vapor,vapor-commands,asynccommand,commandsignature,console,cli,swift]
level: practitioner
status: docs-checked
description: "Write a custom Vapor command with AsyncCommand, Signature, @Argument and @Option, register it in app.asyncCommands, and run it with swift run."
sources:
  - https://docs.vapor.codes/advanced/commands/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add your own CLI command to a Vapor app (the same API powers `serve`, `routes`, `migrate`).

Discover commands: `swift run App --help`, and `swift run App serve --help` for one command. In Xcode, edit the `App` scheme, Arguments tab, and add the command name (e.g. `serve`) to "Arguments Passed On Launch".

**Define and register.** Conform to `AsyncCommand`, implement `run`, declare a `Signature` and `help` text:

```swift
struct HelloCommand: AsyncCommand {
    struct Signature: CommandSignature { }

    var help: String { "Says hello" }

    func run(using context: CommandContext, signature: Signature) async throws {
        context.console.print("Hello, world!")
    }
}

app.asyncCommands.use(HelloCommand(), as: "hello")
```

Run: `swift run App hello`. An empty signature means no arguments or options. `context.console` offers prompting and formatting, e.g. `context.console.ask("What is your \("name", color: .blue)?")`.

**Arguments and options** (from the docs' cowsay example):

```swift
struct Signature: CommandSignature {
    @Argument(name: "message")
    var message: String

    @Option(name: "eyes", short: "e")
    var eyes: String?
}
```

Register with `app.asyncCommands.use(Cowsay(), as: "cowsay")` and call `swift run App cowsay sup --eyes ^^ --tongue "U "` (the example also declares a `tongue` option with short `t`). Optional values are read from `signature.eyes` etc., with defaults applied in code (`signature.eyes ?? "oo"`).

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) advanced/commands, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
