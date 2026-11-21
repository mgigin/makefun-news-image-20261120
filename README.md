# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/mgigin/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/mgigin/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world's news of **Friday 20 November 2026**: a one-page
broadsheet with 35 stories across 7 regions — every one dated that Friday.

## The image

- **Leads:** Russian missiles hit three Kyiv bridges; Cyclone Akvan comes ashore
  in eastern India; an AI sell-off sinks Asia's stock markets.
- **Features:** UK-EU "reset" deal, COP31's last day, a Russian cruise missile in
  Poland, Iraqi army into a militia stronghold, Italy's general strike, Japan
  inflation at 2.3%, Seoul impeachment move, Kenya's first oil well, Nvidia's
  slide, Phillips' 118 against India.
- **22 more stories** in a numbered list, a world map with numbered pins, a stat
  band, region chips, and a DATE CHECK box that discards 19 November news.
- Every story names its source; officials' counts are attributed.

## Build

`build_image.py` (PIL, deterministic, no network) draws the page at 2x and
downsamples to 1024x1024 `entry.png`. The shipped program only copies it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=c6yw2yzb&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
