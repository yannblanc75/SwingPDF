# services.py
import os
import re
import datetime
from typing import Optional
from weasyprint import HTML

# --- Partie Playwright (HTML/URL -> PDF navigateur) ---
import asyncio
from playwright.async_api import async_playwright  # type: ignore


class PdfService:
    @staticmethod
    def render_html_to_pdf(html: str) -> bytes:
        """WeasyPrint (pour tes modèles HTML -> PDF)."""
        return HTML(string=html).write_pdf()

    @staticmethod
    def _chromium_launch_args() -> list[str]:
        """
        Args utiles pour WSL/Docker/CI:
        - no-sandbox : sandbox souvent indisponible
        - disable-dev-shm-usage : évite /dev/shm trop petit en conteneur
        - font rendering plus stable
        """
        return [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--font-render-hinting=none",
        ]

    @staticmethod
    def render_url_to_pdf(url: str, *, wait_until: str = "load") -> bytes:
        """
        Rendu d'une page web distante en PDF via Playwright/Chromium.
        - nécessite `playwright` + `playwright install chromium` + deps systèmes.
        - lève une exception en cas d'erreur.
        """

        async def _run(u: str) -> bytes:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True, args=PdfService._chromium_launch_args()
                )
                try:
                    context = await browser.new_context(locale="fr-FR")
                    page = await context.new_page()
                    # Temps d'attente plus large pour les pages lourdes
                    await page.goto(u, wait_until=wait_until, timeout=90_000)
                    # Ajuste le format/marges au besoin
                    pdf = await page.pdf(format="A4", print_background=True, margin={"top": "15mm", "bottom": "15mm", "left": "12mm", "right": "12mm"})
                    await context.close()
                    return pdf
                finally:
                    await browser.close()

        return asyncio.run(_run(url))


class StorageService:
    @staticmethod
    def make_slug(text: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9_-]", "", text.replace(" ", "_"))
        return slug[:40]

    @staticmethod
    def unique_filename(titre: str) -> str:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = StorageService.make_slug(titre)
        return f"{now}_{slug}.pdf"

    @staticmethod
    def save_pdf(pdf_bytes: bytes, filename: str, folder: str) -> str:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        with open(path, "wb") as f:
            f.write(pdf_bytes)
        return path
