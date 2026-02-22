"""
Procurement Contract PDF Generator
Generates a professional supplier contract for ABC Supplies Inc.
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import BalancedColumns
from reportlab.pdfgen import canvas
from datetime import date
import os

OUTPUT_PATH = "/Users/mohanavasaram/Gen AI Claud Projects/Dynamic Discounts/Supplier_Contract_ABC_Supplies_Inc.pdf"

# ─── Color Palette ──────────────────────────────────────────────────────────
NAVY       = colors.HexColor("#0D2B55")
STEEL      = colors.HexColor("#1F5F8B")
GOLD       = colors.HexColor("#C9A84C")
LIGHT_GREY = colors.HexColor("#F4F6F9")
MID_GREY   = colors.HexColor("#D1D9E6")
DARK_GREY  = colors.HexColor("#4A4A4A")
WHITE      = colors.white
GREEN      = colors.HexColor("#1A7A4A")
RED        = colors.HexColor("#8B1A1A")

# ─── Page Numbers Header/Footer ──────────────────────────────────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for page_num, state in enumerate(self._saved_page_states, start=1):
            self.__dict__.update(state)
            self.draw_header_footer(page_num, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, page_num, page_count):
        w, h = LETTER

        # Header bar
        self.setFillColor(NAVY)
        self.rect(0, h - 0.65*inch, w, 0.65*inch, fill=1, stroke=0)

        # Header left: company
        self.setFillColor(WHITE)
        self.setFont("Helvetica-Bold", 9)
        self.drawString(0.5*inch, h - 0.38*inch, "PINNACLE GLOBAL SOLUTIONS LLC")
        self.setFont("Helvetica", 7.5)
        self.drawString(0.5*inch, h - 0.52*inch, "1250 Commerce Boulevard, Suite 400  |  Chicago, IL 60601  |  USA")

        # Header right: contract ref
        self.setFont("Helvetica-Bold", 8)
        self.drawRightString(w - 0.5*inch, h - 0.38*inch, "CONTRACT REF: PGS-2026-SC-0047")
        self.setFont("Helvetica", 7.5)
        self.drawRightString(w - 0.5*inch, h - 0.52*inch, f"Effective Date: March 1, 2026")

        # Gold accent line under header
        self.setStrokeColor(GOLD)
        self.setLineWidth(2)
        self.line(0, h - 0.67*inch, w, h - 0.67*inch)

        # Footer bar
        self.setFillColor(NAVY)
        self.rect(0, 0, w, 0.5*inch, fill=1, stroke=0)

        self.setFillColor(GOLD)
        self.setFont("Helvetica-Bold", 7.5)
        self.drawString(0.5*inch, 0.18*inch, "CONFIDENTIAL – PROPRIETARY DOCUMENT")

        self.setFillColor(WHITE)
        self.setFont("Helvetica", 7.5)
        self.drawCentredString(w/2, 0.18*inch, "Supplier Contract | ABC Supplies Inc. | PGS-2026-SC-0047")
        self.drawRightString(w - 0.5*inch, 0.18*inch, f"Page {page_num} of {page_count}")



# ─── Style Definitions ───────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    styles = {
        "cover_title": ParagraphStyle(
            "cover_title", fontName="Helvetica-Bold", fontSize=26,
            textColor=NAVY, alignment=TA_CENTER, spaceAfter=6, leading=32
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle", fontName="Helvetica", fontSize=13,
            textColor=STEEL, alignment=TA_CENTER, spaceAfter=4, leading=18
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta", fontName="Helvetica", fontSize=10,
            textColor=DARK_GREY, alignment=TA_CENTER, spaceAfter=3, leading=15
        ),
        "section_header": ParagraphStyle(
            "section_header", fontName="Helvetica-Bold", fontSize=11.5,
            textColor=WHITE, alignment=TA_LEFT, spaceAfter=0,
            spaceBefore=14, leading=14
        ),
        "subsection": ParagraphStyle(
            "subsection", fontName="Helvetica-Bold", fontSize=10,
            textColor=NAVY, spaceBefore=8, spaceAfter=3, leading=13
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=9.5,
            textColor=DARK_GREY, alignment=TA_JUSTIFY, spaceAfter=5,
            leading=14, leftIndent=0
        ),
        "body_indent": ParagraphStyle(
            "body_indent", fontName="Helvetica", fontSize=9.5,
            textColor=DARK_GREY, alignment=TA_JUSTIFY, spaceAfter=4,
            leading=14, leftIndent=18
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Helvetica", fontSize=9.5,
            textColor=DARK_GREY, alignment=TA_JUSTIFY, spaceAfter=3,
            leading=14, leftIndent=24, firstLineIndent=-12
        ),
        "highlight_box": ParagraphStyle(
            "highlight_box", fontName="Helvetica", fontSize=9.5,
            textColor=DARK_GREY, alignment=TA_JUSTIFY, spaceAfter=4,
            leading=14, leftIndent=6, rightIndent=6
        ),
        "table_header": ParagraphStyle(
            "table_header", fontName="Helvetica-Bold", fontSize=9,
            textColor=WHITE, alignment=TA_CENTER, leading=12
        ),
        "table_cell": ParagraphStyle(
            "table_cell", fontName="Helvetica", fontSize=9,
            textColor=DARK_GREY, alignment=TA_LEFT, leading=12
        ),
        "table_cell_center": ParagraphStyle(
            "table_cell_center", fontName="Helvetica", fontSize=9,
            textColor=DARK_GREY, alignment=TA_CENTER, leading=12
        ),
        "table_cell_bold": ParagraphStyle(
            "table_cell_bold", fontName="Helvetica-Bold", fontSize=9,
            textColor=NAVY, alignment=TA_LEFT, leading=12
        ),
        "emphasis": ParagraphStyle(
            "emphasis", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=GREEN, alignment=TA_JUSTIFY, spaceAfter=4, leading=14
        ),
        "warning": ParagraphStyle(
            "warning", fontName="Helvetica-BoldOblique", fontSize=9,
            textColor=RED, spaceAfter=4, leading=13
        ),
        "signature_label": ParagraphStyle(
            "signature_label", fontName="Helvetica-Bold", fontSize=9,
            textColor=NAVY, alignment=TA_LEFT, leading=13
        ),
        "signature_value": ParagraphStyle(
            "signature_value", fontName="Helvetica", fontSize=9,
            textColor=DARK_GREY, alignment=TA_LEFT, leading=13
        ),
    }
    return styles


# ─── Section Header Helper ────────────────────────────────────────────────────
def section_block(number, title, styles, story):
    story.append(Spacer(1, 0.1*inch))
    data = [[Paragraph(f"  ARTICLE {number}  —  {title.upper()}", styles["section_header"])]]
    t = Table(data, colWidths=[7.0*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LINEBELOW",    (0, 0), (-1, -1), 2, GOLD),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.06*inch))


def highlight_table(rows, col_widths, story, header_bg=STEEL):
    """Renders a styled data table with alternating row shading."""
    table_data = []
    for i, row in enumerate(rows):
        table_data.append([Paragraph(str(cell), ParagraphStyle(
            f"tc{i}", fontName="Helvetica-Bold" if i == 0 else "Helvetica",
            fontSize=9, textColor=WHITE if i == 0 else DARK_GREY,
            alignment=TA_CENTER, leading=12
        )) for cell in row])

    t = Table(table_data, colWidths=col_widths)
    style = [
        ("BACKGROUND",    (0, 0), (-1, 0),  header_bg),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GREY),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.5, GOLD),
    ]
    for r in range(1, len(rows)):
        if r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), LIGHT_GREY))
    t.setStyle(TableStyle(style))
    story.append(t)
    story.append(Spacer(1, 0.08*inch))


# ─── Main Document Build ──────────────────────────────────────────────────────
def build_contract():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=LETTER,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.9*inch,
        bottomMargin=0.75*inch,
        title="Supplier Agreement – ABC Supplies Inc.",
        author="Pinnacle Global Solutions LLC",
        subject="Procurement Contract PGS-2026-SC-0047",
    )

    styles = build_styles()
    story  = []
    W      = 7.0 * inch   # usable body width

    # ════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.9*inch))

    # Decorative top bar
    story.append(HRFlowable(width=W, thickness=4, color=NAVY, spaceAfter=6))
    story.append(HRFlowable(width=W, thickness=1.5, color=GOLD, spaceAfter=20))

    story.append(Paragraph("SUPPLIER AGREEMENT", styles["cover_title"]))
    story.append(Paragraph("FOR THE SUPPLY OF GOODS AND SERVICES", styles["cover_subtitle"]))

    story.append(Spacer(1, 0.15*inch))
    story.append(HRFlowable(width=W, thickness=1, color=MID_GREY, spaceAfter=14))

    # Cover info table
    cover_data = [
        ["Contract Reference:", "PGS-2026-SC-0047"],
        ["Effective Date:", "March 1, 2026"],
        ["Expiry Date:", "February 28, 2028  (24-Month Term)"],
        ["Contracting Party (Buyer):", "Pinnacle Global Solutions LLC"],
        ["Supplier:", "ABC Supplies Inc."],
        ["Contract Currency:", "United States Dollar (USD)"],
        ["Governed by:", "Laws of the State of Illinois, USA"],
    ]
    cov_table = Table(
        [[Paragraph(r[0], ParagraphStyle("cl", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY, leading=14)),
          Paragraph(r[1], ParagraphStyle("cv", fontName="Helvetica", fontSize=10, textColor=DARK_GREY, leading=14))]
         for r in cover_data],
        colWidths=[2.5*inch, 4.5*inch]
    )
    cov_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, LIGHT_GREY]),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("LINEBELOW",    (0, 0), (-1, -1), 0.4, MID_GREY),
        ("BOX",          (0, 0), (-1, -1), 1,   NAVY),
    ]))
    story.append(cov_table)

    story.append(Spacer(1, 0.25*inch))
    story.append(HRFlowable(width=W, thickness=1, color=MID_GREY, spaceAfter=14))

    story.append(Paragraph(
        "This Agreement is entered into as of the Effective Date stated above between <b>Pinnacle Global Solutions LLC</b> "
        "(hereinafter \"<b>Buyer</b>\") and <b>ABC Supplies Inc.</b> (hereinafter \"<b>Supplier</b>\"), collectively "
        "referred to as the \"<b>Parties</b>\".",
        styles["cover_meta"]
    ))

    story.append(Spacer(1, 0.3*inch))
    story.append(HRFlowable(width=W, thickness=1.5, color=GOLD, spaceAfter=4))
    story.append(HRFlowable(width=W, thickness=4,   color=NAVY, spaceAfter=2))
    story.append(Spacer(1, 0.1*inch))

    conf_data = [[
        Paragraph("CONFIDENTIAL", ParagraphStyle("cf", fontName="Helvetica-Bold", fontSize=9, textColor=RED, alignment=TA_CENTER, leading=12)),
        Paragraph("INTERNAL USE ONLY", ParagraphStyle("iu", fontName="Helvetica-Bold", fontSize=9, textColor=NAVY, alignment=TA_CENTER, leading=12)),
        Paragraph("DO NOT DISTRIBUTE", ParagraphStyle("dn", fontName="Helvetica-Bold", fontSize=9, textColor=RED, alignment=TA_CENTER, leading=12)),
    ]]
    ct = Table(conf_data, colWidths=[W/3]*3)
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("BOX",        (0, 0), (-1, -1), 0.5, MID_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(ct)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS (simple)
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("TABLE OF CONTENTS", ParagraphStyle(
        "toc_h", fontName="Helvetica-Bold", fontSize=14, textColor=NAVY,
        alignment=TA_CENTER, spaceAfter=8, leading=18
    )))
    story.append(HRFlowable(width=W, thickness=2, color=GOLD, spaceAfter=10))

    toc_items = [
        ("Article 1",  "Definitions and Interpretation",         "3"),
        ("Article 2",  "Scope of Agreement",                     "3"),
        ("Article 3",  "Term and Renewal",                       "4"),
        ("Article 4",  "Purchase Orders and Delivery",           "4"),
        ("Article 5",  "Pricing and Currency of Transaction",    "4"),
        ("Article 6",  "Payment Terms",                          "5"),
        ("Article 7",  "Discount Terms and Early Payment Program","6"),
        ("Article 8",  "Invoicing Requirements",                 "9"),
        ("Article 9",  "Taxes and Duties",                       "9"),
        ("Article 10", "Representations and Warranties",         "10"),
        ("Article 11", "Liability and Indemnification",          "10"),
        ("Article 12", "Confidentiality",                        "11"),
        ("Article 13", "Termination",                            "11"),
        ("Article 14", "Dispute Resolution",                     "12"),
        ("Article 15", "General Provisions",                     "12"),
        ("Exhibit A",  "Approved Product and Service Schedule",  "13"),
        ("Exhibit B",  "Early Payment Discount Rate Card",       "13"),
        ("Signature",  "Execution Page",                         "14"),
    ]
    toc_style = [
        ("LINEBELOW",    (0, 0), (-1, -1), 0.3, MID_GREY),
        ("LEFTPADDING",  (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]
    toc_data = []
    for art, title, pg in toc_items:
        toc_data.append([
            Paragraph(art,   ParagraphStyle("ta", fontName="Helvetica-Bold", fontSize=9, textColor=STEEL, leading=12)),
            Paragraph(title, ParagraphStyle("tt", fontName="Helvetica",      fontSize=9, textColor=DARK_GREY, leading=12)),
            Paragraph(pg,    ParagraphStyle("tp", fontName="Helvetica",      fontSize=9, textColor=DARK_GREY, alignment=TA_RIGHT, leading=12)),
        ])
    toc_t = Table(toc_data, colWidths=[1.1*inch, 5.2*inch, 0.7*inch])
    toc_t.setStyle(TableStyle(toc_style))
    story.append(toc_t)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PREAMBLE
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>SUPPLIER AGREEMENT</b> — This Supplier Agreement (\"Agreement\") is entered into as of <b>March 1, 2026</b> "
        "(\"Effective Date\"), by and between:",
        styles["body"]
    ))

    parties_data = [
        ["BUYER", "SUPPLIER"],
        [
            "Pinnacle Global Solutions LLC\n1250 Commerce Boulevard, Suite 400\nChicago, IL 60601\nUSA\nFederal Tax ID: 36-XXXXXXX\nContact: Ms. Jennifer Hartwell\nTitle: VP of Procurement\nEmail: j.hartwell@pinnacleglobal.com\nPhone: +1 (312) 555-0192",
            "ABC Supplies Inc.\n4820 Industrial Parkway, Building C\nDetroit, MI 48201\nUSA\nFederal Tax ID: 38-XXXXXXX\nContact: Mr. David Okafor\nTitle: Director of Sales & Contracts\nEmail: d.okafor@abcsupplies.com\nPhone: +1 (313) 555-0481"
        ]
    ]
    p_t = Table(parties_data, colWidths=[W/2, W/2])
    p_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 10),
        ("ALIGN",         (0, 0), (-1, 0), "CENTER"),
        ("FONTNAME",      (0, 1), (-1, 1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, 1), 9),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GREY),
        ("LINEBELOW",     (0, 0), (-1, 0), 2, GOLD),
        ("BOX",           (0, 0), (-1, -1), 1, NAVY),
        ("BACKGROUND",    (0, 1), (-1, 1), LIGHT_GREY),
    ]))
    story.append(p_t)
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph(
        "NOW, THEREFORE, in consideration of the mutual covenants, representations, warranties, and agreements set forth "
        "herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby "
        "acknowledged, the Parties agree as follows:",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 1 — DEFINITIONS
    # ════════════════════════════════════════════════════════════════
    section_block(1, "Definitions and Interpretation", styles, story)

    defs = [
        ("<b>\"Agreement\"</b>", "means this Supplier Agreement, including all Exhibits, Schedules, and Purchase Orders incorporated herein."),
        ("<b>\"Buyer\"</b>", "means Pinnacle Global Solutions LLC and its authorized subsidiaries and affiliates."),
        ("<b>\"Supplier\"</b>", "means ABC Supplies Inc. and its permitted subcontractors."),
        ("<b>\"Goods\"</b>", "means all products, materials, components, and equipment specified in Exhibit A."),
        ("<b>\"Services\"</b>", "means maintenance, installation, technical support, and ancillary services specified in Exhibit A."),
        ("<b>\"Purchase Order\" (PO)\"</b>", "means a written or electronic order issued by Buyer specifying Goods/Services, quantity, delivery, and pricing."),
        ("<b>\"Invoice\"</b>", "means a formal billing document issued by Supplier upon delivery of Goods/Services."),
        ("<b>\"Net Invoice Amount\"</b>", "means the total invoice value after application of any volume discounts, exclusive of taxes."),
        ("<b>\"Early Payment Discount (EPD)\"</b>", "means a percentage reduction applied to the Net Invoice Amount in exchange for payment before a specified threshold date."),
        ("<b>\"Payment Due Date\"</b>", "means the date by which full payment must be received by Supplier without penalty."),
        ("<b>\"Business Day\"</b>", "means any day excluding Saturday, Sunday, and U.S. federal public holidays."),
        ("<b>\"Force Majeure\"</b>", "means any event beyond a Party's reasonable control, including natural disasters, war, pandemic, or government action."),
    ]
    for term, defn in defs:
        story.append(Paragraph(f"{term}: {defn}", styles["body_indent"]))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 2 — SCOPE
    # ════════════════════════════════════════════════════════════════
    section_block(2, "Scope of Agreement", styles, story)

    story.append(Paragraph(
        "<b>2.1 Supply Commitment.</b>  Supplier agrees to supply Buyer with Goods and Services as detailed in <b>Exhibit A</b> "
        "(Approved Product and Service Schedule) attached hereto. The scope encompasses, but is not limited to, industrial "
        "consumables, office and facility supplies, MRO (Maintenance, Repair and Operations) goods, and on-site technical "
        "services.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>2.2 Non-Exclusivity.</b>  This Agreement is non-exclusive. Buyer reserves the right to procure similar goods "
        "and services from other suppliers at its sole discretion. Supplier shall not represent Buyer as its sole or "
        "exclusive customer.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>2.3 Minimum Volume.</b>  Buyer commits to a minimum aggregate annual purchase volume of <b>USD 500,000</b> "
        "subject to Buyer's operational requirements. This commitment is indicative and shall not constitute a guarantee "
        "of orders.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>2.4 Changes to Scope.</b>  Any amendments to the scope of supply must be mutually agreed upon in writing "
        "via a formal Change Order signed by authorized representatives of both Parties.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 3 — TERM
    # ════════════════════════════════════════════════════════════════
    section_block(3, "Term and Renewal", styles, story)

    story.append(Paragraph(
        "<b>3.1 Initial Term.</b>  This Agreement shall commence on the Effective Date (<b>March 1, 2026</b>) and remain "
        "in full force for an initial period of <b>twenty-four (24) months</b>, expiring on <b>February 28, 2028</b>, "
        "unless earlier terminated in accordance with Article 13.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>3.2 Renewal.</b>  Upon expiration of the Initial Term, the Agreement shall automatically renew for successive "
        "twelve (12)-month periods unless either Party provides written notice of non-renewal at least <b>sixty (60) "
        "calendar days</b> prior to the applicable expiry date.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>3.3 Price Review at Renewal.</b>  Pricing schedules shall be reviewed no later than forty-five (45) days "
        "before each renewal. Any proposed adjustments must not exceed the U.S. Consumer Price Index (CPI) increase for "
        "the preceding year without mutual written consent.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 4 — PURCHASE ORDERS AND DELIVERY
    # ════════════════════════════════════════════════════════════════
    section_block(4, "Purchase Orders and Delivery", styles, story)

    story.append(Paragraph(
        "<b>4.1 Issuance of Purchase Orders.</b>  All orders shall be placed via written or electronic Purchase Orders "
        "(POs) issued by Buyer's Procurement Department. Verbal orders shall have no legal effect unless subsequently "
        "confirmed in writing within two (2) Business Days.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>4.2 Order Acknowledgment.</b>  Supplier shall acknowledge receipt and acceptance of each PO within "
        "<b>two (2) Business Days</b> of receipt. Failure to acknowledge within this timeframe shall be deemed acceptance.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>4.3 Delivery Terms.</b>  Unless otherwise specified in the applicable PO, all Goods shall be delivered "
        "<b>DDP (Delivered Duty Paid)</b> per Incoterms® 2020 to Buyer's designated facility. Risk of loss and title "
        "transfer to Buyer upon written acceptance.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>4.4 Lead Time.</b>  Supplier shall maintain standard lead times as agreed in Exhibit A. In the event of "
        "unavoidable delays, Supplier must notify Buyer at least <b>five (5) Business Days</b> in advance with a "
        "revised delivery schedule.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>4.5 Inspection and Rejection.</b>  Buyer reserves the right to inspect all Goods within ten (10) Business "
        "Days of delivery. Non-conforming Goods shall be returned at Supplier's cost and expense. Replacement shall be "
        "made within fifteen (15) Business Days of rejection notice.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 5 — PRICING AND CURRENCY
    # ════════════════════════════════════════════════════════════════
    section_block(5, "Pricing and Currency of Transaction", styles, story)

    story.append(Paragraph(
        "<b>5.1 Contract Currency.</b>  All prices, invoices, purchase orders, payments, credits, and financial "
        "transactions under this Agreement shall be denominated and settled exclusively in <b>United States Dollars "
        "(USD, $)</b>. No alternative currency shall be accepted without prior written amendment to this Agreement.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>5.2 Fixed Pricing Period.</b>  Unit prices set forth in Exhibit A shall remain <b>firm and fixed</b> for "
        "the first <b>twelve (12) months</b> of the Agreement (March 1, 2026 – February 28, 2027). No price escalation "
        "shall be permitted during this period.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>5.3 Price Adjustment.</b>  Following the fixed pricing period, Supplier may request a price adjustment "
        "by submitting a written proposal no later than <b>sixty (60) days</b> before the adjustment effective date. "
        "Adjustments are capped at the lesser of: (a) 3% per annum, or (b) the U.S. Bureau of Labor Statistics "
        "Producer Price Index (PPI) change for the relevant product category.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>5.4 Volume Pricing Tiers.</b>  Buyer shall benefit from the following aggregate annual spend volume tiers:",
        styles["body"]
    ))

    vol_data = [
        ["Annual Spend Tier (USD)", "Volume Discount (%)", "Effective Unit Price Reduction"],
        ["< $250,000",             "0.0%",  "Standard list price applies"],
        ["$250,000 – $499,999",    "2.5%",  "2.5% off published unit rates"],
        ["$500,000 – $999,999",    "4.0%",  "4.0% off published unit rates"],
        ["$1,000,000 – $1,999,999","6.0%",  "6.0% off published unit rates"],
        ["≥ $2,000,000",           "8.5%",  "8.5% off published unit rates"],
    ]
    highlight_table(vol_data, [2.5*inch, 1.8*inch, 2.7*inch], story)

    story.append(Paragraph(
        "<b>5.5 Pricing Disputes.</b>  Buyer may dispute any pricing on an invoice within fifteen (15) Business Days "
        "of receipt. Disputed amounts shall not be withheld in their entirety; Buyer shall pay undisputed amounts by "
        "the Payment Due Date.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>5.6 Most Favored Customer.</b>  Supplier represents that the prices offered to Buyer are no less favorable "
        "than those offered to Supplier's most preferred customer purchasing comparable goods and services in comparable "
        "quantities.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 6 — PAYMENT TERMS
    # ════════════════════════════════════════════════════════════════
    section_block(6, "Payment Terms", styles, story)

    story.append(Paragraph(
        "<b>6.1 Standard Payment Terms.</b>  Unless a Purchase Order specifies otherwise or an Early Payment Discount "
        "is exercised per Article 7, Buyer's standard payment terms are <b>Net 45 (N/45)</b> — meaning full payment "
        "of the Net Invoice Amount is due within <b>forty-five (45) calendar days</b> from the date of a valid, "
        "conforming invoice.",
        styles["body"]
    ))

    # Payment terms summary box
    pt_data = [
        ["STANDARD PAYMENT TERMS SUMMARY"],
        ["Standard Terms: Net 45 (payment due within 45 calendar days of valid invoice date)"],
        ["Currency: United States Dollar (USD) only"],
        ["Payment Method: ACH/EFT to Supplier's designated bank account (wire transfer for amounts ≥ USD 50,000)"],
        ["Invoice Submission: Via Supplier Portal (portal.pinnacleglobal.com) or email to ap@pinnacleglobal.com"],
        ["Payment Processing Day: Buyer processes payments on the 5th and 20th of each calendar month"],
        ["Banking Cutoff: Payments initiated after 3:00 PM CT on a processing day carry over to the next cycle"],
    ]
    pt_t = Table(pt_data, colWidths=[W])
    pt_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("BACKGROUND",    (0, 1), (-1, -1), LIGHT_GREY),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.5, GOLD),
        ("LINEBELOW",     (0, 1), (-1, -1), 0.4, MID_GREY),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BOX",           (0, 0), (-1, -1), 1, NAVY),
        ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
    ]))
    story.append(pt_t)
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph(
        "<b>6.2 Invoice Date.</b>  The invoice date shall be the date on which a fully compliant invoice (meeting all "
        "requirements of Article 8) is received by Buyer's Accounts Payable department. Incomplete or non-compliant "
        "invoices will be rejected and returned; the invoice date shall restart upon resubmission.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>6.3 Payment Method.</b>  All payments shall be made via <b>Automated Clearing House (ACH) / Electronic "
        "Funds Transfer (EFT)</b> to Supplier's bank account as designated in writing. Wire transfers shall be used "
        "for individual payment amounts equal to or exceeding USD 50,000. Buyer shall bear no responsibility for "
        "delays attributable to banking intermediaries.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>6.4 Late Payment.</b>  Payments not received by the Payment Due Date shall accrue interest at the rate of "
        "<b>1.5% per month</b> (18% per annum) on the outstanding balance, commencing the day after the Payment Due "
        "Date. Buyer shall have a five (5)-Business Day cure period before interest begins to accrue. Supplier must "
        "submit a separate interest invoice to collect such charges.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>6.5 Set-Off Rights.</b>  Buyer reserves the right to set off against any amount due to Supplier any "
        "amounts owed by Supplier to Buyer, including but not limited to credits, returns, penalty amounts, and "
        "warranty claims.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>6.6 Payment Disputes.</b>  In the event of a payment dispute, Buyer shall notify Supplier in writing "
        "within fifteen (15) Business Days of the invoice date. Disputed portions may be withheld pending resolution; "
        "undisputed amounts remain payable on schedule.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>6.7 Banking Information Changes.</b>  Supplier must provide at least fourteen (14) Business Days' written "
        "notice of any change to banking or payment instructions. Buyer shall not be liable for misdirected payments "
        "resulting from untimely notification.",
        styles["body"]
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 7 — DISCOUNT TERMS (MOST DETAILED)
    # ════════════════════════════════════════════════════════════════
    section_block(7, "Discount Terms and Early Payment Program", styles, story)

    story.append(Paragraph(
        "The Parties recognize the mutual financial benefit of accelerated payment cycles. Accordingly, Supplier "
        "offers, and Buyer may elect to utilize, a comprehensive structured discount program as detailed below. "
        "All discounts are applied to the <b>Net Invoice Amount</b> (after volume tier discounts per Article 5.4 "
        "and before applicable taxes).",
        styles["body"]
    ))

    # ── 7.1 Standard Volume Discounts ──
    story.append(Paragraph("7.1  Standard Volume Discounts", styles["subsection"]))
    story.append(Paragraph(
        "As set forth in Article 5.4, Buyer shall automatically receive volume-based discounts based on cumulative "
        "annual spend. These discounts are applied at the time of invoicing and reflected on the face of each invoice. "
        "Volume discounts are non-cumulative with promotional discounts unless expressly agreed in writing.",
        styles["body"]
    ))

    # ── 7.2 Trade Discounts ──
    story.append(Paragraph("7.2  Prompt Trade Discount", styles["subsection"]))
    story.append(Paragraph(
        "Buyer qualifies for a standing <b>1.0% trade discount</b> on all invoice amounts when purchase orders are "
        "issued with a minimum lead time of fifteen (15) Business Days. This discount is automatically applied by "
        "Supplier at invoice issuance and does not require separate election.",
        styles["body"]
    ))

    # ── 7.3 Early Payment Discount Program ──
    story.append(Paragraph("7.3  Early Payment Discount (EPD) Program — Detailed Terms", styles["subsection"]))

    story.append(Paragraph(
        "The <b>Early Payment Discount (EPD) Program</b> is a voluntary, invoice-level arrangement whereby Buyer may "
        "elect to pay an invoice before its standard Net 45 Payment Due Date in exchange for a predetermined percentage "
        "reduction of the Net Invoice Amount. This program is designed to improve Supplier's working capital and "
        "liquidity position while providing Buyer with a risk-free financial return on available cash.",
        styles["body"]
    ))

    story.append(Paragraph("<u>7.3.1 — How the EPD Program Works</u>", ParagraphStyle(
        "sub2", fontName="Helvetica-BoldOblique", fontSize=9.5, textColor=STEEL,
        spaceBefore=6, spaceAfter=3, leading=13
    )))
    story.append(Paragraph(
        "Upon receipt and verification of a valid, conforming invoice, Buyer's Accounts Payable system will generate "
        "an <b>Early Payment Offer Notification</b> through the Supplier Portal within two (2) Business Days. The "
        "notification will display:",
        styles["body"]
    ))
    epd_how = [
        "The full Net Invoice Amount payable under standard terms (Net 45);",
        "Available EPD tiers with corresponding payment deadlines and discounted amounts;",
        "The equivalent annualized yield for each tier, expressed as Annual Percentage Rate (APR);",
        "The final discounted amount payable by Buyer if the offer is accepted;",
        "The acceptance deadline for each tier.",
    ]
    for item in epd_how:
        story.append(Paragraph(f"• {item}", styles["bullet"]))

    story.append(Paragraph(
        "Supplier must pre-authorize all EPD tiers listed in Section 7.3.2 at the time of invoice submission "
        "by checking the applicable box(es) on the invoice cover form or within the Supplier Portal. Once "
        "pre-authorized, Buyer may elect any available tier without further approval from Supplier.",
        styles["body"]
    ))

    story.append(Paragraph("<u>7.3.2 — EPD Rate Schedule</u>", ParagraphStyle(
        "sub2b", fontName="Helvetica-BoldOblique", fontSize=9.5, textColor=STEEL,
        spaceBefore=6, spaceAfter=3, leading=13
    )))
    story.append(Paragraph(
        "The following EPD tiers are available under this Agreement. All tiers are measured from the <b>invoice "
        "receipt date</b> (as defined in Section 6.2), not the invoice date:",
        styles["body"]
    ))

    epd_table_data = [
        ["EPD Tier", "Payment Window\n(Days from Invoice Receipt)", "Discount Rate\n(% of Net Invoice)", "Example: $100,000 Invoice", "Annualized Yield\n(APR Equivalent)"],
        ["Tier 1 — Ultra Express",  "1 – 7 days",   "3.50%", "$96,500 payable\n($3,500 saved)", "~28.4% APR"],
        ["Tier 2 — Express",        "8 – 15 days",  "2.75%", "$97,250 payable\n($2,750 saved)", "~26.7% APR"],
        ["Tier 3 — Accelerated",    "16 – 20 days", "2.00%", "$98,000 payable\n($2,000 saved)", "~29.2% APR"],
        ["Tier 4 — Standard Early", "21 – 30 days", "1.50%", "$98,500 payable\n($1,500 saved)", "~27.4% APR"],
        ["Tier 5 — Net 35",         "31 – 35 days", "0.75%", "$99,250 payable\n($750 saved)",   "~27.4% APR"],
        ["No Discount (Standard)",  "36 – 45 days", "0.00%", "$100,000 payable",                 "N/A"],
    ]
    epd_widths = [1.55*inch, 1.45*inch, 1.15*inch, 1.55*inch, 1.3*inch]
    epd_t = Table(epd_table_data, colWidths=epd_widths)
    epd_style = [
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GREY),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.5, GOLD),
        ("BOX",           (0, 0), (-1, -1), 1.5, NAVY),
        # Green highlight for best tier
        ("BACKGROUND",    (0, 1), (-1, 1),  colors.HexColor("#E8F5EE")),
        ("TEXTCOLOR",     (0, 1), (0, 1),   GREEN),
        ("FONTNAME",      (0, 1), (0, 1),   "Helvetica-Bold"),
        # Grey out last row
        ("BACKGROUND",    (0, -1), (-1, -1), colors.HexColor("#F0F0F0")),
        ("TEXTCOLOR",     (0, -1), (-1, -1), colors.HexColor("#888888")),
    ]
    for r in range(2, len(epd_table_data)):
        if r % 2 == 0:
            epd_style.append(("BACKGROUND", (0, r), (-1, r), LIGHT_GREY))
    epd_t.setStyle(TableStyle(epd_style))
    story.append(epd_t)
    story.append(Spacer(1, 0.06*inch))

    story.append(Paragraph(
        "<b>APR Note:</b> The annualized yield figures above are provided for informational purposes only and represent "
        "the risk-free return equivalent Buyer obtains by leveraging available cash. Actual returns may vary based on "
        "precise payment timing within each tier window.",
        ParagraphStyle("apr_note", fontName="Helvetica-Oblique", fontSize=8.5, textColor=DARK_GREY, leading=12, spaceAfter=8)
    ))

    story.append(Paragraph("<u>7.3.3 — EPD Election and Payment Mechanics</u>", ParagraphStyle(
        "sub2c", fontName="Helvetica-BoldOblique", fontSize=9.5, textColor=STEEL,
        spaceBefore=6, spaceAfter=3, leading=13
    )))

    epd_mech = [
        ("<b>Step 1 — Invoice Receipt:</b>",
         "Buyer's AP system logs the invoice receipt date upon validation (D=0)."),
        ("<b>Step 2 — EPD Notification:</b>",
         "By D+2, an EPD Offer Notification is sent to Buyer's Treasury team listing all available tiers."),
        ("<b>Step 3 — Tier Election:</b>",
         "Buyer's Treasury or AP team selects a tier via the Supplier Portal or by emailing "
         "ap@pinnacleglobal.com with invoice number and selected tier."),
        ("<b>Step 4 — Payment Initiation:</b>",
         "Payment is initiated by Buyer via ACH/EFT on the next available payment processing date "
         "(5th or 20th of the month) within the elected tier window."),
        ("<b>Step 5 — Discount Application:</b>",
         "The elected discount percentage is deducted from the Net Invoice Amount. Buyer remits the "
         "discounted amount only. The remittance advice must clearly state the invoice number, "
         "EPD tier elected, discount amount, and net amount paid."),
        ("<b>Step 6 — Invoice Closure:</b>",
         "Upon receipt of the discounted payment within the valid tier window, Supplier marks the invoice "
         "as fully paid with no remaining balance."),
    ]
    mech_data = [[Paragraph(s, ParagraphStyle("ms", fontName="Helvetica-Bold", fontSize=9, textColor=NAVY, leading=12)),
                  Paragraph(d, ParagraphStyle("md", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=12))]
                 for s, d in epd_mech]
    mech_t = Table(mech_data, colWidths=[1.8*inch, 5.2*inch])
    mech_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_GREY),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [WHITE, LIGHT_GREY]),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.4, MID_GREY),
        ("BOX",           (0, 0), (-1, -1), 1,   NAVY),
        ("LINEBEFORE",    (1, 0), (1, -1),  0.5, MID_GREY),
    ]))
    story.append(mech_t)
    story.append(Spacer(1, 0.08*inch))

    story.append(Paragraph("<u>7.3.4 — Key EPD Conditions and Restrictions</u>", ParagraphStyle(
        "sub2d", fontName="Helvetica-BoldOblique", fontSize=9.5, textColor=STEEL,
        spaceBefore=6, spaceAfter=3, leading=13
    )))
    epd_conditions = [
        "EPD election is <b>irrevocable</b> once Buyer initiates payment. No tier change may be made after payment initiation.",
        "Payment must be <b>received</b> by Supplier's bank account (not merely initiated by Buyer) within the tier window. Buyer is advised to initiate payment at least two (2) Business Days before the tier deadline to account for banking clearance.",
        "EPD discounts are available only on invoices that are <b>undisputed</b> in their entirety. Partially disputed invoices are ineligible for EPD until the dispute is resolved.",
        "EPD discounts are calculated on the <b>Net Invoice Amount</b> (after volume discounts, before taxes). Taxes are always payable in full regardless of EPD election.",
        "EPD discounts may not be combined with any other promotional, contractual, or ad hoc discounts unless expressly authorized in writing by Supplier's Director of Sales.",
        "Buyer may elect <b>different EPD tiers for different invoices</b> within the same payment run, provided each election is documented separately.",
        "If a payment intended to capture an EPD arrives after the tier window has closed, the discount is forfeited. Supplier shall apply the payment to the standard Net Invoice Amount, and any shortfall shall be invoiced separately.",
        "Supplier guarantees availability of all five EPD tiers for the first twelve (12) months of the Agreement. Tiers may be revised upon sixty (60) days' written notice thereafter.",
        "EPD participation by Buyer is entirely voluntary and does not constitute a waiver of Buyer's right to pay under standard Net 45 terms for any or all invoices.",
    ]
    for item in epd_conditions:
        story.append(Paragraph(f"• {item}", styles["bullet"]))

    story.append(Paragraph("<u>7.3.5 — EPD Financial Example (Worked Illustration)</u>", ParagraphStyle(
        "sub2e", fontName="Helvetica-BoldOblique", fontSize=9.5, textColor=STEEL,
        spaceBefore=6, spaceAfter=3, leading=13
    )))
    story.append(Paragraph(
        "The following table illustrates the financial impact of EPD election across three hypothetical invoices:",
        styles["body"]
    ))

    ex_data = [
        ["Invoice", "Gross Amount\n(USD)", "Volume Disc.", "Net Invoice\n(USD)", "EPD Tier\nElected", "EPD Rate", "Discount\nAmount (USD)", "Amount\nPayable (USD)", "Days to Pay", "Savings\nvs. Net 45"],
        ["INV-10041", "$185,000", "2.5%", "$180,375", "Tier 2\nExpress", "2.75%", "$4,960", "$175,415", "12 days", "$4,960"],
        ["INV-10052", "$320,000", "4.0%", "$307,200", "Tier 3\nAccelerated", "2.00%", "$6,144", "$301,056", "19 days", "$6,144"],
        ["INV-10063", "$75,000",  "0.0%", "$75,000",  "Tier 5\nNet 35", "0.75%", "$563",   "$74,438", "33 days", "$563"],
        ["TOTALS",    "$580,000", "—",    "$562,575",  "—",  "—",   "$11,667", "$550,909", "—", "$11,667"],
    ]
    ex_t = Table(ex_data, colWidths=[0.72*inch, 0.75*inch, 0.62*inch, 0.72*inch, 0.65*inch, 0.55*inch, 0.75*inch, 0.78*inch, 0.6*inch, 0.56*inch])
    ex_style = [
        ("BACKGROUND",    (0, 0), (-1, 0),  STEEL),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 7.5),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 3),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 3),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GREY),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.5, GOLD),
        ("BOX",           (0, 0), (-1, -1), 1, NAVY),
        # Totals row
        ("BACKGROUND",    (0, -1), (-1, -1), NAVY),
        ("TEXTCOLOR",     (0, -1), (-1, -1), WHITE),
        ("FONTNAME",      (0, -1), (-1, -1), "Helvetica-Bold"),
        # Alternating
        ("BACKGROUND",    (0, 2), (-1, 2), LIGHT_GREY),
    ]
    ex_t.setStyle(TableStyle(ex_style))
    story.append(ex_t)
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph(
        "<b>Interpretation:</b> By electing Early Payment Discounts across these three invoices, Buyer saves "
        "<b>USD 11,667</b> against a combined Net Invoice value of USD 562,575 — representing an effective "
        "blended discount of approximately <b>2.07%</b>. Annualized across a USD 500,000 spend commitment, "
        "this program can generate estimated annual savings of <b>USD 10,350 – USD 17,500</b> for Buyer.",
        ParagraphStyle("ex_note", fontName="Helvetica-Oblique", fontSize=8.5, textColor=GREEN, leading=12, spaceAfter=8, leftIndent=4)
    ))

    story.append(Paragraph("<u>7.3.6 — Dynamic Discounting Option</u>", ParagraphStyle(
        "sub2f", fontName="Helvetica-BoldOblique", fontSize=9.5, textColor=STEEL,
        spaceBefore=6, spaceAfter=3, leading=13
    )))
    story.append(Paragraph(
        "In addition to the tiered EPD schedule, the Parties may, by mutual written consent, activate a "
        "<b>Dynamic Discounting</b> arrangement. Under Dynamic Discounting, the discount rate slides on a "
        "day-by-day linear basis between the Tier 1 rate (3.50% at Day 1) and 0.00% at Day 45, calculated "
        "using the following formula:",
        styles["body"]
    ))

    # Formula box
    formula_data = [[
        Paragraph(
            "<b>Applicable Discount Rate</b> = 3.50% × (45 − Days Since Invoice Receipt) ÷ 44",
            ParagraphStyle("formula", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
                           alignment=TA_CENTER, leading=16)
        )
    ]]
    f_t = Table(formula_data, colWidths=[W])
    f_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#EBF3FB")),
        ("BOX",           (0, 0), (-1, -1), 1.5, STEEL),
        ("LINEBELOW",     (0, 0), (-1, -1), 2, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ]))
    story.append(f_t)
    story.append(Spacer(1, 0.06*inch))
    story.append(Paragraph(
        "Dynamic Discounting requires activation through the Supplier Portal and is available only for invoices "
        "of USD 10,000 or greater. Either Party may deactivate Dynamic Discounting with fifteen (15) Business Days' "
        "written notice.",
        styles["body"]
    ))

    # ── 7.4 Seasonal/Promotional Discounts ──
    story.append(Paragraph("7.4  Seasonal and Promotional Discounts", styles["subsection"]))
    story.append(Paragraph(
        "Supplier may, at its sole discretion, offer time-limited promotional discount offers (\"Promotional Offers\") "
        "to Buyer via written notice. Promotional Offers must specify: (a) the eligible goods/services, (b) the "
        "discount rate or amount, (c) the validity period, and (d) any minimum order quantity. Promotional Offers "
        "are non-cumulative with EPD discounts unless stated otherwise.",
        styles["body"]
    ))

    # ── 7.5 Discount Summary Table ──
    story.append(Paragraph("7.5  Consolidated Discount Summary", styles["subsection"]))

    sum_data = [
        ["Discount Type", "Rate / Structure", "Auto-Applied?", "Stackable?", "Max Benefit"],
        ["Volume — Tier 1 (< $250K)",     "0.00%", "Yes", "Yes (with EPD)", "—"],
        ["Volume — Tier 2 ($250K–$499K)", "2.50%", "Yes", "Yes (with EPD)", "2.50%"],
        ["Volume — Tier 3 ($500K–$999K)", "4.00%", "Yes", "Yes (with EPD)", "4.00%"],
        ["Volume — Tier 4 ($1M–$1.99M)",  "6.00%", "Yes", "Yes (with EPD)", "6.00%"],
        ["Volume — Tier 5 (≥ $2M)",        "8.50%", "Yes", "Yes (with EPD)", "8.50%"],
        ["Prompt Trade Discount",          "1.00%", "Yes (if PO ≥ 15 BD lead)", "No", "1.00%"],
        ["EPD Tier 1 — Ultra Express",     "3.50%", "No (election)", "With Volume", "12.00%"],
        ["EPD Tier 2 — Express",           "2.75%", "No (election)", "With Volume", "11.25%"],
        ["EPD Tier 3 — Accelerated",       "2.00%", "No (election)", "With Volume", "10.50%"],
        ["EPD Tier 4 — Standard Early",    "1.50%", "No (election)", "With Volume", "10.00%"],
        ["EPD Tier 5 — Net 35",            "0.75%", "No (election)", "With Volume", "9.25%"],
        ["Dynamic Discounting",            "0–3.50% (sliding)", "No (activation)", "With Volume", "12.00%"],
        ["Promotional Offers",             "As announced", "No", "No", "Per offer"],
    ]
    sum_t = Table(sum_data, colWidths=[2.2*inch, 1.5*inch, 0.9*inch, 0.9*inch, 1.5*inch])
    sum_s = [
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GREY),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.5, GOLD),
        ("BOX",           (0, 0), (-1, -1), 1, NAVY),
        ("FONTNAME",      (0, 1), (0, -1),  "Helvetica-Bold"),
        ("TEXTCOLOR",     (0, 1), (0, -1),  NAVY),
        ("ALIGN",         (0, 1), (0, -1),  "LEFT"),
    ]
    for r in range(1, len(sum_data)):
        if r % 2 == 0:
            sum_s.append(("BACKGROUND", (0, r), (-1, r), LIGHT_GREY))
    sum_t.setStyle(TableStyle(sum_s))
    story.append(sum_t)
    story.append(Spacer(1, 0.06*inch))
    story.append(Paragraph(
        "<b>Note:</b> \"Max Benefit\" column shows the maximum combined discount achievable when Volume Tier 5 (8.50%) "
        "and EPD Tier 1 (3.50%) are stacked. Trade Discount (1.00%) does not stack with EPD. All percentages are "
        "applied sequentially, not additively, on the resulting net amount.",
        ParagraphStyle("note_s", fontName="Helvetica-Oblique", fontSize=8.5, textColor=DARK_GREY, leading=12, spaceAfter=8)
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 8 — INVOICING
    # ════════════════════════════════════════════════════════════════
    section_block(8, "Invoicing Requirements", styles, story)

    story.append(Paragraph(
        "<b>8.1 Invoice Submission.</b>  Supplier shall submit all invoices electronically via the Buyer's Supplier "
        "Portal at <b>portal.pinnacleglobal.com</b> or by email to <b>ap@pinnacleglobal.com</b>. Paper invoices "
        "shall not be accepted after June 1, 2026.",
        styles["body"]
    ))
    story.append(Paragraph("<b>8.2 Required Invoice Information.</b>  Each invoice must include:", styles["body"]))
    inv_reqs = [
        "Buyer's Purchase Order number and line item references;",
        "Supplier's name, address, and Federal Tax ID;",
        "Invoice number, invoice date, and payment due date;",
        "Itemized description of Goods/Services, quantities, unit prices, and extended amounts;",
        "Applicable volume discount tier and discounted net amount;",
        "EPD tiers pre-authorized by Supplier (if applicable);",
        "Tax amounts itemized by jurisdiction;",
        "Total amount due in USD;",
        "Supplier's bank account details (if first invoice or following a banking change);",
        "Delivery confirmation reference or Service Acceptance Certificate number.",
    ]
    for req in inv_reqs:
        story.append(Paragraph(f"({chr(96 + inv_reqs.index(req) + 1)}) {req}", styles["bullet"]))

    story.append(Paragraph(
        "<b>8.3 Invoice Disputes.</b>  Buyer shall notify Supplier of any invoice deficiencies within ten (10) "
        "Business Days of receipt. The invoice date shall restart upon submission of a corrected invoice.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>8.4 Frequency.</b>  Supplier shall submit invoices no more frequently than twice per calendar month "
        "unless otherwise agreed. Monthly consolidated invoices are encouraged for operational efficiency.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 9 — TAXES
    # ════════════════════════════════════════════════════════════════
    section_block(9, "Taxes and Duties", styles, story)

    story.append(Paragraph(
        "<b>9.1 Tax Responsibility.</b>  Buyer shall be responsible for payment of all sales tax, use tax, and "
        "VAT/GST applicable to the purchase of Goods and Services in the relevant jurisdiction, where Buyer is "
        "the taxable party. Each Party shall be solely responsible for its own income taxes.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>9.2 Exemption Certificates.</b>  Buyer shall provide valid tax exemption certificates where applicable. "
        "Supplier shall apply tax exemptions only upon receipt of valid documentation and shall not retroactively "
        "adjust previously invoiced tax amounts without written agreement.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>9.3 Import Duties.</b>  Under DDP terms (Article 4.3), all import duties, customs fees, and related "
        "charges are borne by Supplier and shall not be passed through to Buyer.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>9.4 Tax Indemnification.</b>  Each Party shall indemnify and hold harmless the other from any tax "
        "liability, penalty, or interest arising from its own tax obligations under this Agreement.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 10 — REPRESENTATIONS AND WARRANTIES
    # ════════════════════════════════════════════════════════════════
    section_block(10, "Representations and Warranties", styles, story)

    story.append(Paragraph("<b>10.1 Supplier Representations.</b>  Supplier represents and warrants that:", styles["body"]))
    sup_reps = [
        "It is duly organized, validly existing, and in good standing under the laws of the State of Michigan;",
        "All Goods delivered are new, free from defects in materials and workmanship, and conform to specifications;",
        "Goods comply with all applicable U.S. federal, state, and local laws, regulations, and safety standards;",
        "Supplier holds all necessary licenses, permits, and certifications required to supply the Goods and Services;",
        "No third-party intellectual property rights are infringed by the Goods or Services;",
        "Supplier maintains adequate product liability insurance as specified in Article 11.",
    ]
    for r in sup_reps:
        story.append(Paragraph(f"• {r}", styles["bullet"]))

    story.append(Paragraph(
        "<b>10.2 Warranty Period.</b>  Supplier warrants all Goods against defects for a period of <b>twelve (12) "
        "months</b> from the date of Buyer's acceptance. Defective Goods shall be repaired or replaced at "
        "Supplier's sole cost within fifteen (15) Business Days of written notice.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>10.3 Buyer Representations.</b>  Buyer represents that it is authorized to enter into this Agreement "
        "and that all Purchase Orders shall be issued by duly authorized personnel.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 11 — LIABILITY
    # ════════════════════════════════════════════════════════════════
    section_block(11, "Liability and Indemnification", styles, story)

    story.append(Paragraph(
        "<b>11.1 Limitation of Liability.</b>  Neither Party's total cumulative liability arising out of or related "
        "to this Agreement shall exceed the greater of: (a) <b>USD 2,000,000</b>, or (b) the total payments "
        "made by Buyer to Supplier in the <b>twelve (12) months</b> preceding the event giving rise to the claim.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>11.2 Exclusion of Consequential Damages.</b>  In no event shall either Party be liable for indirect, "
        "incidental, consequential, special, or punitive damages, including but not limited to loss of profits, "
        "business interruption, or reputational harm, regardless of cause or theory of liability.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>11.3 Indemnification by Supplier.</b>  Supplier shall indemnify, defend, and hold harmless Buyer and "
        "its affiliates, officers, and employees from and against any third-party claims arising from: (a) defective "
        "Goods; (b) Supplier's negligence or willful misconduct; (c) Supplier's breach of this Agreement; or "
        "(d) Supplier's violation of applicable laws.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>11.4 Insurance.</b>  Supplier shall maintain throughout the Term: (a) Commercial General Liability "
        "insurance of at least <b>USD 5,000,000</b> per occurrence; (b) Product Liability insurance of at least "
        "<b>USD 2,000,000</b>; (c) Workers' Compensation as required by law; and (d) Employer's Liability of "
        "at least <b>USD 1,000,000</b>. Buyer shall be named as an additional insured on policies (a) and (b).",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 12 — CONFIDENTIALITY
    # ════════════════════════════════════════════════════════════════
    section_block(12, "Confidentiality", styles, story)

    story.append(Paragraph(
        "<b>12.1 Confidential Information.</b>  Each Party (\"Receiving Party\") agrees to keep confidential all "
        "non-public information disclosed by the other Party (\"Disclosing Party\") in connection with this "
        "Agreement, including but not limited to pricing, financial data, business strategies, customer lists, "
        "and technical specifications (\"Confidential Information\").",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>12.2 Obligations.</b>  The Receiving Party shall: (a) use Confidential Information solely for purposes "
        "of this Agreement; (b) not disclose Confidential Information to third parties without prior written "
        "consent; and (c) apply at least the same degree of protection as it applies to its own confidential "
        "information, but no less than reasonable care.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>12.3 Survival.</b>  Confidentiality obligations shall survive expiration or termination of this "
        "Agreement for a period of <b>five (5) years</b>.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 13 — TERMINATION
    # ════════════════════════════════════════════════════════════════
    section_block(13, "Termination", styles, story)

    story.append(Paragraph(
        "<b>13.1 Termination for Convenience.</b>  Either Party may terminate this Agreement without cause upon "
        "<b>sixty (60) calendar days'</b> written notice to the other Party. Buyer shall pay for all Goods "
        "delivered and Services performed prior to the termination effective date.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>13.2 Termination for Cause.</b>  Either Party may terminate this Agreement immediately upon written "
        "notice if the other Party: (a) materially breaches this Agreement and fails to cure within thirty (30) "
        "days of written notice; (b) becomes insolvent or files for bankruptcy; or (c) engages in fraudulent or "
        "illegal conduct.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>13.3 Effect of Termination.</b>  Upon termination: (a) all outstanding POs not yet shipped may be "
        "cancelled by Buyer without penalty; (b) Buyer shall return or destroy Supplier's Confidential Information; "
        "(c) EPD Program elections on invoices issued before termination remain valid; and (d) payment obligations "
        "for delivered Goods and Services survive termination.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 14 — DISPUTE RESOLUTION
    # ════════════════════════════════════════════════════════════════
    section_block(14, "Dispute Resolution", styles, story)

    story.append(Paragraph(
        "<b>14.1 Informal Resolution.</b>  The Parties shall attempt in good faith to resolve any dispute arising "
        "out of or relating to this Agreement through direct negotiation between senior representatives within "
        "<b>thirty (30) days</b> of written notice of the dispute.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>14.2 Mediation.</b>  If informal resolution fails, the Parties shall submit the dispute to non-binding "
        "mediation in Chicago, Illinois, administered by the American Arbitration Association (AAA) under its "
        "Commercial Mediation Procedures.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>14.3 Arbitration.</b>  If mediation fails within sixty (60) days of appointment of a mediator, "
        "disputes shall be finally resolved by binding arbitration under the AAA Commercial Arbitration Rules. "
        "The seat of arbitration shall be Chicago, Illinois. The arbitral award shall be final and enforceable "
        "in any court of competent jurisdiction.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>14.4 Governing Law.</b>  This Agreement shall be governed by and construed in accordance with the "
        "laws of the <b>State of Illinois, USA</b>, without regard to its conflict-of-law principles.",
        styles["body"]
    ))

    # ════════════════════════════════════════════════════════════════
    # ARTICLE 15 — GENERAL PROVISIONS
    # ════════════════════════════════════════════════════════════════
    section_block(15, "General Provisions", styles, story)

    story.append(Paragraph(
        "<b>15.1 Entire Agreement.</b>  This Agreement, together with all Exhibits and incorporated Purchase Orders, "
        "constitutes the entire agreement between the Parties with respect to its subject matter and supersedes all "
        "prior negotiations, representations, and agreements.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>15.2 Amendments.</b>  No amendment to this Agreement shall be valid unless made in writing and signed "
        "by authorized representatives of both Parties.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>15.3 Assignment.</b>  Neither Party may assign this Agreement or any rights hereunder without the prior "
        "written consent of the other Party, except to an affiliate or in connection with a merger, acquisition, "
        "or sale of substantially all assets.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>15.4 Severability.</b>  If any provision of this Agreement is held invalid or unenforceable, the "
        "remaining provisions shall continue in full force and effect.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>15.5 Waiver.</b>  Failure by either Party to enforce any provision of this Agreement shall not "
        "constitute a waiver of future enforcement of that or any other provision.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>15.6 Force Majeure.</b>  Neither Party shall be liable for delays or failures in performance "
        "resulting from Force Majeure events, provided the affected Party gives prompt written notice and "
        "uses commercially reasonable efforts to mitigate the impact.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>15.7 Notices.</b>  All formal notices under this Agreement shall be in writing and delivered via "
        "(a) certified mail, return receipt requested; (b) nationally recognized overnight courier; or "
        "(c) email with read receipt, to the addresses specified on the cover page or as updated in writing.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>15.8 Counterparts.</b>  This Agreement may be executed in one or more counterparts, each of which "
        "shall be deemed an original. Electronic signatures (including DocuSign) shall be deemed valid.",
        styles["body"]
    ))
    story.append(Paragraph(
        "<b>15.9 Anti-Corruption.</b>  Each Party represents that it complies with all applicable anti-bribery "
        "and anti-corruption laws, including the U.S. Foreign Corrupt Practices Act (FCPA). Neither Party shall "
        "offer, give, or receive any improper payment or benefit in connection with this Agreement.",
        styles["body"]
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # EXHIBIT A
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("EXHIBIT A — APPROVED PRODUCT AND SERVICE SCHEDULE", ParagraphStyle(
        "ex_h", fontName="Helvetica-Bold", fontSize=13, textColor=NAVY,
        alignment=TA_CENTER, spaceAfter=6
    )))
    story.append(HRFlowable(width=W, thickness=2, color=GOLD, spaceAfter=10))

    exhibit_a = [
        ["Category", "Description", "Unit", "List Price (USD)", "Volume Tier Applies?"],
        ["Industrial Consumables", "Safety gloves, PPE kits, fasteners, lubricants", "Per Kit/Box", "$18.00 – $450.00", "Yes"],
        ["MRO Supplies", "Bearings, seals, filters, gaskets, O-rings", "Per Unit/Set", "$5.00 – $2,800.00", "Yes"],
        ["Office Supplies", "Paper, toner, binders, pens, filing systems", "Per Box/Item", "$2.00 – $85.00", "Yes"],
        ["Facility Supplies", "Cleaning agents, janitorial equipment, signage", "Per Unit/Case", "$8.00 – $620.00", "Yes"],
        ["Packaging Materials", "Corrugated boxes, stretch film, bubble wrap, tape", "Per Roll/Bundle", "$3.50 – $180.00", "Yes"],
        ["Technical Services", "On-site installation, calibration, equipment servicing", "Per Hour/Day", "$95/hr – $850/day", "No (fixed rate)"],
        ["Preventive Maintenance", "Scheduled quarterly maintenance programs", "Per Program", "$1,200 – $8,500", "No (fixed rate)"],
        ["Emergency Call-Out", "24/7 emergency repair and response", "Per Call", "$350 + parts", "No"],
    ]
    highlight_table(exhibit_a, [1.6*inch, 2.3*inch, 0.75*inch, 1.35*inch, 1.0*inch], story)

    # ════════════════════════════════════════════════════════════════
    # EXHIBIT B
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("EXHIBIT B — EARLY PAYMENT DISCOUNT RATE CARD", ParagraphStyle(
        "ex_b_h", fontName="Helvetica-Bold", fontSize=13, textColor=NAVY,
        alignment=TA_CENTER, spaceAfter=6
    )))
    story.append(HRFlowable(width=W, thickness=2, color=GOLD, spaceAfter=10))
    story.append(Paragraph(
        "This Exhibit B summarizes the official EPD Rate Card effective from the Agreement Effective Date. "
        "Rates are applicable to all invoices meeting the eligibility criteria in Article 7.3.4.",
        styles["body"]
    ))

    epd_card = [
        ["Tier", "Name", "Payment Window", "Discount", "Min. Invoice (USD)", "APR Equiv.", "Status"],
        ["1", "Ultra Express", "Days 1–7",   "3.50%", "$5,000",  "~28.4%", "ACTIVE"],
        ["2", "Express",       "Days 8–15",  "2.75%", "$5,000",  "~26.7%", "ACTIVE"],
        ["3", "Accelerated",   "Days 16–20", "2.00%", "$2,500",  "~29.2%", "ACTIVE"],
        ["4", "Standard Early","Days 21–30", "1.50%", "$2,500",  "~27.4%", "ACTIVE"],
        ["5", "Net 35",        "Days 31–35", "0.75%", "$1,000",  "~27.4%", "ACTIVE"],
        ["—", "Dynamic Disc.", "Days 1–44",  "0–3.50% (linear)", "$10,000", "Sliding", "OPT-IN"],
        ["—", "Standard N/45", "Days 36–45", "0.00%", "—",       "N/A",   "DEFAULT"],
    ]
    epd_c_t = Table(epd_card, colWidths=[0.4*inch, 1.0*inch, 1.0*inch, 0.8*inch, 1.15*inch, 0.85*inch, 0.8*inch])
    epd_c_s = [
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GREY),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.5, GOLD),
        ("BOX",           (0, 0), (-1, -1), 1.5, NAVY),
        ("TEXTCOLOR",     (6, 1), (6, 5),   GREEN),
        ("FONTNAME",      (6, 1), (6, 5),   "Helvetica-Bold"),
        ("TEXTCOLOR",     (6, 6), (6, 6),   colors.orange),
        ("TEXTCOLOR",     (6, -1), (6, -1), colors.HexColor("#888888")),
    ]
    for r in range(1, len(epd_card)):
        if r % 2 == 0:
            epd_c_s.append(("BACKGROUND", (0, r), (-1, r), LIGHT_GREY))
    epd_c_t.setStyle(TableStyle(epd_c_s))
    story.append(epd_c_t)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # SIGNATURE PAGE
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("EXECUTION PAGE", ParagraphStyle(
        "sig_h", fontName="Helvetica-Bold", fontSize=14, textColor=NAVY,
        alignment=TA_CENTER, spaceAfter=6
    )))
    story.append(HRFlowable(width=W, thickness=2, color=GOLD, spaceAfter=10))
    story.append(Paragraph(
        "IN WITNESS WHEREOF, the Parties have executed this Supplier Agreement as of the Effective Date "
        "first written above. Each signatory warrants that he or she is duly authorized to execute this "
        "Agreement on behalf of the respective Party.",
        styles["body"]
    ))
    story.append(Spacer(1, 0.2*inch))

    def sig_block(party_label, name, title, company, date_str):
        return [
            [Paragraph(party_label, ParagraphStyle("sl_h", fontName="Helvetica-Bold", fontSize=10,
                        textColor=WHITE, alignment=TA_CENTER, leading=14))],
            [Paragraph("Signature:", ParagraphStyle("sl", fontName="Helvetica-Bold", fontSize=9, textColor=NAVY, leading=13))],
            [Paragraph("_" * 40, ParagraphStyle("sl2", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=20))],
            [Paragraph(f"<b>Printed Name:</b>  {name}", ParagraphStyle("sl3", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=14))],
            [Paragraph(f"<b>Title:</b>  {title}", ParagraphStyle("sl4", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=14))],
            [Paragraph(f"<b>Company:</b>  {company}", ParagraphStyle("sl5", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=14))],
            [Paragraph(f"<b>Date:</b>  {date_str}", ParagraphStyle("sl6", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=14))],
        ]

    buyer_data  = sig_block("BUYER",    "Jennifer Hartwell", "VP of Procurement", "Pinnacle Global Solutions LLC", "March 1, 2026")
    sup_data    = sig_block("SUPPLIER", "David Okafor",      "Director of Sales & Contracts", "ABC Supplies Inc.", "March 1, 2026")

    buyer_style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",  (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GREY),
        ("LINEBELOW",  (0, 0), (-1, 0), 2, GOLD),
        ("BOX",        (0, 0), (-1, -1), 1, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING",  (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("RIGHTPADDING",(0, 0), (-1, -1), 12),
    ]

    sig_row = Table(
        [[
            Table(buyer_data, colWidths=[3.3*inch], style=TableStyle(buyer_style)),
            Spacer(0.4*inch, 1),
            Table(sup_data,   colWidths=[3.3*inch], style=TableStyle(buyer_style)),
        ]],
        colWidths=[3.3*inch, 0.4*inch, 3.3*inch]
    )
    story.append(sig_row)

    story.append(Spacer(1, 0.3*inch))
    story.append(HRFlowable(width=W, thickness=1, color=MID_GREY, spaceAfter=8))
    story.append(Paragraph(
        "<b>APPROVED BY BUYER'S LEGAL COUNSEL:</b>",
        ParagraphStyle("lc", fontName="Helvetica-Bold", fontSize=9, textColor=NAVY, leading=14)
    ))
    story.append(Spacer(1, 0.05*inch))
    legal_data = [
        [Paragraph("Signature: _____________________________", ParagraphStyle("ls", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=16)),
         Paragraph("Date: ___________________________", ParagraphStyle("ld", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=16))],
        [Paragraph("Name: ________________________________", ParagraphStyle("ln", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=16)),
         Paragraph("Title: ___________________________", ParagraphStyle("lt", fontName="Helvetica", fontSize=9, textColor=DARK_GREY, leading=16))],
    ]
    legal_t = Table(legal_data, colWidths=[W/2, W/2])
    legal_t.setStyle(TableStyle([
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    story.append(legal_t)

    story.append(Spacer(1, 0.2*inch))
    story.append(HRFlowable(width=W, thickness=1.5, color=GOLD, spaceAfter=4))
    story.append(HRFlowable(width=W, thickness=3,   color=NAVY, spaceAfter=4))
    story.append(Paragraph(
        "Contract Reference: PGS-2026-SC-0047  |  Version 1.0  |  Effective: March 1, 2026  |  "
        "Generated: February 22, 2026  |  © 2026 Pinnacle Global Solutions LLC",
        ParagraphStyle("footer_text", fontName="Helvetica", fontSize=7.5, textColor=DARK_GREY,
                       alignment=TA_CENTER, leading=11)
    ))

    # ─── Build PDF ─────────────────────────────────────────────────
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_contract()
