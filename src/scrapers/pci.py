from typing import List, Dict, Any
from src.scrapers.base import BaseScraper

class PCIScraper(BaseScraper):
    def extrair(self, regiao_url: str = "nordeste") -> List[Dict[str, Any]]:
        url = f"https://www.pciconcursos.com.br/concursos/{regiao_url}/"
        soup = self.fetch_soup(url, encoding='utf-8')
        if not soup:
            return []

        dados = []
        for div_concurso in soup.find_all("div", class_="na"):
            try:
                tag_ca = div_concurso.find("div", class_="ca")
                if not tag_ca: continue
                
                tag_a = tag_ca.find("a")
                if not tag_a or not tag_a.has_attr("href"): continue

                link = tag_a["href"]
                titulo_principal = tag_a.get("title", tag_a.text.strip())
                
                estado_tag = div_concurso.find("div", class_="cc")
                estado = estado_tag.text.strip() if estado_tag else ""
                
                vagas_tag = div_concurso.find("div", class_="cd")
                vagas = vagas_tag.get_text(separator=" | ", strip=True) if vagas_tag else ""
                
                prazo_tag = div_concurso.find("div", class_="ce")
                prazo = prazo_tag.get_text(separator=" ", strip=True) if prazo_tag else "Sem data"

                titulo_completo = f"{titulo_principal} [{estado}] - {vagas}"
                link_completo = link if link.startswith("http") else f"https://www.pciconcursos.com.br{link}"

                dados.append({
                    "titulo": " ".join(titulo_completo.split()),
                    "status": prazo,
                    "link": link_completo,
                    "fonte": "PCI"
                })
            except Exception:
                continue
        return dados