from typing import List, Dict, Any
from src.scrapers.base import BaseScraper

class IBFCScraper(BaseScraper):
    def extrair(self, regiao_url: str = "nordeste") -> List[Dict[str, Any]]:
        url = "https://ibfc.selecao.net.br/index/abertos/"
        soup = self.fetch_soup(url, encoding='ISO-8859-1')
        if not soup:
            return []

        dados = []
        for link_tag in soup.find_all("a", class_="lista-concurso"):
            try:
                if not link_tag.has_attr("href"): continue
                
                titulo_limpo = " ".join(link_tag.text.split())
                link_completo = f"https://ibfc.selecao.net.br{link_tag['href']}"

                div_pai = link_tag.parent
                status_tag = div_pai.find("span", class_="inscricoesabertas") if div_pai else None
                status = status_tag.text.strip() if status_tag else "Status desconhecido"

                dados.append({
                    "titulo": titulo_limpo,
                    "status": status,
                    "link": link_completo,
                    "fonte": "IBFC"
                })
            except Exception:
                continue
        return dados