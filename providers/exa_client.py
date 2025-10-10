from dataclasses import dataclass
from typing import List, Optional
import requests
import logging


@dataclass
class ExaResult:
    url: str
    title: Optional[str]


class ExaClient:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def search(self, query: str, top_k: int = 5) -> List[ExaResult]:
        try:
            resp = requests.post(
                "https://api.exa.ai/search",
                headers={"x-api-key": self._api_key, "Content-Type": "application/json"},
                json={"query": query, "numResults": max(1, min(top_k, 10))},
                timeout=15,
            )
            if resp.status_code != 200:
                logging.warning("EXA search failed %s: %s", resp.status_code, resp.text[:200])
                return []
            data = resp.json()
            results = []
            for item in data.get("results", [])[:top_k]:
                url = item.get("url") or item.get("id") or ""
                if url:
                    results.append(ExaResult(url=url, title=item.get("title")))
            return results
        except Exception as e:
            logging.exception("EXA search error: %s", e)
            return []


