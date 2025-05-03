# scraper/decisiones.py
import re
import pandas as pd
from bs4 import BeautifulSoup
from scraper.browser import BASE

URL = f"{BASE}/decisiones"


def _num(s: str) -> int:
    """Convierte '27,183' → 27183 (o 0 si la cadena está vacía)."""
    if not s:
        return 0
    s = s.replace(".", "").replace(",", "")
    return int(float(s))


def scrape(ctx) -> pd.DataFrame:
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")
    html = page.content()
    page.close()

    soup  = BeautifulSoup(html, "html.parser")
    texto = soup.get_text(" ", strip=True)

    # ── salarios propuestos ────────────────────────────────────────────
    salario_jr  = _num(soup.select_one("#salario_jr")["value"])
    salario_ssr = _num(soup.select_one("#salario_ssr")["value"])
    salario_sr  = _num(soup.select_one("#salario_sr")["value"])

    # ── fondos disponibles ─────────────────────────────────────────────
    m = re.search(r"Fondos Disponibles:\s*\$([\d\.,]+)", texto)
    fondos = _num(m.group(1)) if m else 0

    # ── horas ──────────────────────────────────────────────────────────
    m = re.search(r"Horas Disponibles:\s*([\d\.,]+)", texto)
    horas_disp = _num(m.group(1)) if m else 0

    m = re.search(r"Horas Comprometidas:\s*([\d\.,]+)", texto)
    horas_comp = _num(m.group(1)) if m else 0

    m = re.search(r"Carga\s+Horaria\s+(\d+)%", texto)
    carga_pct = int(m.group(1)) if m else 0

    # ── DataFrame final ────────────────────────────────────────────────
    df = pd.DataFrame([{
        "salario_jr"       : salario_jr,
        "salario_ssr"      : salario_ssr,
        "salario_sr"       : salario_sr,
        "fondos_disponibles": fondos,
        "horas_disponibles": horas_disp,
        "horas_comprometidas": horas_comp,
        "carga_horaria_pct": carga_pct,
    }])

    return df