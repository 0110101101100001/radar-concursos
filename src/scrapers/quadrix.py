from typing import List, Dict, Any
from src.scrapers.base import BaseScraper

class QuadrixScraper(BaseScraper):
    def extrair(self) -> List[Dict[str, Any]]:
        url = "https://www.quadrix.org.br/index/abertos/"
        soup = self.fetch_soup(url, encoding='iso-8859-1')
        if not soup:
            return []

        dados = []
        for h3 in soup.find_all("h3"):
            tag_a = h3.find("a", href=True)
            if not tag_a:
                continue
            
            titulo = tag_a.get_text(strip=True)
            if not titulo:
                continue
                
            link = tag_a["href"]
            link_completo = link if link.startswith("http") else f"https://www.quadrix.org.br{link}"
            
            dados.append({
                "titulo": titulo,
                "status": "Inscrições Abertas",
                "link": link_completo,
                "fonte": "Quadrix"
            })
        return dados