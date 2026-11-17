---
id: computing-software.web-development.laravel.response-types-and-downloads
name: response-types-and-downloads
category: computing-software
field: web-development
product: laravel
tags: [laravel, responses, json, downloads, file-responses, markdown]
level: practitioner
status: docs-checked
description: "Return view, JSON, JSONP, Markdown, download and inline file responses in Laravel through the response() factory."
sources:
  - https://laravel.com/docs/responses
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`response()` with no arguments returns an implementation of the `Illuminate\Contracts\Routing\ResponseFactory` contract.

View with custom status and headers (use the global `view` helper if you need neither):

```php
return response()->view('hello', $data, 200)->header('Content-Type', $type);
```

JSON sets `Content-Type: application/json` and uses `json_encode`; add `withCallback` for JSONP:

```php
return response()->json(['name' => 'Abigail', 'state' => 'CA']);
return response()->json(['name' => 'Abigail'])->withCallback($request->input('callback'));
```

Markdown sets `Content-Type: text/markdown`; optional status and headers follow:

```php
return response()->markdown("# Hello\n\nWorld");
return response()->markdown('# Not Found', 404, ['X-Custom-Header' => 'Value']);
```

Download forces the browser to save the file; the second argument sets the user-visible filename, third is headers. Symfony HttpFoundation requires an ASCII filename:

```php
return response()->download($pathToFile);
return response()->download($pathToFile, $name, $headers);
```

Show a file such as an image or PDF in the browser (absolute path, optional headers):

```php
return response()->file($pathToFile);
return response()->file($pathToFile, $headers);
```

Turn a string result into a download without writing it to disk:

```php
return response()->streamDownload(function () {
    echo GitHub::api('repo')->contents()->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

## Checked

2026-11-07

Method: read the whole responses page (markdown source of the laravel/docs 13.x branch, commit f7a20c4, which is what laravel.com/docs renders) and compared every claim and example in the skill against it; nothing was run.

Confirmed the ResponseFactory contract, view(), json with withCallback, markdown(), download with its name and header arguments and the ASCII filename warning, file(), and streamDownload. The linked MDN pages were not opened.
