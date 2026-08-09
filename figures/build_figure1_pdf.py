#!/usr/bin/env python3
"""Build the junction-orientation schematic as a native vector PDF."""

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, Color, white


OUT = Path(__file__).with_name("figure1_junction_orientation.pdf")
W, H = 1200, 690


def arrow(c, x1, y1, x2, y2, open_head=False):
    c.saveState()
    c.setStrokeColor(black); c.setFillColor(black)
    c.setLineWidth(2.5)
    c.line(x1, y1, x2, y2)
    head = [(x2, y2), (x2 - 15, y2 + 8), (x2 - 15, y2 - 8)]
    p = c.beginPath()
    p.moveTo(*head[0]); p.lineTo(*head[1]); p.lineTo(*head[2])
    if open_head:
        c.setFillColor(white); c.setStrokeColor(black)
        p.close(); c.drawPath(p, stroke=1, fill=1)
    else:
        p.close(); c.drawPath(p, stroke=1, fill=1)
    c.restoreState()


def centered(c, text, x, y, size=20, bold=False):
    c.setFont("Times-Bold" if bold else "Times-Roman", size)
    c.drawCentredString(x, y, text)


def main():
    c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setFillColor(white); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(black); c.setStrokeColor(black)
    centered(c, "Declared timelike junction and retained regions", W / 2, 646, 27, True)

    # Retained regions, with restrained monochrome textures.
    c.setFillColor(Color(.97, .97, .97)); c.rect(72, 143, 440, 455, stroke=1, fill=1)
    c.setFillColor(Color(.985, .985, .985)); c.rect(512, 143, 616, 455, stroke=1, fill=1)
    c.saveState()
    clip = c.beginPath(); clip.rect(72, 143, 440, 455); c.clipPath(clip, stroke=0)
    c.setStrokeColor(Color(.72, .72, .72)); c.setLineWidth(.7)
    for x in range(-250, 750, 18): c.line(x, 143, x + 330, 598)
    c.restoreState()
    c.setFillColor(Color(.58, .58, .58))
    for x in range(530, 1120, 22):
        for y in range(160, 590, 22): c.circle(x, y, 1.1, stroke=0, fill=1)
    c.setStrokeColor(black); c.setFillColor(black); c.setLineWidth(2)
    c.rect(72, 143, 440, 455, stroke=1, fill=0); c.rect(512, 143, 616, 455, stroke=1, fill=0)

    centered(c, "Homogeneous Kantowski-Sachs side", 292, 558, 24, True)
    centered(c, "Retained Schwarzschild exterior", 820, 558, 24, True)
    centered(c, "Areal radius depends only on time", 292, 520, 19)
    centered(c, "F(R) = 1 - 2m/R > 0", 820, 520, 19)

    # Timelike shell.
    p = c.beginPath(); p.moveTo(512, 143)
    p.curveTo(485, 230, 539, 322, 512, 415)
    p.curveTo(485, 505, 539, 550, 512, 598)
    c.setLineWidth(7); c.drawPath(p, stroke=1, fill=0)
    c.setFont("Times-Bold", 22); c.drawString(535, 365, "Shell")
    c.setFont("Times-Roman", 18); c.drawString(535, 337, "timelike shell")
    c.drawString(535, 311, "areal radius R")

    arrow(c, 518, 440, 685, 440)
    centered(c, "parent normal: outward (+ branch)", 610, 460, 19)
    arrow(c, 675, 270, 965, 270, True)
    centered(c, "increasing areal radius R", 820, 291, 19)
    c.circle(1060, 270, 7, stroke=0, fill=1)
    centered(c, "spatial infinity", 1060, 299, 19)
    arrow(c, 505, 220, 397, 220, True)
    centered(c, "child normal: either orientation", 430, 241, 19)

    c.setLineWidth(1.5); c.line(72, 105, 1128, 105)
    c.setFont("Times-Roman", 18)
    c.drawString(72, 70, "Ordinary exterior branch: the retained parent contains spatial infinity, so its normal points toward increasing R.")
    c.drawString(72, 39, "The negative parent branch retains a different Schwarzschild side; it is not a sign alternative for this gluing.")
    c.showPage(); c.save()
    print(OUT)


if __name__ == "__main__":
    main()
