from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO, BytesIO
import requests

def convert_online_pdf_to_txt(url, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    with StringIO() as output:
        manager = PDFResourceManager()
        with TextConverter(manager, output, laparams=LAParams()) as converter:
            interpreter = PDFPageInterpreter(manager, converter)
            r = requests.get(url)
            infile = BytesIO(r.content)
            for page in PDFPage.get_pages(infile, pagenums):
                interpreter.process_page(page)
        text = output.getvalue()
    return text

if __name__ == '__main__':
    url = 'https://www.who.int/docs/default-source/coronaviruse/situation-reports/20200329-sitrep-69-covid-19.pdf?sfvrsn=8d6620fa_2'
    txt = convert_online_pdf_to_txt(url)
    print(txt)
    print(type(txt))
