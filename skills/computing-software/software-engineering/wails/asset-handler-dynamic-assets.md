---
id: computing-software.software-engineering.wails.asset-handler-dynamic-assets
name: asset-handler-dynamic-assets
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, assets, assetserver, http-handler, dynamic-assets, vite]
level: practitioner
status: docs-checked
description: "Serve files on the fly in a Wails v2 app with an AssetServer Handler that catches missing GET requests and all non-GET requests."
sources: [https://wails.io/docs/guides/dynamic-assets, https://wails.io/docs/guides/application-development]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: load or generate frontend assets dynamically through the asset server's `http.Handler`.

## How it routes
- GET requests are handled by the bundled `Assets` FS first; if the file is not found, the request is forwarded to the handler.
- Any non-GET request goes straight to the handler (so POST/PUT can be processed).
- Setting `Assets` to `nil` means only the handler is used.

## Example: load files from disk
```go
type FileLoader struct {
	http.Handler
}

func NewFileLoader() *FileLoader {
	return &FileLoader{}
}

func (h *FileLoader) ServeHTTP(res http.ResponseWriter, req *http.Request) {
	var err error
	requestedFilename := strings.TrimPrefix(req.URL.Path, "/")
	println("Requesting file:", requestedFilename)
	fileData, err := os.ReadFile(requestedFilename)
	if err != nil {
		res.WriteHeader(http.StatusBadRequest)
		res.Write([]byte(fmt.Sprintf("Could not load file %s", requestedFilename)))
	}

	res.Write(fileData)
}
```

Register it:

```go
AssetServer: &assetserver.Options{
	Assets:  assets,
	Handler: NewFileLoader(),
},
```

In `wails dev` the console shows the external handler trying and failing on `favicon.ico`, then falling back to the handler. From the devtools console, `await fetch('does-not-exist.txt')` shows the handler's error response; the page also shows the result of requesting `go.mod` (as an image). The handler can also feed images: `<img src="build/appicon.png">`.

## Gotchas stated by the page
- Does not work with vite v5.0.0+ and Wails v2 (changes planned in v3); stay on vite v4 if you need it (issue 3240).
- Serving the filesystem like this is a security risk; manage access properly (the example performs no path restriction).
- The example writes the error body but continues to write `fileData`; add a `return` in real code (observation, not stated by the page).

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Dynamic Assets" guide; "Application Development" guide.

Corrected or removed: Removed the claim that requesting go.mod "returns the file"; the page shows that result only as an image.

Method: documentation only; no commands were run.
