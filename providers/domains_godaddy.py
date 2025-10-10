from dataclasses import dataclass
import os
import requests
import logging


@dataclass
class DomainAvailability:
    domain: str
    available: bool
    reason: str | None = None


class GoDaddyClient:
    def __init__(self, key: str, secret: str) -> None:
        self._key = key
        self._secret = secret

    def check_availability(self, domain: str) -> DomainAvailability:
        try:
            base = os.getenv("GODADDY_BASE", "https://api.godaddy.com")  # use https://api.ote-godaddy.com for OTE keys
            url = f"{base}/v1/domains/available?domain={domain}"
            headers = {
                "Authorization": f"sso-key {self._key}:{self._secret}",
                "Accept": "application/json",
            }
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                logging.warning("GoDaddy availability failed %s: %s", resp.status_code, resp.text[:200])
                return DomainAvailability(domain=domain, available=False, reason="error")
            data = resp.json()
            return DomainAvailability(domain=domain, available=bool(data.get("available")), reason=data.get("reason"))
        except Exception as e:
            logging.exception("GoDaddy error: %s", e)
            return DomainAvailability(domain=domain, available=False, reason="exception")


