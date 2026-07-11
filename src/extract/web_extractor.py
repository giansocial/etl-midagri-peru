from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.extract.base_extractor import BaseExtractor
from src.config.settings import REQUESTS_TIMEOUT, USER_AGENT


class WebExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("web")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def extract(
        self,
        url: str,
        table_index: int = 0,
        attrs: Optional[dict] = None,
    ) -> pd.DataFrame:
        self.logger.info(f"Extrayendo tabla HTML: {url}")

        try:
            response = self.session.get(url, timeout=REQUESTS_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error(f"Error al acceder a {url}: {e}")
            return pd.DataFrame()

        tables = pd.read_html(
            response.text,
            attrs=attrs,
            encoding="utf-8",
        )

        if not tables:
            self.logger.warning("No se encontraron tablas en la pagina")
            return pd.DataFrame()

        if table_index >= len(tables):
            self.logger.warning(
                f"Indice {table_index} fuera de rango. "
                f"Se encontraron {len(tables)} tablas"
            )
            table_index = 0

        df = tables[table_index]
        self.validate_output(df)
        return df

    def extract_links(
        self,
        url: str,
        pattern: str = "",
        extension: str = "",
    ) -> List[str]:
        self.logger.info(f"Buscando enlaces en: {url}")

        try:
            response = self.session.get(url, timeout=REQUESTS_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error(f"Error al acceder a {url}: {e}")
            return []

        soup = BeautifulSoup(response.text, "lxml")
        links = []

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if pattern and pattern not in href:
                continue
            if extension and not href.endswith(extension):
                continue
            if href.startswith("/"):
                href = f"{url.rstrip('/')}{href}"
            links.append(href)

        self.logger.info(f"Se encontraron {len(links)} enlaces")
        return links

    def download_file(self, url: str, output_path: str) -> bool:
        try:
            response = self.session.get(url, timeout=REQUESTS_TIMEOUT, stream=True)
            response.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            self.logger.info(f"Archivo descargado: {output_path}")
            return True
        except requests.RequestException as e:
            self.logger.error(f"Error al descargar {url}: {e}")
            return False
