# test_pdf_service.py
import pytest
from html2pdf.blueprints.main.services import PdfService

def test_render_html_to_pdf():
    html = "<h1>Test PDF</h1><p>Contenu</p>"
    pdf_bytes = PdfService.render_html_to_pdf(html)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 100
    assert pdf_bytes.startswith(b'%PDF')
