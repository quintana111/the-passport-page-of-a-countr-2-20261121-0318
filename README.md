# The Passport Page of a Country That Isn't There

[![the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/quintana111/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/quintana111/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

An invented passport spread for the **Republic of Meridia** — a country
that isn't there. One 1024×1024 image, deep teal and gold on cream paper,
with fine guilloché line work throughout.

- **Left page — data page:** a stylised geometric portrait (not a real
  person), holder Elena Maris Amara, passport MD 4829137, dates of issue
  and expiry, the Meridian coat of arms (star shield), and a machine-readable
  MRZ strip along the bottom.
- **Right page — visas & stamps:** four fictional entry stamps — Port
  Serenne (02 Jun 2026), Caldor Bay (19 Jul 2026), Velmora (03 Sep 2026),
  Ostara (21 Oct 2026) — over a large watermark compass-star emblem, plus
  a multiple-entry visa box and the holder's signature.

The image is rendered deterministically with Python PIL (`compose.py`) and
contains no AI-generated art. Two runs are byte-identical.

## Run

```sh
# Re-render the spread (PIL only; deterministic)
python3 compose.py

# Copy the entry image to /output/entry.png with sha256 verification
node main.ts
```

## Files

- `entry.png` — the entry image (1024×1024, PNG)
- `main.ts` — Node 22, stdlib only; copies `entry.png` to `/output/entry.png` and verifies byte-length + sha256 on read-back
- `compose.py` — the deterministic PIL renderer that draws the spread
