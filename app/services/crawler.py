import os
import requests
from bs4 import BeautifulSoup


def _resolve_final_url(url: str) -> str:
    try:
        # Follow redirects to get the final URL (HEAD first, fallback to GET)
        r = requests.head(url, allow_redirects=True, timeout=8)
        if r.status_code >= 400:
            r = requests.get(url, allow_redirects=True, timeout=8)
        return str(r.url)
    except Exception:
        return url


def collect_baidu(keyword: str, limit: int = 20, pn: int = 0):
    params = {
        "rtt": "1",
        "bsst": "1",
        "cl": "2",
        "tn": "news",
        "rsv_dl": "ns_pc",
        "word": keyword,
        "pn": str(max(pn, 0)),
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        "sec-fetch-mode": "navigate",
    }
    cookie = os.environ.get("BAIDU_COOKIE")
    if cookie:
        headers["cookie"] = cookie

    resp = requests.get("https://www.baidu.com/s", params=params, headers=headers, timeout=12)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    items = []
    for item in soup.select(".result, .c-container"):
        a = item.select_one("h3 a, .c-title a, a")
        title = a.get_text(strip=True) if a else None
        url = a.get("href") if a else None

        img_el = item.select_one("img")
        cover = img_el.get("src") if img_el else None

        summary_el = item.select_one(".c-summary, .c-font, .summary, .content, .c-line-clamp3")
        summary = summary_el.get_text(strip=True) if summary_el else None

        source_el = item.select_one(".c-span-last, .c-color-gray, .source, .news-source, .from")
        source = source_el.get_text(strip=True) if source_el else None

        if title and url:
            final_url = _resolve_final_url(url)
            items.append({
                "标题": title,
                "概要": summary,
                "封面": cover,
                "原始URL": final_url,
                "来源": source,
            })
        if len(items) >= max(limit, 1):
            break

    return items


def collect_xinhua_sichuan(limit: int = 20):
    # Minimal placeholder implementation; can be extended for real channel parsing
    # Return empty list with correct structure if source unreachable
    try:
        # Example page (subject to change); implement robust parsing when stabilizing source
        resp = requests.get("https://www.sc.xinhuanet.com/", timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        for a in soup.select("a"):
            title = a.get_text(strip=True)
            href = a.get("href")
            if title and href and href.startswith("http"):
                items.append({
                    "标题": title,
                    "概要": None,
                    "封面": None,
                    "原始URL": href,
                    "来源": "新华网四川频道",
                })
            if len(items) >= limit:
                break
        return items
    except Exception:
        return []
