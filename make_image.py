#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Thursday, 19 November 2026.

Every story on the page was reported on 19 November 2026 (see README.md
for the sources). The picture is drawn from scratch with Pillow: masthead,
headlines, short decks and simple geometric illustrations. No network, no
external images, no randomness -- running this script always writes the
same bytes to entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GREY = (90, 90, 90)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_flag_us(draw, x, y, w, h):
    """Small US flag: red/white stripes and a blue canton with dots."""
    stripe = h / 13.0
    for i in range(13):
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                       fill=RED if i % 2 == 0 else (255, 255, 255))
    cw, ch = w * 0.4, h * 7 / 13.0
    draw.rectangle([x, y, x + cw, y + ch], fill=(30, 50, 110))
    for r in range(4):
        for c in range(5):
            sx = x + 6 + c * (cw - 10) / 4
            sy = y + 5 + r * (ch - 10) / 3
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))


def draw_flag_cn(draw, x, y, w, h):
    """Small Chinese flag: red field, one big yellow star + four small."""
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))

    def star(cx, cy, r):
        import math
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.38
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=(255, 222, 0))

    star(x + w * 0.18, y + h * 0.25, h * 0.16)
    for dx, dy in [(0.38, 0.12), (0.46, 0.24), (0.46, 0.38), (0.38, 0.48)]:
        star(x + w * dx, y + h * dy, h * 0.06)


