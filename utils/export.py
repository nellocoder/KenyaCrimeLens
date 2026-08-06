"""Export helpers for Kenya CrimeLens: CSV, styled Excel and a PDF briefing."""

from __future__ import annotations

import re
from datetime import datetime
from io import BytesIO

import pandas as pd

from utils import config as C

try:
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                    TableStyle)
    HAS_REPORTLAB = True
except ImportError:  # pragma: no cover - optional dependency
    HAS_REPORTLAB = False


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """UTF-8 CSV export of the given table."""
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Incidents") -> bytes:
    """Styled Excel export: branded header row, frozen pane, auto column widths."""
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter",
                        datetime_format="yyyy-mm-dd") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        book, sheet = writer.book, writer.sheets[sheet_name]
        header_fmt = book.add_format({
            "bold": True, "font_color": "#ffffff", "bg_color": C.KENYA_GREEN,
            "border": 1, "border_color": "#e2e8f0",
        })
        for col_idx, name in enumerate(df.columns):
            sheet.write(0, col_idx, name, header_fmt)
            sample = df[name].astype(str).str.len()
            width = min(max(int(sample.quantile(0.9)) if len(sample) else 10,
                            len(name)) + 2, 60)
            sheet.set_column(col_idx, col_idx, width)
        sheet.freeze_panes(1, 0)
        sheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    return buf.getvalue()


def _strip_tags(text_html: str) -> str:
    return re.sub(r"<[^>]+>", "", text_html)


def to_pdf_bytes(title: str, summary_html: str, kpi_cards: list[dict],
                 scoreboard: pd.DataFrame | None = None) -> bytes | None:
    """One-page PDF briefing: title, KPI table, narrative, county scoreboard.

    Returns None when reportlab is not installed.
    """
    if not HAS_REPORTLAB:
        return None

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm,
                            rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm, title=title)
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Title"], fontSize=18,
                        textColor=rl_colors.HexColor(C.INK), spaceAfter=2)
    small = ParagraphStyle("Small", parent=styles["Normal"], fontSize=8,
                           textColor=rl_colors.HexColor(C.MUTED))
    body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10,
                          leading=15)

    story = [
        Paragraph(f"{C.APP_NAME} · {title}", h1),
        Paragraph(f"Generated {datetime.now():%Y-%m-%d %H:%M} · {C.DATA_DISCLAIMER}",
                  small),
        Spacer(1, 8),
    ]

    kpi_rows = [[c["label"] for c in kpi_cards],
                [str(c["value"]) for c in kpi_cards],
                [str(c.get("sub", "")) for c in kpi_cards]]
    kpi_tbl = Table(kpi_rows, hAlign="LEFT")
    kpi_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), rl_colors.HexColor(C.KENYA_GREEN)),
        ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTSIZE", (0, 1), (-1, 1), 12),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 2), (-1, 2), 7),
        ("TEXTCOLOR", (0, 2), (-1, 2), rl_colors.HexColor(C.MUTED)),
        ("GRID", (0, 0), (-1, -1), 0.4, rl_colors.HexColor("#e2e8f0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story += [kpi_tbl, Spacer(1, 10),
              Paragraph("<b>Analysis summary</b>", body),
              Paragraph(_strip_tags(summary_html), body), Spacer(1, 10)]

    if scoreboard is not None and not scoreboard.empty:
        top = scoreboard.head(15)
        data = [list(top.columns)] + top.astype(str).values.tolist()
        tbl = Table(data, hAlign="LEFT", repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), rl_colors.HexColor(C.INK)),
            ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.3, rl_colors.HexColor("#e2e8f0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [rl_colors.white, rl_colors.HexColor("#f8fafc")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story += [Paragraph("<b>County scoreboard (top 15)</b>", body),
                  Spacer(1, 4), tbl]

    doc.build(story)
    return buf.getvalue()
