---
id: computing-software.software-engineering.wails.dogs-api-tutorial
name: dogs-api-tutorial
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, tutorial, svelte, http]
level: practitioner
status: docs-checked
description: "Follow the Wails Dogs API tutorial: a Svelte app whose Go methods fetch dog images from dog.ceo and display them with generated bindings."
sources: [https://wails.io/docs/tutorials/dogsapi]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dogs API tutorial (Svelte)

Goal: build a small app where Go does the HTTP work and Svelte displays it.

## Method

1. `wails init -n dogs-api -t svelte` (optionally `-ide vscode` or `-ide goland`), then `cd dogs-api`.
2. Remove the template's unused code: the `Greet` method in `app.go`, all lines of `frontend/src/App.svelte`, and `frontend/src/assets/images/logo-universal.png`.
3. In `app.go` add structs matching the dog.ceo JSON: `RandomImage{Message string; Status string}`, `AllBreeds{Message map[string]map[string][]string; Status string}`, `ImagesByBreed{Message []string; Status string}`.
4. Add methods on `App`: `GetRandomImageUrl() string` (GET https://dog.ceo/api/breeds/image/random), `GetBreedList() []string` (GET .../breeds/list/all, collect map keys, `sort.Strings`), `GetImageUrlsByBreed(breed string) []string` (GET .../breed/BREED/images). Each reads the body, `json.Unmarshal`s into the struct and returns the Message data.
5. Update imports in app.go: context, fmt, encoding/json, io/ioutil, log, net/http, sort.
6. In `App.svelte`, import the three functions from `../wailsjs/go/main/App.js`, call them with `.then(...)` to fill `randomImageUrl`, `breeds` and `photos`, and render a button for a random dog, a `<select>` bound to the breed list, and `<img>` tags.
7. Run `wails dev` to generate bindings and test; run `wails build` for a single production binary.

## Gotchas
- The tutorial code calls `log.Fatal` on request errors, which would end the app; treat it as demo code.
- Tutorial credit: @tatadan's Wails examples repository.

## Related skills
- computing-software.software-engineering.wails.call-go-from-frontend
- computing-software.software-engineering.wails.dev-mode

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Dogs API" tutorial.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
