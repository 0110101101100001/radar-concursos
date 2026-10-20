from typing import List, Dict, Any
from src.scrapers.base import BaseScraper

class CebraspeScraper(BaseScraper):
    def extrair(self, regiao_url: str = "nordeste") -> List[Dict[str, Any]]:
        url = "https://www.cebraspe.org.br/concursos/inscricoes-abertas/"
        soup = self.fetch_soup(url, encoding='utf-8')
        if not soup:
            return []

        dados = []
        for card in soup.find_all("li", class_="q_circle_outer"):
            try:
                tag_titulo = card.find("h3", class_="q_circle_title")
                tag_a = card.find("a", class_="icon_with_title_link")
                
                if not tag_titulo or not tag_a or not tag_a.has_attr("href"):
                    continue

                titulo = tag_titulo.get_text(strip=True)
                link = tag_a["href"]
                link_completo = link if link.startswith("http") else f"https://www.cebraspe.org.br{link}"

                dados.append({
                    "titulo": titulo,
                    "status": "Inscrições Abertas",
                    "link": link_completo,
                    "fonte": "Cebraspe"
                })
            except Exception:
                continue
        return dados