from typing import List, Dict, Any
import requests
import logging


class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash") -> None:
        self._api_key = api_key
        self._model = model

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.4) -> str:
        try:
            url = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent".format(self._model)
            headers = {"x-goog-api-key": self._api_key, "Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code != 200:
                logging.warning("Gemini generate failed %s: %s", resp.status_code, resp.text[:200])
                return ""
            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return ""
            parts = candidates[0].get("content", {}).get("parts", [])
            text_parts = [p.get("text", "") for p in parts if isinstance(p, dict)]
            return "\n".join([t for t in text_parts if t])
        except Exception as e:
            logging.exception("Gemini error: %s", e)
            return ""

    def generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any],
        max_tokens: int = 1024,
        temperature: float = 0.4,
    ) -> str:
        """
        Returns the raw JSON string produced by Gemini using structured output.
        Caller is responsible for json.loads and mapping.
        """
        try:
            url = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent".format(self._model)
            headers = {"x-goog-api-key": self._api_key, "Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                    "responseMimeType": "application/json",
                    "responseSchema": response_schema,
                },
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            if resp.status_code != 200:
                logging.warning("Gemini structured failed %s: %s", resp.status_code, resp.text[:200])
                return ""
            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return ""
            parts = candidates[0].get("content", {}).get("parts", [])
            # Expect a single JSON string in parts
            for p in parts:
                if isinstance(p, dict) and "text" in p:
                    return p["text"]
            return ""
        except Exception as e:
            logging.exception("Gemini structured error: %s", e)
            return ""


