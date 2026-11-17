---
id: computing-software.systems-network-administration.audiobookshelf.podcast-folder-structure-and-tags
name: podcast-folder-structure-and-tags
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [podcasts, directory-structure, id3, episodes, genres]
level: practitioner
status: docs-checked
description: "Structure Audiobookshelf podcast folders flat and map ID3 tags to podcast and episode fields."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/podcast-library/1.podcast-directory-structure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Podcasts are folders in a **flat** structure (no season folders). Each audio file is one episode, and the one cover image goes in the same folder:

```
Lex Fridman Podcast/
  #219 - Donald Knuth.mp3
  #252 - Elon Musk.mp3
  Cover.jpg
Self-Hosted/
  #69 - Get Off My Lawn.mp3
```

Podcast metadata comes from the first audio file found.

| Tag | Field |
| --- | --- |
| album / series | podcast title |
| album-artist / artist | author |
| genre | genres (split by `/`, `//` or `;`) |
| language | language |
| itunes-id | itunesId |
| podcast-type | podcastType |
| comment / description | episode description |
| subtitle | episode subtitle |
| date | pubDate, publishedAt |
| disc | season |
| track / series-part | episode |
| title | episode title |
| episode-type | episodeType (`full`, `trailer`, `bonus`) |

Only episode files downloaded to the server are shown.

## Checked

Method: docs-checked 2026-11-09 against the Podcast Library Structure page of the Audiobookshelf docs repo, read in full from raw markdown.
