#!/usr/bin/env python3
"""Build the dimensionless static-family surface-stress plot as vector PDF."""

from math import sqrt
from pathlib import Path

from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas


OUT = Path(__file__).with_name("figure2_static_family.pdf")
W, H = 900, 545
LEFT, RIGHT, BOTTOM, TOP = 92, 865, 72, 505
XMIN, XMAX, YMIN, YMAX = 2.0, 8.0, -2.0, 2.0


def xp(x):
    return LEFT + (x - XMIN) * (RIGHT - LEFT) / (XMAX - XMIN)


def yp(y):
    return BOTTOM + (y - YMIN) * (TOP - BOTTOM) / (YMAX - YMIN)


def draw_curve(c, function, color, dash=None, width=2.3):
    path = c.beginPath()
    first = True
    for i in range(1601):
        x = 2.015 + (8.0 - 2.015) * i / 1600
        y = max(YMIN - 0.2, min(YMAX + 0.2, function(x)))
        if first:
            path.moveTo(xp(x), yp(y)); first = False
        else:
            path.lineTo(xp(x), yp(y))
    c.saveState()
    c.setStrokeColor(color); c.setLineWidth(width)
    if dash:
        c.setDash(dash)
    c.drawPath(path, stroke=1, fill=0)
    c.restoreState()


def main():
    blue = Color(0.12, 0.31, 0.48)
    orange = Color(0.65, 0.29, 0.16)
    green = Color(0.18, 0.49, 0.20)
    purple = Color(0.42, 0.30, 0.60)
    gray = Color(0.35, 0.35, 0.35)
    grid = Color(0.84, 0.84, 0.84)

    c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setFillColor(white); c.rect(0, 0, W, H, stroke=0, fill=1)

    # Grid and axes.
    c.setStrokeColor(grid); c.setLineWidth(0.7)
    for x in range(2, 9):
        c.line(xp(x), BOTTOM, xp(x), TOP)
    for y in range(-2, 3):
        c.line(LEFT, yp(y), RIGHT, yp(y))
    c.setStrokeColor(black); c.setLineWidth(1.1)
    c.rect(LEFT, BOTTOM, RIGHT - LEFT, TOP - BOTTOM, stroke=1, fill=0)
    c.line(LEFT, yp(0), RIGHT, yp(0))

    # Curves in units c^4/(8 pi G m).
    draw_curve(c, lambda x: -2 * sqrt(1 - 2 / x) / x, blue)
    draw_curve(c, lambda x: (x - 1) / (x * x * sqrt(1 - 2 / x)), orange, [8, 5])
    draw_curve(c, lambda x: (3 - x) / (x * x * sqrt(1 - 2 / x)), green, None, 2.6)
    draw_curve(c, lambda x: 2 / (x * x * sqrt(1 - 2 / x)), purple, [2, 4])

    # Photon sphere marker.
    c.saveState(); c.setStrokeColor(gray); c.setLineWidth(1.1); c.setDash(7, 4)
    c.line(xp(3), BOTTOM, xp(3), TOP); c.restoreState()
    c.saveState(); c.translate(xp(3) + 13, TOP - 10); c.rotate(-90)
    c.setFillColor(gray); c.setFont("Times-Roman", 14)
    c.drawString(0, 0, "photon sphere   R0 = 3m"); c.restoreState()

    # Tick labels.
    c.setFillColor(black); c.setFont("Times-Roman", 13)
    for x in range(2, 9):
        c.drawCentredString(xp(x), BOTTOM - 22, str(x))
    for y in range(-2, 3):
        c.drawRightString(LEFT - 11, yp(y) - 4, str(y))
    c.setFont("Times-Roman", 16)
    c.drawCentredString((LEFT + RIGHT) / 2, 24, "Matched radius   R0 / m")
    c.saveState(); c.translate(25, (BOTTOM + TOP) / 2); c.rotate(90)
    c.drawCentredString(0, 0, "Surface stress in units of c^4 / (8 pi G m)")
    c.restoreState()

    # Legend.
    legend = [(blue, None, "m sigma0"), (orange, [8, 5], "m ps0"),
              (green, None, "m (sigma0 + ps0)"), (purple, [2, 4], "m (sigma0 + 2 ps0)")]
    lx, ly = 575, 468
    c.setFillColor(Color(1, 1, 1, alpha=0.94)); c.setStrokeColor(Color(.65, .65, .65))
    c.rect(lx - 14, ly - 74, 287, 86, stroke=1, fill=1)
    for idx, (color, dash, label) in enumerate(legend):
        row = idx // 2; col = idx % 2
        x0 = lx + col * 140; y0 = ly - row * 36
        c.saveState(); c.setStrokeColor(color); c.setLineWidth(2.4)
        if dash: c.setDash(dash)
        c.line(x0, y0, x0 + 33, y0); c.restoreState()
        c.setFillColor(black); c.setFont("Times-Roman", 12.5); c.drawString(x0 + 40, y0 - 4, label)

    # Region labels.
    c.setFillColor(green); c.setFont("Times-Bold", 13)
    c.drawString(xp(2.18), yp(0.63), "NEC satisfied")
    c.drawString(xp(4.45), yp(-0.63), "NEC violated")
    c.setStrokeColor(green); c.setLineWidth(1.2)
    c.line(xp(2.55), yp(0.54), xp(2.63), yp(0.24))
    c.line(xp(4.52), yp(-0.53), xp(4.25), yp(-0.09))

    c.showPage(); c.save(); print(OUT)


if __name__ == "__main__":
    main()
