---
id: computing-software.search-and-information-retrieval.typesense.image-search-with-clip
name: image-search-with-clip
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [image-search, clip, image-embedding, typesense]
level: advanced
status: docs-checked
description: "Index images in Typesense with the built-in CLIP model (type image, store false, embed.from) and search by text, by indexed document id, or by an uploaded image."
sources: ["https://typesense.org/docs/30.2/api/image-search.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image search with CLIP

Built-in CLIP support lets you (1) search images with a text description, (2) find images similar to one already indexed, (3) find images similar to a newly uploaded one, embedded at search time.

## Schema

Create a collection with a `name` string field, an `image` field of `"type": "image"` with `"store": false`, and an `embedding` field of type `float[]` whose `embed` has `"from": ["image"]` and `"model_config": {"model_name": "ts/clip-vit-b-p32"}`. An image field holds a base64 string in BMP, JPG or PNG; `store: false` uses it only to build the embedding and then discards the image from the document instead of saving it on disk. To mix text and image in one embedding use `"from": ["name", "image"]`.

## Documents

Import objects like `{"name": "an image with a dog", "image": "<base64 encoded string of the image>"}`.

## Queries (POST /multi_search)

- By text: `{"collection": "images", "q": "animals", "query_by": "embedding"}`. The `q` text is embedded with the same CLIP model and nearest neighbours are returned.
- Similar to a stored image: `"q": "*", "vector_query": "embedding:([], id:123)"`.
- Similar to an uploaded image: `"q": "*", "vector_query": "embedding:([], image:BASE64_REPRESENTATION_OF_IMAGE)"`; results are ordered by closeness.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Image Search page (https://typesense.org/docs/30.2/api/image-search.html). Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
