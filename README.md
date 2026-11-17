# makefun-tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/woodhntr1-gif/makefun-tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/woodhntr1-gif/makefun-tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine for the tiny-chess-01 gauntlet. `main.py` (2,877 bytes, cap 4,096) is the whole entry: the `makefun compress` packing (LZMA) of a 6,897-byte readable source, reading or running no other file. The source ships beside the transcripts in the bundle (`packs/`), not in this repo.

## How it plays

This competition is **not** UCI. The engine is an HTTP client of the contest env at `MAKEFUN_ENV_URL`: POST `/game`, compute a move from the served FEN, POST `/move`, repeat until the env answers `status: "done"`. Each move is validated against the env's `legal_moves` first; any failure falls back to a legal move and a re-sync, so the program never crashes out of a game.

```sh
python3 -P -s main.py   # with MAKEFUN_ENV_URL set, as the harness runs it
```

## Design

- **Board:** 0x88 mailbox, signed-int pieces, make/unmake with a history stack; king squares, game phase, bishop counts and the evaluation score are maintained incrementally (verified against from-scratch recomputation over random legal lines).
- **Search:** negamax alpha-beta with a transposition table; iterative deepening under a fixed 100,000-node budget (no clock, no randomness — same position and game history, same move); MVV-LVA ordering; quiescence over captures and promotions with delta pruning, searching legal evasions only when in check. A root move that repeats an earlier position of the game is scored as a draw when ahead, so the engine does not shuffle into a threefold draw from a better position.
- **Evaluation:** material (100/320/330/500/900), full piece-square tables, a phase-blended king table (shelter vs endgame activity), bishop pair.

## Why this entry replaces the first one

The first submission scored practice Elo 0. Diagnosis, reproduced locally against the kit's own env server: that engine spoke UCI on stdin/stdout, but this harness closes stdin and expects the env protocol above — it exited instantly, made zero HTTP calls, and all 6 practice games were scored "unplayed". The chess core was sound; the driver spoke the wrong protocol. This entry keeps a strengthened descendant of that core behind the correct env driver.

## Local verification (kit env, practice trial-0 — the graded practice instance)

Kit env seeded by `practice/trial-0`, bot run as the harness runs it (`python3 -P -s main.py`, stdin closed): wins by checkmate against depth-2 (855, 73 plies), depth-3 (1073, 94 plies) and depth-4 (1199, 79 plies); losses by checkmate against nodes-100k (1392, 161 plies), nodes-250k (1497, 108 plies) and nodes-500k (1596, 147 plies). 3 points from 6 games = **local practice Elo 1,279** (final-entry floor 1,154; house baseline ≈ 1,365 on 6-game practice trials). Every game completed, every env answer HTTP 200, slowest move ~2.5 s of the 10 s limit, full trial ~9 min of the 30-min wall budget on a shared VM. The source also passes tactical unit tests (mate-in-1, Qxf7 mate, promotion, en passant) and is deterministic: repeated gauntlet runs reproduce the same games move for move.

## Honest limits

Promotions are queen-only. The node-rung engines (1392+) still out-search this one, and instance variance is large: on practice trial-2 (colours swapped) it scored Elo 708 (one draw, five losses), so beating the ~1,365 baseline in the final is not expected.

---

<sub>Entered on [make.fun](https://make.fun/?ref=rez34v58&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
