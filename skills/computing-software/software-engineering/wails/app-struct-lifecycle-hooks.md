---
id: computing-software.software-engineering.wails.app-struct-lifecycle-hooks
name: app-struct-lifecycle-hooks
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, lifecycle, app-structure, startup, shutdown, context]
level: practitioner
status: docs-checked
description: "Structure a Wails v2 app with main.go and app.go, saving the startup context and wiring OnStartup and OnShutdown hooks."
sources: [https://wails.io/docs/guides/application-development, https://wails.io/docs/howdoesitwork]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set up the standard Wails v2 app layout so lifecycle hooks and the runtime context are available.

## Method
The default templates split the project: `main.go` configures and runs the app, `app.go` holds application logic. `app.go` defines a struct with two hook methods:

```go
type App struct {
	ctx context.Context
}

func NewApp() *App {
	return &App{}
}

func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
}

func (a *App) shutdown(ctx context.Context) {
}
```

- `startup` is called once Wails has allocated the resources it needs. Create resources and set up event listeners here. Save the `context.Context` in a struct field: it is required for calling the runtime. If `startup` returns an error the application terminates; in dev mode the error is printed to the console.
- `shutdown` is called at the very end of shutdown; free memory and do final tasks here.

`main.go` is normally one `wails.Run()` call. Create `app := NewApp()` first, then pass the hooks:

```go
err := wails.Run(&options.App{
	Title:      "My App",
	Width:      800,
	Height:     600,
	OnStartup:  app.startup,
	OnShutdown: app.shutdown,
})
if err != nil {
	log.Fatal(err)
}
```

## Several structs needing the context
Pass the context from `OnStartup` into each struct (the page uses a `SetContext` method on each):

```go
OnStartup: func(ctx context.Context) {
	app.SetContext(ctx)
	otherStruct.SetContext(ctx)
},
```

## Other setup notes from the page
- Menu: pass a Menu struct as `Menu: app.menu()` in `options.App`; a method on `App` returning the menu is the common pattern.
- The templates generate `go.mod` with module name "changeme"; rename it after generating the project.

Related: `computing-software.software-engineering.wails.bind-go-methods-and-enums`.

## Gaps
The lifecycle callbacks, including `OnDomReady` and `OnBeforeClose`, are described on the "How does it work" page, not here.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Application Development" guide; "How does it work" (howdoesitwork).

Corrected or removed: Pointed the Gaps note at the page that actually describes OnDomReady and OnBeforeClose, and added it to sources.

Method: documentation only; no commands were run.
