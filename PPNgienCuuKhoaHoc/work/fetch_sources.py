import concurrent.futures
import hashlib
import json
import pathlib
import shutil
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'TaiLieuNguon'
SOURCES.mkdir(exist_ok=True)
TASKS = {
    'paper.pdf': 'https://mdpi-res.com/d_attachment/data/data-07-00146/article_deploy/data-07-00146.pdf',
    'paper.html': 'https://www.mdpi.com/2306-5729/7/11/146',
    'crossref.json': 'https://api.crossref.org/works/10.3390/data7110146',
    'dataset.zip': 'https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip',
    'uci.html': 'https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success',
    'journal-indexing.html': 'https://www.mdpi.com/journal/data/indexing',
    'journal.html': 'https://www.mdpi.com/journal/data',
    'mau-thuyet-minh.docx': 'https://drive.google.com/uc?export=download&id=1fCjJPgMqbIlt4Wm_iBOtdzIx2Ui7pXFZ',
}


def fetch(item):
    name, url = item
    path = SOURCES / name
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=35) as response:
            body = response.read()
            content_type = response.headers.get('Content-Type')
            final_url = response.url
        path.write_bytes(body)
        return {'file': name, 'url': url, 'final_url': final_url, 'content_type': content_type, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
    except Exception as error:
        return {'file': name, 'url': url, 'error': str(error)}


if __name__ == '__main__':
    previous = pathlib.Path('C:/Users/ASUS/Documents/Codex/2026-10-21/https-drive-google-com-drive-folders/work/course-review')
    for name, file_id in {
        'de-giua-ky.docx': '1TfaRqkeQhOuPJNt0X3xg56aXTrodM37F.docx',
        'de-cuoi-ky.pdf': '1ksE0lPCzEx9gTvJLHdTI0AKJaGILQXQ7.pdf',
        'mau-bia.doc': '1Flcd-s4bcivE0LM_-6oA7WeI11qSLFpZ.doc',
        'de-cuong-2024.pdf': '1eTbvNt-JrhOhd-HKly34XQt5kDWpz6dc.pdf',
    }.items():
        shutil.copy2(previous / file_id, SOURCES / name)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(fetch, TASKS.items()))
    (ROOT / 'work' / 'source-manifest.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    for result in results:
        print(json.dumps(result, ensure_ascii=False))
