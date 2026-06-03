import argparse
from pathlib import Path
import sys
import markdown
from weasyprint import HTML

def render_pdf(html, page_size):
    pdf = HTML(string=html)

    return pdf.write_pdf()

def text_to_html(text):
    fenced = f"```\n{text}\n```"
    return markdown.markdown(
        fenced,
        extensions=["fenced_code"]
    )

def markdown_to_html(text):
    return markdown.markdown(
        text,
        extensions=[
            "fenced_code",
            "tables",
            "toc",
            "codehilite"
        ]
    )

def convert_to_html(content, input_type):
    if input_type == "html":
        return content

    if input_type == "markdown":
        return markdown_to_html(content)

    if input_type == "text":
        return text_to_html(content)

    raise ValueError(f"Unknown type: {input_type}")

def read_input(filename):
    if filename is None:
        return sys.stdin.read()

    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
    import sys


def write_output(pdf_bytes, destination):
    if destination == "-":
        sys.stdout.buffer.write(pdf_bytes)
        return

    with open(destination, "wb") as f:
        f.write(pdf_bytes)

def build_parser():
    parser = argparse.ArgumentParser(
        prog="topdf",
        description="Convert text, markdown, or HTML into PDF."
    )

    parser.add_argument(
        "input",
        nargs="?",
        help="Input file. If omitted, read from stdin."
    )

    parser.add_argument(
        "output",
        nargs="?",
        help="Output PDF file."
    )

    fmt = parser.add_mutually_exclusive_group()

    fmt.add_argument(
        "-M", "--markdown",
        action="store_true",
        help="Treat input as Markdown."
    )

    fmt.add_argument(
        "-T", "--text",
        action="store_true",
        help="Treat input as plain text."
    )

    fmt.add_argument(
        "-H", "--html",
        action="store_true",
        help="Treat input as HTML."
    )

    size = parser.add_mutually_exclusive_group()

    size.add_argument(
        "-a", "--a4",
        action="store_true",
        help="Use A4 paper."
    )

    size.add_argument(
        "-l", "--letter",
        action="store_true",
        help="Use Letter paper."
    )

    parser.add_argument(
        "-o", "--output-file",
        help="Output PDF filename."
    )

    parser.add_argument(
        "-O", "--stdout",
        action="store_true",
        help="Write PDF to stdout."
    )

    return parser

def detect_input_type(args, filename):
    if args.markdown:
        return "markdown"

    if args.text:
        return "text"

    if args.html:
        return "html"

    if filename:
        ext = Path(filename).suffix.lower()

        if ext in (".md", ".markdown"):
            return "markdown"

        if ext in (".html", ".htm"):
            return "html"

    return "text"

def main():
    parser = build_parser()
    args = parser.parse_args()

    input_source = determine_input(args)
    output_target = determine_output(args)

    raw_text = read_input(input_source)

    input_type = detect_input_type(args, input_source)

    html = convert_to_html(raw_text, input_type)

    pdf_bytes = render_pdf(html, paper_size(args))

    write_output(pdf_bytes, output_target)

