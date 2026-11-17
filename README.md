# makefun-tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/woodhntr1-gif/makefun-tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/woodhntr1-gif/makefun-tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A complete chess engine in 3,998 bytes of Python (cap: 4,096) — the whole entry is `main.py` at the root, and it reads or runs no other file. 0x88 board, negamax alpha-beta with capture quiescence and MVV-LVA ordering, iterative deepening under a fixed 60,000-node budget: fully deterministic (no clock, no randomness), stdlib only, UCI on stdin/stdout.

## Run it

```sh
python3 -P -s main.py
```

Speaks UCI: `uci`, `isready`, `ucinewgame`, `position startpos|fen … [moves …]`, `go …`, `quit`. The `go` parameters are parsed but ignored by design — every move uses the same fixed node budget, so the chosen move is a pure function of the position.

---

<sub>Entered on [make.fun](https://make.fun/?ref=rez34v58&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>

## Design

- **Board:** 0x88 mailbox (128 squares), pieces as signed ints (white positive, black negative; 1 pawn … 6 king), castling bitmask, en-passant square, make/unmake with a history stack.
- **Moves:** pseudo-legal generation (pawn pushes/captures/en passant, queen-only promotions, sliders, king, fully-checked castling). Interior nodes punish a move that leaves its own king en prise via king-capture scoring (Sunfish-style); root moves are filtered through full legality, so the played move is always legal.
- **Search:** negamax + alpha-beta; capture quiescence with stand-pat; mate/stalemate at terminal nodes; iterative deepening discards an unfinished iteration when the budget runs out. Depth 4–6 in the middlegame, 0.7–2.2 s per move locally — far under the 10 s/move cap.
- **Evaluation:** material (100/320/330/500/900) plus formulaic positional terms (pawn advancement/centrality, piece centrality, king-centrality penalty) — piece-square tables would not fit.

## Tests

Local suite (kept outside this repo — the entry tree is size-capped): 16/16 checks pass — byte size, single `import sys`, no `time`/`random`/`open(`, UCI handshake, legal bestmoves, mate-in-1, hanging queen taken, promotion, determinism, and a 30-ply self-play game with every move validated by an independent legal-move generator.

## Honest limits

Elo cannot be verified locally (no house engines or Sunfish baseline available); queen-only promotions are generated (underpromotions are vanishingly rare); no repetition/fifty-move handling, no opening book — the harness's draw rules still apply.
