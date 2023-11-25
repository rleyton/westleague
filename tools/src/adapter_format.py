import pandas as pd
from .utils_config import RESULTS_DIR
from .utils_consts import MARKDOWN_DIR, HTML_DIR
from .adapter_pretty_html import render
import pathlib
import markdown
from markdown import Markdown
from io import StringIO


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    return __md.convert(text)


def check_dirs_exist(dir: str):
    pathlib.Path(dir + MARKDOWN_DIR).mkdir(parents=True, exist_ok=True)
    pathlib.Path(dir + HTML_DIR).mkdir(parents=True, exist_ok=True)


# markdown = Markdown()


def export_results(
    results=None,
    results_dir: str = RESULTS_DIR,
    base_file_name: str = None,
    suffix: str = None,
    index: bool = False,
):
    check_dirs_exist(dir=results_dir)
    files = {
        "csv": results_dir + "/" + base_file_name + suffix + ".csv",
        "markdown": results_dir
        + "/"
        + MARKDOWN_DIR
        + "/"
        + base_file_name
        + suffix
        + ".md",
        "html": results_dir + HTML_DIR + "/" + base_file_name + suffix + ".html",
    }
    results.to_csv(files["csv"], index=index)
    results.to_markdown(files["markdown"], index=index)
    # markdown.markdownFromFile(input=files["markdown"],output=files["html"],encoding="utf8",extensions=['markdown.extensions.tables'])
    render(df=results, style="blue_light", filename=files["html"])

    return files


def get_html(data):
    return data["html"].split("/")[-1:][0]
