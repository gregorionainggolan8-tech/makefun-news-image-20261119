[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/gregorionainggolan8-tech/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/gregorionainggolan8-tech/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# THE WORLD TODAY — Thursday, 19 November 2026

A newspaper front page that sums up the world's news of Thursday
19 November 2026 in a single 1024×1024 image, drawn from scratch with
Python + Pillow (`make_image.py`). The program (`main.ts`) simply copies
the finished image to the output directory; no network, no dependencies,
and the output is byte-identical on every run.

## Stories on the page

**Lead — Trump, Xi and Putin meet in Shenzhen.** US President Donald
Trump has arrived in Shenzhen, China, for a trilateral meeting with
Chinese President Xi Jinping and Russian President Vladimir Putin on
the sidelines of the APEC summit. (CareerIndia school-assembly roundup;
SimpleLife.news daily digest, 19 Nov 2026.)

**Record $81.3bn IPO as Anthropic joins Nasdaq.** Shares priced at $83,
above the $70–$78 range; trading starts Thursday under the ticker ANT.
The largest IPO on record, passing SpaceX's. (BusinessWorld/Reuters,
FinanceFeeds, PYMNTS, 19 Nov 2026.)

**World court to rule on Rohingya genocide case.** The International
Court of Justice delivers its judgment in The Gambia v. Myanmar at The
Hague. (CareerIndia; Pollar News; Daily Spokesman, 19 Nov 2026.)

**Israel launches rare ground operation in central Gaza.** Troops move
beyond the Yellow Line; Australia, Canada, Italy and the UK urge Israel
to let aid reach flooded Gaza. (Sky News via Crypto Economics News;
The Paris Eye, 19 Nov 2026.)

**Crimea Bridge struck again overnight.** Traffic halted after a third
attack in a week; officials assess damage to the key supply route.
(en.h.ua; Le Monde via Crypto Economics News, 19 Nov 2026.)

**US–Iran strikes widen across the Gulf.** Iran hits targets in Kuwait
and Bahrain; the US struck a missile site on Qeshm Island.
(SimpleLife.news, 19 Nov 2026.)

**Also today (footer ticker):** Democrats nominate Hakeem Jeffries for
US House Speaker (NDTV); NASA's Voyager 1 reaches one light-day from
Earth (Al Jazeera); the US pursues a $2bn-plus loan package for the
Philippines (White House via AppiSToS); Grand Theft Auto VI gets its UK
release (BBC).

## How to run / rebuild

```sh
# Re-draw the image from scratch (needs Python 3 + Pillow)
python3 make_image.py

# Run the entrypoint (needs Node 22)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png
```

## License

MIT — see `LICENSE`.
