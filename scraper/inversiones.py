# scraper/inversiones.py
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

# Reutilizamos la constante BASE ya definida en scraper.browser
from scraper.browser import BASE

#  ID del <table> en el HTML  →  nombre de worksheet en Google Sheets
TABLES = {
    "tabla_rrhh":          "Inversiones_RRHH",
    "tabla_marketing":     "Inversiones_Marketing",
    "tabla_desarrollo":    "Inversiones_Desarrollo",
    "tabla_capacitaciones":"Inversiones_Capacitaciones",
}

URL = f"{BASE}/inversiones"               # ← URL absoluta ✔


def _grab_table_html(page, table_id: str) -> str:
    """
    Espera a que DataTables inserte filas en <tbody> y devuelve
    el outerHTML de la tabla ya completa.
    """
    # DataTables agrega un <tr class="odd|even"> cuando carga datos
    page.wait_for_selector(f"#{table_id} tbody tr:not(.dataTables_empty)")
    return page.eval_on_selector(f"#{table_id}", "el => el.outerHTML")


def scrape(ctx) -> dict[str, pd.DataFrame]:
    """
    Devuelve un dict  {nombre_worksheet: DataFrame}
    """
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")

    dataframes: dict[str, pd.DataFrame] = {}

    for table_id, sheet_name in TABLES.items():
        html = _grab_table_html(page, table_id)

        # ── parseo sin "flavor" para que use lxml y evitar el bug de BS4 4.12 ──
        df = pd.read_html(StringIO(html))[0]

        # Columnas en minúsculas, sin espacios "raros"
        df.columns = [c.strip().lower() for c in df.columns]

        # Quitamos la col. 'contratar' (sólo tiene botones)
        df = df.drop(columns=[c for c in df.columns if c.startswith("contratar")])

        # Deduplicar por PK si está presente
        if "inversion_participante_id" in df.columns:
            df = df.drop_duplicates(subset=["inversion_participante_id"])

        dataframes[sheet_name] = df

    page.close()
    return dataframes