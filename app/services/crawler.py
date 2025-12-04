import os
import requests
from bs4 import BeautifulSoup


def fetch_baidu_news(keyword: str, limit: int = 20, pn: int = 0, resolve_final: bool = True):
    params = {
        "rtt": "1",
        "bsst": "1",
        "cl": "2",
        "tn": "news",
        "rsv_dl": "ns_pc",
        "word": keyword,
        "pn": str(pn),
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        "sec-fetch-mode": "navigate",
    }
    cookie = os.getenv("BAIDU_COOKIE")
    if cookie:
        headers["cookie"] = cookie
    resp = requests.get("https://www.baidu.com/s", params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    results = []
    for item in soup.select(".result, .c-container"):
        a = item.select_one("h3 a, .c-title a, a")
        title = a.get_text(strip=True) if a else None
        url = a.get("href") if a else None

        summary_el = item.select_one(".c-summary, .c-font, .summary, .content")
        summary = summary_el.get_text(strip=True) if summary_el else None

        img_el = item.select_one("img")
        cover = img_el.get("src") if img_el else None
        if not cover:
            cover = item.get("data-thumb") if hasattr(item, "get") else None

        source_el = item.select_one(".c-span-last, .c-color-gray, .source, .news-source, .from")
        source = source_el.get_text(strip=True) if source_el else None

        final_url = url
        if resolve_final and url:
            try:
                r = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
                final_url = r.url or url
            except Exception:
                final_url = url

        if title and url:
            results.append(
                {
                    "标题": title,
                    "概要": summary,
                    "封面": cover,
                    "原始URL": url,
                    "最终URL": final_url,
                    "来源": source,
                }
            )

        if len(results) >= int(limit):
            break

    return results
