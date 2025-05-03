# main.py
from scraper.browser import get_context
from scraper import tweets, sheets

# si luego agregas más sub‑scrapers (proyectos, inversiones, etc.)
# simplemente:
from scraper import proyectos, inversiones, empleados, decisiones


def run():
    with get_context() as ctx:
        # ── 1) Tweets ────────────────────────────────────────────────
        sheets.write_df("Tweets", tweets.scrape(ctx))

        # ── 2) Otros módulos (actívalos si los tienes) ───────────────
        sheets.write_df("Proyectos", proyectos.scrape(ctx))
        for ws_name, df in inversiones.scrape(ctx).items():
            sheets.write_df(ws_name, df)
        for ws_name, df in empleados.scrape(ctx).items():
            sheets.write_df(ws_name, df)
        sheets.write_df("Decisiones", decisiones.scrape(ctx))


if __name__ == "__main__":
    run()
