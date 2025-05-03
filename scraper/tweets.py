# scraper/tweets.py
import re, pandas as pd
from bs4 import BeautifulSoup

URL = "http://ec2-54-94-226-166.sa-east-1.compute.amazonaws.com:8080/tweets"

def scrape(ctx) -> pd.DataFrame:
    page     = ctx.new_page()
    resp     = page.goto(URL, wait_until="networkidle")

    if resp and resp.status >= 400:
        print(f"⚠️ /tweets devolvió {resp.status}")
    html = page.content()
    page.close()

    soup  = BeautifulSoup(html, "html.parser")
    cards = soup.select(".tweet-container-tweets")
    if not cards:
        print("⚠️ No se encontraron tweets — devuelvo DF vacío")
        return pd.DataFrame(columns=["fuente", "texto", "fecha", "polarity"])

    rows = [{
        "fuente": c.select_one(".twitter-handle").text.strip("@"),
        "texto" : c.select_one(".tweet-tweets p").text.strip(),
        "fecha" : c.select_one(".time-and-date-tweets p").text.strip()
    } for c in cards]

    df = pd.DataFrame(rows)

    # muy rudimentario: +1 si ve palabras “positivas”, −1 si “negativas”, 0 resto
    df["polarity"] = df["texto"].apply(
        lambda t:  1 if re.search(r"\b(baja|mejora|desacelera)\b", t, re.I)
        else -1 if re.search(r"\b(alza|crisis|inflación)\b", t, re.I)
        else 0
    )
    return df