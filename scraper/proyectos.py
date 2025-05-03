# scraper/proyectos.py
import re
import pandas as pd
from scraper.browser import BASE          # lo tienes en browser.py

URL = f"{BASE}/proyectos"


def _camel_to_snake(name: str) -> str:
    """
    Convierte camelCase → snake_case   (proyectoID → proyecto_id, etc.)
    """
    name = re.sub(r'ID$', '_id', name)           # …ID  → …_id  (caso especial)
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name) # camel → snake
    return name.lower()


def scrape(ctx) -> pd.DataFrame:
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")

    page.wait_for_function(
        "typeof lista_proyectos_periodo !== 'undefined' && "
        "lista_proyectos_periodo.length > 0",
        timeout=60_000          # 60 s para más margen
    )

    # array JS → lista de dicts Python
    projects = page.evaluate("lista_proyectos_periodo")
    page.close()

    df = pd.DataFrame(projects)

    # nombres de columnas legibles
    df = df.rename(columns=_camel_to_snake)

    # claves que nos interesa tener con nombre “bonito”
    df = df.rename(columns={
        "proyecto_id":              "proyecto_id",
        "periodoxparticipante":     "periodo_x_participante",
        "periodostrabajados":       "periodos_trabajados",
    })

    # eliminar duplicados
    if "proyecto_id" in df.columns:
        df = df.drop_duplicates(subset=["proyecto_id"])

    # numeric clean‑up
    num_cols = [
        "precio_min", "precio_max", "paga", "monto_oferta", "monto_final",
        "precio_medio", "precio_hora_est", "hs_trabajo"
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[^\d\.]", "", regex=True)
                .replace("", "0")
                .astype(float)
            )

    return df