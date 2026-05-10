import time
from typing import Dict, Any, Optional, List
import requests
import pandas as pd
from src.extract.base_extractor import BaseExtractor
from src.config.settings import REQUESTS_TIMEOUT, REQUESTS_RETRY, USER_AGENT


class ApiExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("api")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def extract(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data_key: Optional[str] = None,
    ) -> pd.DataFrame:
        self.logger.info(f"Consultando API: {url}")
        response = self._request_with_retry(url, params)

        if response is None:
            return pd.DataFrame()

        json_data = response.json()

        if data_key and data_key in json_data:
            records = json_data[data_key]
        elif isinstance(json_data, list):
            records = json_data
        else:
            records = [json_data]

        df = pd.DataFrame(records)
        self.validate_output(df)
        return df

    def extract_paginated(
        self,
        url: str,
        page_param: str = "page",
        limit_param: str = "limit",
        limit: int = 100,
        data_key: Optional[str] = None,
        max_pages: int = 50,
    ) -> pd.DataFrame:
        all_records: List[Dict] = []
        page = 1

        while page <= max_pages:
            params = {page_param: page, limit_param: limit}
            response = self._request_with_retry(url, params)

            if response is None:
                break

            json_data = response.json()
            records = json_data.get(data_key, []) if data_key else json_data

            if not records:
                break

            all_records.extend(records)
            self.logger.info(f"Pagina {page}: {len(records)} registros")
            page += 1
            time.sleep(0.5)

        df = pd.DataFrame(all_records)
        self.validate_output(df)
        return df

    def _request_with_retry(
        self,
        url: str,
        params: Optional[Dict] = None,
    ) -> Optional[requests.Response]:
        for attempt in range(1, REQUESTS_RETRY + 1):
            try:
                response = self.session.get(
                    url, params=params, timeout=REQUESTS_TIMEOUT
                )
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                self.logger.warning(
                    f"Intento {attempt}/{REQUESTS_RETRY} fallido: {e}"
                )
                if attempt < REQUESTS_RETRY:
                    time.sleep(2 ** attempt)

        self.logger.error(f"Todos los intentos fallaron para {url}")
        return None
