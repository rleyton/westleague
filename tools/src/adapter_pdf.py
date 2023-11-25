import datetime
import pdfkit
import tempfile
from pypdf import PdfMerger
from .utils_config import RESULTS_DIR
from .utils_consts import PDF_DIR, GENDER_COMPETITION_MAP


def get_options(header):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "page-size": "A4",
        "margin-top": "0.9in",
        "margin-right": "0.9in",
        "margin-bottom": "0.9in",
        "margin-left": "0.9in",
        "encoding": "UTF-8",
        "header-center": f"{header}",
        "footer-center": f"updated: {dt}, latest at: results.westleague.org.uk",
        "custom-header": [("Accept-Encoding", "gzip")],
        "no-outline": None,
    }


def do_html_to_pdf(file, html, summary):
    if type(file) is str:
        filename = file
    else:
        filename = file.name

    pdfkit.from_file(html, filename, options=get_options(header=summary))


def generate_pdf(competition, gender, resultshtml, teamhtml, prefix=None):
    gender_full = GENDER_COMPETITION_MAP[gender]
    output_file = RESULTS_DIR + PDF_DIR + f"/{competition}-{gender}.pdf"
    result_file = tempfile.NamedTemporaryFile(
        suffix=".pdf",
    )
    team_file = tempfile.NamedTemporaryFile(
        suffix=".pdf",
    )
    if prefix is None:
        prefix = ""

    do_html_to_pdf(
        file=result_file,
        html=resultshtml,
        summary=f"{prefix}{competition} {gender_full} - race results",
    )
    do_html_to_pdf(
        file=team_file,
        html=teamhtml,
        summary=f"{prefix}{competition} {gender_full} - team results",
    )

    merger = PdfMerger()
    for file in [result_file, team_file]:
        merger.append(file.name)

    merger.write(output_file)
    merger.close()

    return output_file


def generate_single_pdf(filename, html, summary=None):
    output_file = RESULTS_DIR + PDF_DIR + "/" + filename + ".pdf"

    do_html_to_pdf(file=output_file, html=html, summary=summary)

    return output_file


def combined_pdf(pdf_list, summary, target):
    merger = PdfMerger()
    summary_file = tempfile.NamedTemporaryFile(suffix=".pdf")

    if summary is not None:
        pdfkit.from_string(input=summary, output_path=summary_file.name)
        merger.append(summary_file.name)
    for pdf in pdf_list:
        merger.append(pdf)

    merger.write(target)
    merger.close()
