# scraper/sheets.py
"""
Utilidades mínimas para volcar un DataFrame a Google Sheets **sin** dar formato.
Requiere:
    pip install gspread gspread-dataframe google-auth
y la credencial del service‑account en una variable de entorno:
    GOOGLE_SERVICE_ACCOUNT_JSON=/ruta/credenciales.json
"""

import os
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from dotenv import load_dotenv

load_dotenv()

# ── credenciales ───────────────────────────────────────────────────────
CREDS_JSON     = os.getenv("GOOGLE_CREDS_JSON")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID") or "1-jaTeMIjrlsoIfTUBGZhT88D0lssWez256S8YM5ae7o"

gc = gspread.service_account(filename=CREDS_JSON)

# ── API sencilla ───────────────────────────────────────────────────────
def write_df(sheet_name: str, df: pd.DataFrame):
    """Sobrescribe *sheet_name* con el contenido de *df* (incluye encabezados)."""
    sh = gc.open_by_key(SPREADSHEET_ID)

    # crea la hoja si no existe
    try:
        ws = sh.worksheet(sheet_name)
        ws.clear()
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=sheet_name, rows="1", cols="1")

    if df.empty:
        print(f"⚠️  {sheet_name}: DataFrame vacío — no se actualiza.")
        return

    set_with_dataframe(
        ws, df,
        include_index=False,
        include_column_header=True,
        resize=True        # ajusta filas/columnas a la forma del DF
    )

    print(f"✅  {sheet_name}: {len(df)} filas cargadas.")
