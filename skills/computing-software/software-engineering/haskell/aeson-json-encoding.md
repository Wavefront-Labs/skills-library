---
id: computing-software.software-engineering.haskell.aeson-json-encoding
name: aeson-json-encoding
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, aeson, json, tojson, fromjson, generic-deriving, eitherdecode, value, key, parsejson, withobject, aeson-json-encoding, haskell-parsing]
level: practitioner
status: docs-checked
description: "Encode and decode JSON with aeson: ToJSON/FromJSON via Generic and Options, manual instances with withObject and .:?, KeyMap values, decode vs eitherDecode."
sources: ["https://hackage.haskell.org/package/aeson/docs/Data-Aeson.html", "https://hackage.haskell.org/package/aeson/docs/Data-Aeson-Types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON with aeson

**Goal:** convert between Haskell types and JSON. Package: `aeson`.

```haskell
{-# LANGUAGE DeriveGeneric, DeriveAnyClass, OverloadedStrings, DerivingStrategies #-}
import Data.Aeson
import GHC.Generics

data User = User { userId :: Int, userName :: Text, email :: Maybe Text }
  deriving stock (Show, Generic)

instance ToJSON User where
  toJSON = genericToJSON defaultOptions { fieldLabelModifier = camelTo2 '_' . drop 4, omitNothingFields = True }
instance FromJSON User where
  parseJSON = genericParseJSON defaultOptions { fieldLabelModifier = camelTo2 '_' . drop 4 }

encode (User 1 "a" Nothing)                     -- lazy ByteString
eitherDecode "{\"user_id\":1,\"user_name\":\"a\"}" :: Either String User
decodeFileStrict "cfg.json" :: IO (Maybe Cfg)

-- manual
instance FromJSON Point where
  parseJSON = withObject "Point" $ \o -> Point <$> o .: "x" <*> o .:? "y" .!= 0   -- .:? optional, .!= default
instance ToJSON Point where toJSON (Point x y) = object ["x" .= x, "y" .= y]
```

## Facts
- `Value` is the untyped JSON AST (`Object`, `Array`, `String`, `Number`, `Bool`, `Null`); in aeson 2.x objects are `KeyMap Value` with `Key` keys (use `Data.Aeson.KeyMap`, `Data.Aeson.Key`; `fromString`).
- Prefer `eitherDecode`/`eitherDecodeStrict`: they are like `decode` but return an error message (`Either String a`) when decoding fails.
- Generic encoding of sum types is controlled by `Options` fields such as `sumEncoding`, `allNullaryToStringTag` and `tagSingleConstructors`.
- `genericToEncoding` provides a generic `toEncoding` (direct serialisation).
- JSON numbers are represented as `Scientific`.

## Gotchas
- `omitNothingFields` only affects encoding: with it, `Nothing` fields are omitted instead of encoded as `null`. For parsing, `Maybe` fields are optional regardless; `allowOmittedFields` controls whether other missing fields are filled with `omittedField` values.
- `rejectUnknownFields` makes the parser reject unknown keys; use it for strict APIs.
- Keep wire types separate from domain types; derive with explicit options, not defaults.

## Self-check
- [ ] Round-trip property `decode (encode x) == Just x` passes (QuickCheck).
- [ ] Unknown or missing fields give a clear error.

## Checked
2026-11-03. Confirmed against the Haddock pages for `Data.Aeson` and `Data.Aeson.Types` and `Data.Aeson.TH`: `genericToJSON`, `genericParseJSON`, `genericToEncoding`, `defaultOptions`, `fieldLabelModifier`, `camelTo2`, `omitNothingFields`, `allowOmittedFields`, `rejectUnknownFields`, `sumEncoding`, `tagSingleConstructors`, `eitherDecode`, `eitherDecodeStrict`, `decodeFileStrict`, `withObject`, `.:`, `.:?`, `.!=`, `.=`, `object`, `KeyMap`, `Scientific`. Removed: the memory-blowup claim for large exponents, the error-paths claim, and the Either tagged-object claim.
Method: documentation only; no commands were run.
