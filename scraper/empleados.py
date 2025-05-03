# scraper/empleados.py
import pandas as pd
from bs4 import BeautifulSoup

from scraper.browser import BASE

URL = f"{BASE}/empleados"                 # ← URL absoluta ✔


def _table_to_df(table):
    """Convierte un <table> (BeautifulSoup) en DataFrame limpio."""
    if table is None:
        return pd.DataFrame()

    head = [th.text.strip() for th in table.select("thead th")]
    rows = [
        [td.text.strip() for td in tr.select("td")]
        for tr in table.select("tbody tr")
    ]
    return pd.DataFrame(rows, columns=head)


def scrape(ctx) -> dict[str, pd.DataFrame]:
    """
    Devuelve:
        {
          "Empleados":  df_empleados,
          "Talentos":   df_talentos,
          "Beneficios": df_beneficios,
          "Equipos":    df_equipos,
        }
    """
    page = ctx.new_page()
    response = page.goto(URL, wait_until="networkidle")

    if response and response.status >= 400:
        print(f"⚠️  /empleados devolvió {response.status}")

    soup = BeautifulSoup(page.content(), "html.parser")
    page.close()

    return {
        "Empleados":  _table_to_df(soup.select_one("#tabla_empleados")),
        "Talentos":   _table_to_df(soup.select_one("#tabla_empleados_posibles")),
        "Beneficios": _table_to_df(soup.select_one("#tabla_beneficios")),
        "Equipos":    _table_to_df(soup.select_one("#tabla_equipamiento")),
    }