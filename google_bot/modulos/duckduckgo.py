from duckduckgo_search import DDGS

def duckduckgo_search(query: str, results: int = 10) -> list[str]:
    urls = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=results):
            # Cada r es un dict con 'href'
            href = r.get("href")
            if href:
                urls.append(href)
    return urls