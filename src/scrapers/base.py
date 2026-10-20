import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BaseScraper:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = self._criar_sessao()

    def _criar_sessao(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        return session

    def fetch_soup(self, url: str, encoding: Optional[str] = None) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code != 200:
                logging.warning(f"HTTP {response.status_code}: {url}")
                return None
            if encoding:
                response.encoding = encoding
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logging.error(f"Erro ao acessar {url}: {e}")
            return None

    def extrair(self, **kwargs) -> List[Dict[str, Any]]:
        raise NotImplementedError