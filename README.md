# Mengho Scraper ↔ Google Sheets

Automatiza la extracción diaria de datos de tu partida *Mengho* y los actualiza en una hoja de Google Sheets con un formato legible.

---

## 📦 Estructura del proyecto

```
.
├── main.py                # punto de entrada
├── .env                   # variables de entorno (no se sube al repo)
├── creds.json             # credenciales de la Service‑Account de Google
└── scraper/
    ├── browser.py         # login + contexto Playwright
    ├── sheets.py          # helpers para Google Sheets
    ├── tweets.py          # /tweets
    ├── proyectos.py       # /proyectos
    ├── inversiones.py     # /inversiones  (4 tablas)
    ├── empleados.py       # /empleados    (4 tablas)
    └── decisiones.py      # /decisiones   (stats empresa)
```

---

## 🚀 Instalación rápida

```bash
# 1) clona el repo
$ git clone https://github.com/tu‑usuario/mengho-scraper.git
$ cd mengho-scraper

# 2) crea un entorno virtual
$ python -m venv venv && source venv/bin/activate

# 3) instala dependencias
$ pip install -r requirements.txt

# 4) instala navegadores para Playwright
$ playwright install chromium
```

### Variables de entorno (`.env`)

```dotenv
SIMU_USER=TuUsuario
SIMU_PASS=TuPassword
SPREADSHEET_ID=1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_CREDS_JSON=./creds.json
```

* `SIMU_*` → credenciales del sitio Mengho.
* `SPREADSHEET_ID` → ID que aparece en la URL de tu hoja.
* `GOOGLE_CREDS_JSON` → ruta al **JSON** de la *Service Account* con acceso de edición a esa hoja.

> **Tip:** comparte la hoja con el e‑mail que figura dentro de `creds.json` (campo `client_email`).

---

## ▶️ Ejecutar

```bash
$ python main.py
```

Al finalizar verás algo como:

```
✅ Login OK → llegó a /misPartidas
✅ Partida activa → …/partida?partida_id=1486
✅ Tweets enviados a Sheets ➜ pestaña Tweets
✅ Empleados actualizados     ➜ Empleados, Talentos, Beneficios, Equipos
✅ Inversiones actualizadas   ➜ Inversiones_* (4 pestañas)
✅ Proyectos actualizados     ➜ Proyectos
✅ Stats actualizados         ➜ Stats
Todo OK ✅
```

Cada scraper deja su DataFrame en la pestaña homónima.
Si la pestaña no existe, `sheets.write_df()` la crea.
