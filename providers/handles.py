import requests
from dataclasses import dataclass


SOCIAL_BASE = {
    "x": "https://x.com/{}",
    "instagram": "https://instagram.com/{}",
    "youtube": "https://youtube.com/@{}",
}


@dataclass
class HandleStatus:
    network: str
    handle: str
    exists: bool


def check_handle(network: str, handle: str, timeout: int = 8) -> HandleStatus:
    url = SOCIAL_BASE[network].format(handle)
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        exists = resp.status_code == 200
        return HandleStatus(network=network, handle=handle, exists=exists)
    except Exception:
        return HandleStatus(network=network, handle=handle, exists=False)


