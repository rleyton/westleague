import pandas as pd
from .utils_consts import RESULTS_DIR, MARKDOWN_DIR, HTML_DIR
from .adapter_pretty_html import render


def export_results(
    results=None,
    results_dir: str = RESULTS_DIR,
    base_file_name: str = None,
    suffix: str = None,
    index: bool = False,
):

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
    render(df=results, style="blue_light", filename=files["html"])

    return files


def get_html(data):
    return data["html"].split("/")[-1:][0]
