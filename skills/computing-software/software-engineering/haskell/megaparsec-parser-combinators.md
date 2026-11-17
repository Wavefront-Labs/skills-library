---
id: computing-software.software-engineering.haskell.megaparsec-parser-combinators
name: megaparsec-parser-combinators
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, megaparsec, attoparsec, parsec, parser-combinators, lexer, parse-errors, parsec-alternatives, applicative-parsing, megaparsec-parser-combinators]
level: advanced
status: draft
description: "Write parsers with megaparsec (Parsec type, lexeme/symbol, try, errors) or attoparsec (fast, backtracking), operator tables and good error messages."
sources: ["https://hackage.haskell.org/package//aeson", "https://hackage.haskell.org/package//megaparsec", "https://hackage.haskell.org/package//attoparsec"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parser combinators

**Goal:** parse text or bytes into structure with good errors.

```haskell
{-# LANGUAGE OverloadedStrings #-}
import Text.Megaparsec
import Text.Megaparsec.Char
import qualified Text.Megaparsec.Char.Lexer as L
import Control.Monad.Combinators.Expr (makeExprParser, Operator(..))
import Data.Void
type Parser = Parsec Void Text

sc :: Parser ()
sc = L.space space1 (L.skipLineComment "--") (L.skipBlockComment "{-" "-}")
lexeme = L.lexeme sc
symbol = L.symbol sc
integer = lexeme L.decimal
parens = between (symbol "(") (symbol ")")

expr :: Parser Int
expr = makeExprParser term [[InfixL ((*) <$ symbol "*")], [InfixL ((+) <$ symbol "+"), InfixL ((-) <$ symbol "-")]]
term = parens expr <|> integer

main = case parse (sc *> expr <* eof) "input" "1 + 2 * (3 - 1)" of
  Left err -> putStr (errorBundlePretty err)
  Right v  -> print v
```

## Choosing
- **megaparsec**: rich error messages (custom `ParseError` components, labels with `<?>`), streams of Text/String/ByteString, maintained and common for languages and configs.
- **attoparsec**: very fast incremental ByteString/Text parser; always backtracks; poor errors; good for protocols and logs.
- **parsec**: older, the model for both; `parsec` ships with GHC.
- **happy/alex**: generator-based parsers/lexers for large grammars; `trifecta`, `earley` for ambiguous grammars.

## Rules and gotchas
- megaparsec does not backtrack on consumed input: wrap alternatives that share prefixes with `try`; `notFollowedBy` for keywords; `lookAhead`.
- Whitespace convention: every token parser consumes trailing space (lexeme), the top-level consumes leading space once.
- Left recursion loops: use `makeExprParser`, `chainl1`, or `many`.
- Always require `eof`; otherwise trailing junk is ignored.
- Label tokens (`<?>`) for readable errors; avoid `try` everywhere because it degrades them.

## Self-check
- [ ] Parser handles `1+2`, ` 1 + 2 `, and rejects `1+`.
- [ ] Error output shows line, column and expected tokens.
