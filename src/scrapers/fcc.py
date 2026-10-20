from typing import List, Dict, Any
from src.scrapers.base import BaseScraper

class FCCScraper(BaseScraper):
    def extrair(self, regiao_url: str = "nordeste") -> List[Dict[str, Any]]:
        url = "https://www.concursosfcc.com.br/"
        soup = self.fetch_soup(url, encoding='iso-8859-1')
        if not soup:
            return []

        dados = []
        for tag_a in soup.find_all("a", class_="textoPreto", href=True):
            titulo = tag_a.get_text(separator=" ", strip=True)
            if not titulo:
                continue
                
            tag_span = tag_a.find_next_sibling("span", class_="textocinza")
            detalhes = tag_span.get_text(separator=" ", strip=True) if tag_span else ""
            
            if detalhes and detalhes not in titulo:
                titulo_completo = f"{titulo} - {detalhes}"
            else:
                titulo_completo = titulo

            link = tag_a["href"]
            if link.startswith("http"):
                link_completo = link
            else:
                link_completo = f"https://www.concursosfcc.com.br{link}" if link.startswith("/") else f"https://www.concursosfcc.com.br/{link}"
            
            dados.append({
                "titulo": titulo_completo,
                "status": "Inscrições Abertas",
                "link": link_completo,
                "fonte": "FCC"
            })
        return dados