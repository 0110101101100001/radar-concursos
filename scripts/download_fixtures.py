import os
import requests

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "tests", "fixtures")
os.makedirs(FIXTURES_DIR, exist_ok=True)

SITES = {
    "pci_nordeste.html": "https://www.pciconcursos.com.br/concursos/nordeste/",
    "ibfc.html": "https://ibfc.selecao.net.br/index/abertos/",
    "cebraspe.html": "https://www.cebraspe.org.br/concursos/"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def baixar():
    for filename, url in SITES.items():
        filepath = os.path.join(FIXTURES_DIR, filename)
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            res.encoding = "ISO-8859-1" if "ibfc" in url else "utf-8"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(res.text)
        except Exception as e:
            print(f"Erro em {url}: {e}")

if __name__ == "__main__":
    baixar()