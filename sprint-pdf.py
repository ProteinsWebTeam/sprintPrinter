import re
import copy
import sys
import csv
import argparse
from reportlab.lib.units import cm
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import KeepInFrame

from reportlab.lib.colors import (
    red, yellow, green, blue, orange, violet, black, purple, white, magenta,
    cyan, darkred, lightblue, darkgreen, darkseagreen, darkblue, darkslateblue
)

from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from textwrap import wrap

parser = argparse.ArgumentParser(
    description='Generate PDF with stories from a sprint'
)
parser.add_argument(
    '--input', '-i', type=str,
    help='input file (tsv file from Jira)'
)
parser.add_argument(
    '--output', '-o', type=str,
    help='output file (pdf)'
)
args = parser.parse_args()

if args.input:
    input = open(args.input, 'r')
else:
    input = sys.stdin

if args.output:
    output = args.output
else:
    output = sys.stdout


def debug_log(*text):
    print(*text, file=(sys.stderr if args.output else sys.stdout))

styles = getSampleStyleSheet()

ParaStyle = copy.deepcopy(styles['Normal'])
ParaStyle.spaceBefore = 0.2 * cm
ParaStyle.alignment = TA_JUSTIFY


def stylesheet():
    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            textColor=black,
            backColor=None,
            wordWrap=None,
            borderWidth=0,
            borderPadding=0,
            borderColor=None,
            borderRadius=None,
            allowWidows=1,
            allowOrphans=0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
        ),
    }
    styles['title_left'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=TA_LEFT,
        textColor=black,
    )
    styles['body_text'] = ParagraphStyle(
        'BodyText',
        parent=styles['default'],
        fontName='Helvetica',
        fontSize=14,
        leading=16,
        alignment=TA_LEFT,
        textColor=black,
    )
    styles['alert'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        leading=14,
        backColor=yellow,
        borderColor=black,
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
    )
    return styles


def create_story_card(c, story, y_value):
    availableWidth = 360
    availableHeight = 180
    topline = 650
    left_edge_x = 80
    left_edge_y = 420

    allowedWidth = 400
    allowedHeight = 280

    c.roundRect(
        left_edge_x, left_edge_y - y_value,
        400, 280, 4, stroke=1, fill=0
    )
    c.line(left_edge_x, topline - y_value, 480, topline - y_value)
    c.setFont('Helvetica-Bold', 25)
    c.drawString(110, 670-y_value, story[0][4:8])
    c.line(225, topline-y_value, 225, 700-y_value)
    c.setFont('Helvetica', 16)
    c.drawString(230, 670-y_value, '')
    c.line(380, topline-y_value, 380, 700-y_value)
    c.setFont('Helvetica-Bold', 25)
    c.drawString(420, 670-y_value, story[2])
    try:
        code = int(story[1])
    except:
        try:
            code = [
                x in story[1].lower()
                for x in ['XXX', 'interpro', 'emg ', 'hmmer', 'pfam']
            ].index(True)
        except:
            code = 5

    colors = [
        None, purple, (0.45, 0.62, 0.67), darkred,
        darkslateblue, orange, lightblue
    ]
    c.setFillColor(colors[code])

    c.rect(left_edge_x, topline-y_value, 20, 50, stroke=0, fill=1)
    c.rect(220, topline-y_value, 5, 50, stroke=0, fill=1)

    c.setFillColor(green)
    c.setFont('Helvetica', 16)
    time = story[3]
    try:
        time = int(time)
        if time > 200:  # in seconds
            time = time/3600
    except:
        time = 'NaN'
    c.drawString(370, 430-y_value, 'story points: ' + str(int(time)))

    # some other annotations

    c.setFillColor(black)
    mystylesheet = stylesheet()
    story_title = Paragraph(story[5], mystylesheet['title_left'])

    wt, ht = story_title.wrap(380, 80)
    lines = story_title.getActualLineWidths0()
    debug_log(lines)
    line_count = len(lines)
    debug_log(len(story[4]), line_count)
    y_start = 620
    yt_offset = (line_count-1) * 25
    if line_count > 1:
        yt_offset = (line_count-1) * 25
        y_start = 620 - yt_offset

    story_title.drawOn(c, 90, y_start-y_value)
    if len(story) > 6:
        debug_log(len(story))
        new_desc = story[6][:350]
        desc = Paragraph(new_desc, mystylesheet['body_text'])
        wdtxt, hdtxt = desc.wrap(370, 80)
        desc_lines = desc.getActualLineWidths0()
        desc_line_count = len(desc_lines)
        debug_log(len(story[6]), desc_lines)
        desc_y_start = 580 - yt_offset
        yd_offset = 0
        if desc_line_count > 1:
            yd_offset = ((desc_line_count-1) * 14)
            desc_y_start = desc_y_start - yd_offset
        desc.drawOn(c, 110, desc_y_start-y_value)

# generate the story cards


def even():
    even = True
    while True:
        yield even
        even = not even

c = canvas.Canvas(output, pagesize=pagesizes.A4)
(width, height) = pagesizes.A4

for [story, even] in zip(csv.reader(input, delimiter='\t'), even()):
    # print story
    if len(story) < 2:
        continue
    debug_log(story)
    if even:
        create_story_card(c, story, 0)
    else:
        create_story_card(c, story, 350)
        c.showPage()
        debug_log(story)

c.showPage()
c.save()
