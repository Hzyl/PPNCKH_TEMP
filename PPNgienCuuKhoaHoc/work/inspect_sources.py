import json
import pathlib
import zipfile

from docx import Document
from lxml import etree
from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'TaiLieuNguon'
reader = PdfReader(SOURCE / 'paper.pdf')
pages = [{'page': i, 'text': page.extract_text()} for i, page in enumerate(reader.pages, 1)]
(ROOT / 'work' / 'paper-pages.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
(ROOT / 'work' / 'paper.txt').write_text('\n\n'.join(f'PAGE {p["page"]}\n{p["text"]}' for p in pages), encoding='utf-8')
print('Paper pages:', len(pages))
for name in ['mau-thuyet-minh.docx', 'de-giua-ky.docx']:
    doc = Document(SOURCE / name)
    paragraphs = []
    for p in doc.element.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        content = ''.join(p.itertext())
        texts = p.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
        content = ''.join(t.text or '' for t in texts)
        if content.strip():
            paragraphs.append(content)
    (ROOT / 'work' / f'{name}.txt').write_text('\n'.join(paragraphs), encoding='utf-8')
    print(name, 'paragraphs:', len(paragraphs), 'tables:', len(doc.tables))
    for sec in doc.sections:
        print('Page/margins cm:', [round(x.cm, 3) for x in [sec.page_width, sec.page_height, sec.top_margin, sec.bottom_margin, sec.left_margin, sec.right_margin]])
with zipfile.ZipFile(SOURCE / 'dataset.zip') as archive:
    print('Dataset members:', archive.namelist())
    for info in archive.infolist():
        if info.filename.endswith('.csv') and '..' not in pathlib.PurePosixPath(info.filename).parts:
            (SOURCE / 'data.csv').write_bytes(archive.read(info.filename))
crossref = json.loads((SOURCE / 'crossref.json').read_text(encoding='utf-8'))['message']
print(json.dumps({k: crossref.get(k) for k in ['title', 'author', 'container-title', 'published', 'DOI', 'ISSN']}, ensure_ascii=False, indent=2))
