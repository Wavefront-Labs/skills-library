---
id: computing-software.systems-network-administration.jellyfin.provider-ids-in-names
name: provider-ids-in-names
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, metadata-provider, tmdbid, tvdbid, imdbid, identifiers, naming]
level: practitioner
status: docs-checked
description: "Force correct matches by adding tmdbid, tvdbid or imdbid identifiers to Jellyfin folder and file names, and find each id."
sources: ["https://jellyfin.org/docs/general/server/metadata/identifiers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Metadata provider identifiers in names

To improve identification, put a provider id in the movie or show folder or file name. Several ids can be given, and the brackets may be `[]`, `()` or `{}`.

```txt
Movies
├── Best_Movie_Ever (1994) [tmdbid-680] [imdbid-1234]
├── Best_Movie_Ever_2 (1994) {tmdb-680}
└── Movie (2021) [imdbid-tt12801262]
Shows
└── Series Name (2018) [tvdbid-79168]
```

For movies with multiple versions the id must be in both the parent folder and the file.

**Supported providers and where to find the id**

| Provider | Tag | Alias | Where |
| --- | --- | --- | --- |
| The Movie DB | `[tmdbid-569094]` | `[tmdb-569094]` | the number in the title's URL, such as `/movie/569094-spider-man-across-the-spider-verse` |
| The TV Database | `[tvdbid-266189]` | `[tvdb-266189]` | shown on the title's main page |
| OMDb (English only) | `[imdbid-tt9362722]` | `[imdb-tt9362722]` | the IMDb id in the IMDb URL, `/title/tt9362722/` |

OMDb uses IMDb ids as identifiers.

If a title stays wrong, follow `computing-software.systems-network-administration.jellyfin.fix-misidentified-media`.

## Checked

2026-11-03. Confirmed against the Jellyfin Metadata Provider Identifiers page: bracket styles, multiple ids, multiple-versions rule, TMDB/TVDB/OMDb tags and aliases, English-only OMDb. Removed: unsupported claim about season and episode ids and the invented self-check.

Method: documentation only; no commands were run.
