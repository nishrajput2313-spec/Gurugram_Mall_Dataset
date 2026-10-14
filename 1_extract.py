import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_shopping_malls_in_India"
HEADERS = {"User-Agent": "StudentProject/1.0 (learning project)"}
KEYWORDS = ("gurgaon", "gurugram")

html = requests.get(URL, headers=HEADERS, timeout=30).text
rows = []

try:
    for t in pd.read_html(StringIO(html)):
        t = t.astype(object)
        mask = t.apply(lambda r: any(k in " ".join(map(str, r)).lower() for k in KEYWORDS), axis=1)
        for _, r in t[mask].iterrows():
            rows.append({"name": str(r.iloc[0]), "details": " | ".join(map(str, r.values)), "source": "table"})
except ValueError:
    print("No tables found on the page")

# Part B: look at bullet-list items under a Gurgaon heading, or mentioning Gurgaon
soup = BeautifulSoup(html, "lxml")
section = ""
for el in soup.select("div.mw-parser-output")[0].find_all(["h2", "h3", "h4", "li"]):
    if el.name in ("h2", "h3", "h4"):
        section = el.get_text(strip=True).replace("[edit]", "")
    else:
        if (el.get("id") or "").startswith("cite_note"):
            continue
        text = el.get_text(" ", strip=True)
        if any(k in (text + " " + section).lower() for k in KEYWORDS):
            rows.append({"name": text.split(" - ")[0].split(",")[0],
                         "details": text, "source": "list"})

pd.DataFrame(rows).to_csv("raw_data.csv", index=False)
print("Rows collected:", len(rows))