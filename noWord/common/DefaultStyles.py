#!/usr/bin/env python
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER


assetsDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Choosing font
pdfmetrics.registerFont(
    TTFont('FontAwesome', os.path.join(assetsDir, "FontAwesome.ttf")))


styles = {}

# margins
styles["marginL"] = 78
styles["marginR"] = 78
styles["marginT"] = 106
styles["marginB"] = 78
styles["headerMargin"] = 0.2 * cm
styles["footerMargin"] = 1.2 * cm

# colors
styles['darkgray'] = colors.HexColor("#222222")
styles['green'] = colors.HexColor("#00aa00")
styles['darkyellow'] = colors.HexColor("#999900")

# Some characters usable as list bullets
longdash = u"\u2014"
bullet = "circle"
emptyBullet = u"\u25CB"
arrow = u"\u2192"

# Naming templates
styles["templates"] = {}
styles["templates"]["documentTitleTemplate"] = "{mainSubject}"
styles["templates"]["documentMetaTitleTemplate"] = "{shortDocumentType} {mainSubject} Rev. {revision}"
styles["templates"]["documentMetaAuthorTemplate"] = "noWord"
styles["templates"]["documentMetaSubjectTemplate"] = "{documentType}"
styles["templates"]["documentMetaKeywordsTemplate"] = "{shortDocumentType} {mainSubject}"
styles["templates"]["documentIdentifierTemplate"] = "{shortDocumentType}_{mainSubject}_{revision}.pdf"
styles["templates"]["outputFileTemplate"] = "{shortDocumentType}_{mainSubject}_{revision}.pdf"
styles["templates"]["revisionTemplate"] = "{shortDocumentType}_r.{revision}"

# list styles
styles["itemsInterSpace"] = 0
styles["listBullet"] = bullet
styles["listNumberFormat"] = "%s. "
styles["listBulletFontName"] = "Times-Roman"
styles["listBulletFontSize"] = 10

# table styles
styles["headerBackground"] = colors.lightgrey
styles["highlightBackground"] = colors.HexColor("#ffff00")

# paragraph styles
styles['default'] = ParagraphStyle(name="default",
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
                                   textColor=styles["darkgray"],
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
                                   splitLongWords=1)

styles['BodyText'] = ParagraphStyle(name="BodyText",
                                    parent=styles['default'],
                                    alignment=TA_JUSTIFY,
                                    fontSize=12,
                                    spaceBefore=6,
                                    spaceAfter=6)


styles["HeaderRight"] = ParagraphStyle(name="HeaderRight",
                                       parent=styles['default'],
                                       fontSize=10,
                                       alignment=TA_RIGHT)


styles["FooterRight"] = ParagraphStyle(name="FooterRight",
                                       parent=styles['default'],
                                       fontSize=10,
                                       alignment=TA_RIGHT)
