import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent":
    "Mozilla/5.0"
}


def extract_url(url: str):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove unnecessary elements

    for tag in soup([
        "script",
        "style",
        "noscript",
        "header",
        "footer",
        "nav",
        "aside"
    ]):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return [
        {
            "page": 1,
            "text": text
        }
    ]