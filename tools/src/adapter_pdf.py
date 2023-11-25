import pdfkit
import tempfile
from pypdf import PdfMerger

from .utils_config import RESULTS_DIR
from .utils_consts import PDF_DIR

def get_options(header):
    return {
        "page-size": "A4",
        "margin-top": "0.9in",
        "margin-right": "0.9in",
        "margin-bottom": "0.9in",
        "margin-left": "0.9in",
        "encoding": "UTF-8",
        "header-center": f"{header}",
        "custom-header": [("Accept-Encoding", "gzip")],
        "no-outline": None,
    }

def generate_pdf(competition, gender, resultshtml, teamhtml, summary=None):
    if gender is not None:
        result_file = RESULTS_DIR + PDF_DIR + f"/{competition}-{gender}.pdf"
    else:
        gender=""
        result_file = RESULTS_DIR + PDF_DIR + f"/{competition}.pdf"
    options = get_options(f"{competition} {gender}")
    page1 = tempfile.NamedTemporaryFile(suffix=".html")
    if summary is None:
        page1.write(f"<h1>{competition} {gender} Race results</h1>".encode("utf8"))
    else:
        page1.write(summary.encode("utf8"))
    page1.flush()

    page2 = tempfile.NamedTemporaryFile(suffix=".html")
    page2.write(f"<h1>{competition} {gender} Team results</h1>".encode("utf8"))
    page2.flush()

    pages = [page1.name, resultshtml]
    if teamhtml is not None:
        pages.append(page2.name)
        pages.append(teamhtml)

    pdfkit.from_file(
        pages,
        result_file,
        options=options,
    )
    page1.close()
    page2.close()

    return result_file


def combined_pdf(pdf_list, summary, target):
    merger = PdfMerger()
    summary_file = tempfile.NamedTemporaryFile(suffix=".pdf")
    
    if summary is not None:    
        pdfkit.from_string(input=summary,output_path=summary_file.name)
        merger.append(summary_file.name)
    for pdf in pdf_list:
        merger.append(pdf)

    merger.write(target)
    merger.close()
