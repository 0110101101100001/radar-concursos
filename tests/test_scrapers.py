import os
import pytest
from bs4 import BeautifulSoup
from src.scrapers.pci import PCIScraper
from src.scrapers.cebraspe import CebraspeScraper
from src.scrapers.ibfc import IBFCScraper

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture
def pci_html():
    with open(os.path.join(FIXTURES_DIR, "pci_nordeste.html"), "r", encoding="utf-8") as f:
        return f.read()

def test_pci_parser(mocker, pci_html):
    mocker.patch.object(PCIScraper, "fetch_soup", return_value=BeautifulSoup(pci_html, "html.parser"))
    scraper = PCIScraper()
    resultados = scraper.extrair("nordeste")
    assert len(resultados) > 0
    assert "titulo" in resultados[0]
    assert "link" in resultados[0]