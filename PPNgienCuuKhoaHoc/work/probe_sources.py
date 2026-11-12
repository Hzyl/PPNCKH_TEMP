from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
ROOT = Path(__file__).resolve().parents[1]
urls = {
    "sjr-google": "https://r.jina.ai/https://www.google.com/search?q=" + quote('site:scimagojr.com/journalsearch.php "21100924372"'),
    "sjr-bing": "https://r.jina.ai/https://www.bing.com/search?q=" + quote('site:scimagojr.com "Data" "Computer Science Applications"'),
    "sjr-mobile": "https://www.scimagojr.com/journalsearch.php?clean=0&q=21100924372&tip=sid",
    "vietnam": "https://r.jina.ai/https://www.google.com/search?q=" + quote('dự báo sinh viên bỏ học học máy tạp chí đại học Việt Nam'),
}
def run(item):
    name, url = item
    try:
        data = urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()
        (ROOT / "TaiLieuNguon" / ("root-" + name + ".txt")).write_bytes(data)
        return name, len(data), data.decode("utf-8", errors="replace")[:18000]
    except Exception as exc:
        return name, str(exc)
for result in ThreadPoolExecutor(max_workers=4).map(run, urls.items()):
    print(result)
