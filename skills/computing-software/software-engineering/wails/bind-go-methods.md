---
id: computing-software.software-engineering.wails.bind-go-methods
name: bind-go-methods
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, binding, enums]
level: practitioner
status: docs-checked
description: "Expose Go struct methods to the frontend through the Bind option, including multiple structs and enum binding with EnumBind."
sources: [https://wails.io/docs/howdoesitwork]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binding Go methods and enums

Goal: make Go code callable from JavaScript.

## Method

1. Define a struct with exported (uppercase) methods, for example `func (a *App) Greet(name string) string`.
2. Create an instance and add it to `Bind` in `options.App`. Wails requires an instance of the struct, not the type.

```go
app := &App{}
wails.Run(&options.App{
	// ...
	Bind: []interface{}{
		app,
		&mystruct1{},
		&mystruct2{},
	},
})
```

You can bind as many structs as you like. Think of them as controllers in a web app. At startup Wails inspects the instances, finds public methods and generates JavaScript versions.

Enums: build a slice of structs holding `Value` and `TSName`, then pass it in `EnumBind`:

```go
type Weekday string
const (
	Sunday Weekday = "Sunday"
	Monday Weekday = "Monday"
)

var AllWeekdays = []struct {
	Value  Weekday
	TSName string
}{
	{Sunday, "SUNDAY"},
	{Monday, "MONDAY"},
}

// in options.App:
EnumBind: []interface{}{ AllWeekdays },
```

`wails dev` or `wails generate module` then generates JavaScript bindings, TypeScript declarations for bound methods, and TypeScript definitions for structs used as inputs or outputs.

## Related skills
- computing-software.software-engineering.wails.call-go-from-frontend

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "How does it work" (howdoesitwork).

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
