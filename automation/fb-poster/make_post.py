#!/usr/bin/env python3
"""
Picks today's Facebook post (random topic, avoiding recent repeats),
generates a branded 1080x1080 image, and prints the image path + caption
as JSON on stdout so the calling agent can upload it to Facebook.

Usage: python3 make_post.py
"""
import json, os, random, sys, textwrap
from datetime import date
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TOPICS_FILE = os.path.join(HERE, "topics.json")
STATE_FILE = os.path.join(HERE, "state", "recent.json")
IMG_DIR = os.path.join(HERE, "images")
LOGO = "/home/claude/legalkhata-oldrepo/assets/img/logo-white.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# Brand palette (rotates per post so the feed doesn't look identical every day)
PALETTES = [
    ("#0b3d2e", "#eafff2"),  # deep green / mint text
    ("#102a43", "#e8f0ff"),  # navy / pale blue text
    ("#5c1a1a", "#ffece8"),  # maroon / warm white text
    ("#1a2e05", "#f2ffe0"),  # olive / lime-tinted white
]

W = H = 1080

def wrap(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if draw.textlength(test, font=font) <= max_width:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def load_recent():
    try:
        return json.load(open(STATE_FILE))
    except Exception:
        return []

def save_recent(recent):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    json.dump(recent[-8:], open(STATE_FILE, "w"))

def pick_topic(topics):
    recent = load_recent()
    choices = [t for t in topics if t["id"] not in recent] or topics
    topic = random.choice(choices)
    recent.append(topic["id"])
    save_recent(recent)
    return topic

def make_image(topic, out_path):
    bg_hex, fg_hex = random.choice(PALETTES)
    img = Image.new("RGB", (W, H), bg_hex)
    draw = ImageDraw.Draw(img)

    # thin accent bar at top
    draw.rectangle([0, 0, W, 14], fill=fg_hex)

    # headline
    headline_font = ImageFont.truetype(F_BOLD, 64)
    lines = wrap(draw, topic["headline"], headline_font, W - 160)
    y = 160
    for ln in lines:
        draw.text((80, y), ln, font=headline_font, fill=fg_hex)
        y += 78

    # thin rule
    y += 20
    draw.line([(80, y), (W - 80, y)], fill=fg_hex, width=2)
    y += 50

    # short body (first ~2 lines of the caption, trimmed, no emoji/phone/link lines)
    body_font = ImageFont.truetype(F_REG, 34)
    body_src = topic["caption"].split("\n\n")[0]
    for ln in wrap(draw, body_src, body_font, W - 160)[:6]:
        draw.text((80, y), ln, font=body_font, fill=fg_hex)
        y += 46

    # footer: logo + contact
    try:
        logo = Image.open(LOGO).convert("RGBA")
        logo.thumbnail((260, 90))
        img.paste(logo, (80, H - 190), logo)
    except Exception:
        pass
    contact_font = ImageFont.truetype(F_BOLD, 32)
    draw.text((80, H - 90), "legalkhata.com   •   +91 70489 15155", font=contact_font, fill=fg_hex)

    os.makedirs(IMG_DIR, exist_ok=True)
    img.save(out_path, "PNG")

def main():
    topics = json.load(open(TOPICS_FILE))
    topic = pick_topic(topics)
    out_path = os.path.join(IMG_DIR, "post-%s.png" % date.today().isoformat())
    make_image(topic, out_path)
    print(json.dumps({"image_path": out_path, "caption": topic["caption"], "topic_id": topic["id"]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
