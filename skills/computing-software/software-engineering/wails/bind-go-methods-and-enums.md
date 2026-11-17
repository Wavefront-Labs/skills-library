---
id: computing-software.software-engineering.wails.bind-go-methods-and-enums
name: bind-go-methods-and-enums
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, binding, enums, typescript, bind]
level: practitioner
status: docs-checked
description: "Expose Go struct methods to the Wails frontend with Bind and generate TypeScript enum models with EnumBind."
sources: [https://wails.io/docs/guides/application-development, https://wails.io/docs/howdoesitwork]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make public Go methods callable from JavaScript and get enum types in the generated models.

## Bind methods
Add exported methods to the struct in `app.go`:

```go
func (a *App) Greet(name string) string {
	return fmt.Sprintf("Hello %s!", name)
}
```

Then list the instance under `Bind` in `main.go`:

```go
err := wails.Run(&options.App{
	Title:      "My App",
	Width:      800,
	Height:     600,
	OnStartup:  app.startup,
	OnShutdown: app.shutdown,
	Bind: []interface{}{
		app,
	},
})
```

All public methods are bound; `startup` and `shutdown` are never bound.

## Multiple structs
To let each bound struct keep the context for runtime calls, the page suggests passing it from `OnStartup` into each struct instance (see `computing-software.software-engineering.wails.app-struct-lifecycle-hooks`).

## Enums
To get frontend models for enum-like types, define the type and constants, plus a slice of structs with the value and the TypeScript name:

```go
type Weekday string

const (
	Sunday Weekday = "Sunday"
	Monday Weekday = "Monday"
	// ...
)

var AllWeekdays = []struct {
	Value  Weekday
	TSName string
}{
	{Sunday, "SUNDAY"},
	{Monday, "MONDAY"},
	// ...
}
```

Register the slice with `EnumBind`:

```go
Bind:     []interface{}{app},
EnumBind: []interface{}{AllWeekdays},
```

The guide says this adds the missing enums to your `model.ts`; the "How does it work" page imports the generated TypeScript models from `wailsjs/go/models`.

## Gaps
Generated binding file layout and Promise behaviour are on the "How does it work" page (see `computing-software.software-engineering.wails.call-go-from-frontend`).

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Application Development" guide; "How does it work" (howdoesitwork).

Corrected or removed: Changed "must receive the context" to the page suggestion (a good pattern, not a requirement); noted the model.ts versus models.ts naming difference between the two pages; added How does it work to sources.

Method: documentation only; no commands were run.
