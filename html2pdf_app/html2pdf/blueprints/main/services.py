# services.py
import os
import re
import datetime
from typing import Optional
from weasyprint import HTML

class PdfService:
    @staticmethod
    def render_html_to_pdf(html: str) -> bytes:
        pdf_bytes = HTML(string=html).write_pdf()
        return pdf_bytes

class StorageService:
    @staticmethod
    def make_slug(text: str) -> str:
        slug = re.sub(r'[^a-zA-Z0-9_-]', '', text.replace(' ', '_'))
        return slug[:40]

    @staticmethod
    def unique_filename(titre: str) -> str:
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        slug = StorageService.make_slug(titre)
        return f"{now}_{slug}.pdf"

    @staticmethod
    def save_pdf(pdf_bytes: bytes, filename: str, folder: str) -> str:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        with open(path, 'wb') as f:
            f.write(pdf_bytes)
        return path
