# scraper/browser.py
import os, re, contextlib
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

BASE   = "http://ec2-54-94-226-166.sa-east-1.compute.amazonaws.com:8080"
LOGIN  = f"{BASE}/login"

@contextlib.contextmanager
def get_context():
    pw      = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)     # headless=False para debug visual
    ctx     = browser.new_context()
    page    = ctx.new_page()

    # 1) LOGIN --------------------------------------------------------
    page.goto(LOGIN)
    page.fill("#emailONombreUsuario", os.getenv("SIMU_USER"))
    page.fill("#password",            os.getenv("SIMU_PASS"))

    with page.expect_navigation(url=re.compile(r".*/misPartidas.*")):
        page.click("#btn_logear_usuario")

    print("✅ Login OK → llegó a /misPartidas")

    # 2) Click en “Entrar” (primera partida) --------------------------
    page.wait_for_selector("#tabla_partidas tbody tr", timeout=15_000)
    fila       = page.locator("#tabla_partidas tbody tr").first
    btn_entrar = fila.locator("text=Entrar")

    with page.expect_navigation(url=re.compile(r".*/partida\?partida_id=\d+")):
        btn_entrar.click()

    print("✅ Partida activa →", page.url)

    # 3) Contexto listo ----------------------------------------------
    yield ctx      # los scrapers abrirán pestañas nuevas reutilizando la sesión

    browser.close()
    pw.stop()