def draw_flag_ru(draw, x, y, w, h):
    """Small Russian flag: white, blue, red horizontal bands."""
    for i, col in enumerate([(255, 255, 255), (0, 60, 160), (210, 30, 30)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def draw_summit(draw, x, y, w, h):
    """Three flags on poles above a round summit table, drawn geometrically.

    Labels sit directly under their flag, clear of the table, which is
    drawn low and narrow so nothing overlaps.
    """
    draw.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    draw.rectangle([x, y + h * 0.72, x + w, y + h], fill=(196, 178, 150))
    flags = [draw_flag_us, draw_flag_cn, draw_flag_ru]
    labels = ["USA", "CHINA", "RUSSIA"]
    fw, fh = 140, 84
    gap = (w - 3 * fw) / 4
    for i, (fn, lab) in enumerate(zip(flags, labels)):
        fx = x + gap + i * (fw + gap)
        fy = y + 8
        draw.rectangle([fx + fw, fy, fx + fw + 4, y + h * 0.72], fill=(70, 60, 50))
        fn(draw, fx, fy, fw, fh)
        lab_f = font(SANS_B, 18)
        tw = draw.textlength(lab, font=lab_f)
        draw.text((fx + fw / 2 - tw / 2, fy + fh + 4), lab,
                  font=lab_f, fill=INK)
    # round table, low and narrow
    tx = x + w / 2
    ty = y + h * 0.76
    draw.ellipse([tx - 150, ty, tx + 150, ty + 26], fill=(120, 70, 40))
    draw.rectangle([tx - 10, ty + 22, tx + 10, y + h - 4], fill=(90, 55, 30))


def draw_chart(draw, x, y, w, h):
    """Rising bar chart for the IPO story; h includes the year labels."""
    bars = [("2024", 34), ("2025", 58), ("2026", 100)]
    bw = w / (len(bars) * 2 + 1)
    base = y + h - 24
    for i, (lab, val) in enumerate(bars):
        bx = x + bw * (2 * i + 1)
        bh = (h - 24) * val / 100
        col = RED if i == 2 else (120, 140, 170)
        draw.rectangle([bx, base - bh, bx + bw, base], fill=col)
        lf = font(SANS_B, 16)
        lw = draw.textlength(lab, font=lf)
        draw.text((bx + bw / 2 - lw / 2, base + 4), lab, font=lf, fill=INK)


def draw_scales(draw, x, y, w, h):
    """Simple scales of justice sized to fit a box (x, y, w, h)."""
    cx = x + w / 2
    top, bot = y + 4, y + h - 6
    mid = y + h / 2
    draw.line([(cx, top), (cx, bot)], fill=INK, width=4)
    draw.line([(cx - w * 0.32, top + 6), (cx + w * 0.32, top + 6)],
              fill=INK, width=4)
    draw.rectangle([cx - 40, bot, cx + 40, bot + 5], fill=INK)
    for sx in (cx - w * 0.32, cx + w * 0.32):
        draw.line([(sx, top + 6), (sx, mid)], fill=INK, width=3)
        draw.arc([sx - 26, mid - 12, sx + 26, mid + 12], 0, 180,
                 fill=INK, width=3)
        draw.line([(sx - 26, mid), (sx + 26, mid)], fill=INK, width=3)
    draw.ellipse([cx - 6, top - 4, cx + 6, top + 8], fill=RED)


def draw_column(draw, x, y, w, kicker, head, deck):
    d = draw
    d.text((x, y), kicker, font=font(SANS_B, 16), fill=RED)
    yy = y + 22
    yy = draw_lines(d, wrap(d, head, font(SERIF, 22), w), x, yy,
                    font(SERIF, 22), leading=26)
    yy += 3
    draw_lines(d, wrap(d, deck, font(SANS, 17), w), x, yy,
               font(SANS, 17), leading=21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30  # margin
    R = W - M

    # ---- Masthead (0-168) ----
    hrule(d, M, R, 12, 4)
    title = "THE WORLD TODAY"
    tf = font(SERIF, 66)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 20), title, font=tf, fill=INK)
    hrule(d, M, R, 96, 2)
    date = "Thursday, 19 November 2026"
    df = font(SERIF, 30)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 104), date, font=df, fill=RED)
    tag = "ONE DAY  •  ONE PAGE  •  THE WORLD IN ONE PICTURE"
    tg = font(SANS_B, 16)
    tw2 = d.textlength(tag, font=tg)
    d.text(((W - tw2) / 2, 142), tag, font=tg, fill=GREY)
    hrule(d, M, R, 168, 2)

    # ---- Lead story (176-518) ----
    y = 176
    d.text((M, y), "SUMMIT IN SHENZHEN  •  APEC", font=font(SANS_B, 17), fill=RED)
    y += 24
    hf = font(SERIF, 38)
    y = draw_lines(d, ["TRUMP, XI AND PUTIN MEET", "IN RARE THREE-WAY TALKS"],
                   M, y, hf, leading=44)
    y += 6
    draw_summit(d, M, y, W - 2 * M, 160)
    y += 168
    deck = ("US President Donald Trump has arrived in Shenzhen for a "
            "trilateral meeting with China's Xi Jinping and Russia's "
            "Vladimir Putin at the APEC summit.")
    y = draw_lines(d, wrap(d, deck, font(SANS, 20), W - 2 * M), M, y,
                   font(SANS, 20), leading=25)
    y += 8
    hrule(d, M, R, y, 2)
    y += 12

    # ---- Second row: IPO + ICJ (530-746) ----
    col_w = (W - 2 * M - 24) // 2
    y0 = y
    d.text((M, y0), "TECH  •  MARKETS", font=font(SANS_B, 16), fill=RED)
    y1 = draw_lines(d, wrap(d, "Record $81.3bn IPO as Anthropic joins Nasdaq",
                            font(SERIF, 26), col_w), M, y0 + 22,
                    font(SERIF, 26), leading=31)
    draw_chart(d, M, y1 + 6, col_w, 62)
    y2 = y1 + 74
    draw_lines(d, wrap(d, "Shares priced at $83; trading starts Thursday "
                          "under ticker ANT.", font(SANS, 18), col_w),
               M, y2, font(SANS, 18), leading=22)
    x2 = M + col_w + 24
    d.text((x2, y0), "JUSTICE  •  THE HAGUE", font=font(SANS_B, 16), fill=RED)
    y1b = draw_lines(d, wrap(d, "World court to rule on Rohingya genocide case",
                             font(SERIF, 26), col_w), x2, y0 + 22,
                     font(SERIF, 26), leading=31)
    draw_scales(d, x2 + col_w - 170, y1b + 6, 170, 62)
    y2b = y1b + 74
    draw_lines(d, wrap(d, "The ICJ delivers its judgment in The Gambia "
                          "v. Myanmar today.", font(SANS, 18), col_w),
               x2, y2b, font(SANS, 18), leading=22)
    y = y0 + 216
    hrule(d, M, R, y, 2)
    y += 12

    # ---- Third row: three short stories (758-937) ----
    cw3 = (W - 2 * M - 48) // 3
    draw_column(d, M, y, cw3, "GAZA",
                "Israel launches rare ground operation in central Gaza",
                "Troops move beyond the Yellow Line; four allies urge "
                "Israel to let aid reach flooded Gaza.")
    draw_column(d, M + cw3 + 24, y, cw3, "UKRAINE",
                "Crimea Bridge struck again overnight",
                "Traffic halted after a third attack in a week as "
                "officials assess damage to the supply route.")
    draw_column(d, M + 2 * (cw3 + 24), y, cw3, "THE GULF",
                "US–Iran strikes widen across the Gulf",
                "Iran hits targets in Kuwait and Bahrain; the US struck "
                "a missile site on Qeshm Island.")
    y += 167
    hrule(d, M, R, y, 2)

    # ---- Ticker + footer (945-1010) ----
    y += 10
    ticker = ("ALSO TODAY:  Democrats nominate Hakeem Jeffries for US House "
              "Speaker  •  Voyager 1 reaches one light-day from Earth  •  "
              "US pursues $2bn-plus loan for the Philippines  •  GTA VI gets "
              "UK release")
    y = draw_lines(d, wrap(d, ticker, font(SANS_B, 17), W - 2 * M), M, y,
                   font(SANS_B, 17), fill=INK, leading=21)
    y += 6
    hrule(d, M, R, y, 2)
    y += 7
    foot = "THE WORLD TODAY  •  Thursday, 19 November 2026  •  All stories reported on 19 November 2026"
    ff = font(SANS, 14)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, y), foot, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
