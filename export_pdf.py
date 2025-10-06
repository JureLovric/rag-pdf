from reportlab.lib.pagesizes import A4
elif ln.strip() == "":
flow.append(Spacer(1, 6))
else:
flow.append(Paragraph(ln, BASE_STYLE))
return flow




def _add_page_number(canvas: _canvas.Canvas, doc):
page_num = canvas.getPageNumber()
text = f"{page_num}"
canvas.setFont("Helvetica", 10)
# fixed margins: 2cm; place number at bottom-right margin line
canvas.drawRightString(A4[0] - 2*cm, 1.5*cm, text)




def render_pdf(md: str, out_path: str, title: str = "RAG Output") -> str:
doc = SimpleDocTemplate(
out_path,
pagesize=A4,
rightMargin=2*cm,
leftMargin=2*cm,
topMargin=2*cm,
bottomMargin=2*cm,
title=title,
)
flow = md_to_flowables(md)
doc.build(flow, onFirstPage=_add_page_number, onLaterPages=_add_page_number)
return out_path
