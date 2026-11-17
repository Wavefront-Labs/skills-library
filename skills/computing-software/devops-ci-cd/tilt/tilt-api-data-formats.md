---
id: computing-software.devops-ci-cd.tilt.tilt-api-data-formats
name: tilt-api-data-formats
category: computing-software
field: devops-ci-cd
product: tilt
tags: [api-data-formats]
level: practitioner
status: docs-checked
description: "Tiltfile JSON and YAML helpers: decode, encode and read functions for single documents and YAML streams."
sources:
  - "https://docs.tilt.dev/api.html#api.decode_yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON and YAML helpers

Goal: convert between text and Starlark objects in a Tiltfile.

## JSON

- `decode_json(json)`: deserializes a string or Blob of JSON into a Starlark object.
- `encode_json(obj)`: serializes an object to JSON, returning a Blob. Only supports maps with string keys, lists, strings, ints and bools.
- `read_json(path, default=None)`: reads the file and deserializes it as JSON.

## YAML

- `decode_yaml(yaml)`: deserializes one YAML document (string or Blob).
- `decode_yaml_stream(yaml)`: deserializes any number of YAML documents separated by `"\n---\n"` into a list of objects.
- `encode_yaml(obj)`: serializes an object to YAML (Blob). Same type limits as `encode_json`.
- `encode_yaml_stream(objs)`: serializes a list of objects into a YAML stream of documents separated by `"\n---\n"`. Same type limits.
- `read_yaml(path, default=None)`: reads the file and deserializes it into a Starlark object.
- `read_yaml_stream(path, default=None)`: reads a YAML stream from the file into a list of objects.

## Reading files

For all `read_*` functions, `path` is local, either absolute or relative to the Tiltfile location. If the path does not exist and `default` is not None, `default` is returned. In any other case, an error reading `path` is a Tiltfile load error.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/api.html#api.decode_yaml (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
