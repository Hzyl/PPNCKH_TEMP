from pathlib import Path
import urllib.request, json, hashlib, shutil
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader
ROOT=Path(r'C:\Users\ASUS\OneDrive\Máy tính\c\PPNgienCuuKhoaHoc')
OUT=ROOT/'TaiLieuNguon'/'TongQuan_2026-11-06'
OUT.mkdir(exist_ok=True)
items=[
('P3_Phashed_2023','https://mdpi-res.com/d_attachment/applsci/applsci-13-04702/article_deploy/applsci-13-04702.pdf'),
('P4_Finland_2024','https://trepo.tuni.fi/bitstream/handle/10024/210457/Predicting_student_dropouts.pdf?sequence=1'),
('P5_EDM_2024','https://educationaldatamining.org/edm2024/proceedings/2024.EDM-short-papers.32/2024.EDM-short-papers.32.pdf'),
('P6_Sahmyook_2023','https://mdpi-res.com/d_attachment/applsci/applsci-13-12004/article_deploy/applsci-13-12004.pdf')]
def one(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  data=urllib.request.urlopen(req,timeout=60).read()
  assert data[:5]==b'%PDF-',data[:50]
  f=OUT/(name+'.pdf'); f.write_bytes(data)
  r=PdfReader(f); pages=[p.extract_text() or '' for p in r.pages]
  (OUT/(name+'.txt')).write_text('\n\n'.join(f'=== PAGE {i+1} ===\n{t}' for i,t in enumerate(pages)),encoding='utf-8')
  (OUT/(name+'.pages.json')).write_text(json.dumps(pages,ensure_ascii=False),encoding='utf-8')
  return dict(id=name,url=url,pages=len(pages),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),file=str(f))
 except Exception as e:return dict(id=name,url=url,error=str(e))
results=list(ThreadPoolExecutor(4).map(one,items))
(OUT/'downloads.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
