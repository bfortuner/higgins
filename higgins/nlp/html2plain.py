import mistletoe

from pathlib import Path
import pandas as pd
import pypandoc
import json
import re
from html2text import HTML2Text
from bs4 import BeautifulSoup


def table_to_json(html):
    table_data = [
        [cell.text for cell in row("td")] for row in BeautifulSoup(html)("tr")
    ]
    return dict(table_data)


def table_to_list(html: str) -> list:
    soup = BeautifulSoup(html)
    rows = soup.findAll("tr")
    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = thead.findAll("th")
        for i in range(len(thead)):
            headers[i] = thead[i].text.strip().lower()
    data = []
    for row in rows:
        cells = row.findAll("td")
        if thead:
            items = {}
            for index in headers:
                items[headers[index]] = cells[index].text
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        data.append(items)
    return data


def extract_tables_from_html(html):
    soup = BeautifulSoup(html)
    tabletag = soup.findAll("table")
    print(f"Found {len(tabletag)} tables")
    return [t.prettify() for t in tabletag]


def extract_tables_from_html_pandas(html: str):
    dfs = pd.read_html(html)
    return dfs


def html2md(html):
    parser = HTML2Text()
    parser.ignore_images = True
    parser.ignore_anchors = True
    parser.body_width = 0
    md = parser.handle(html)
    return md


def html2plain_old(html):
    # HTML to Markdown
    md = html2md(html)
    # Normalise custom lists
    md = re.sub(r"(^|\n) ? ? ?\\?[•·–-—-*]( \w)", r"\1  *\2", md)
    # Convert back into HTML
    html_simple = mistletoe.markdown(md)
    # Convert to plain text
    soup = BeautifulSoup(html_simple)
    text = soup.getText()
    # Strip off table formatting
    text = re.sub(r"(^|\n)\|\s*", r"\1", text)
    # Strip off extra emphasis
    text = re.sub(r"\*\*", "", text)
    # Remove trailing whitespace and leading newlines
    text = re.sub(r" *$", "", text)
    text = re.sub(r"\n\n+", r"\n\n", text)
    text = re.sub(r"^\n+", "", text)
    return text


def html2md_pandoc(html):
    # ...but you can overwrite the format via the `format` argument:
    # output = pypandoc.convert_file('somefile.txt', 'rst', format='md')
    # alternatively you could just pass some string. In this case you need to
    # define the input format:
    output = pypandoc.convert_text(html, to="md", format="html")
    # output == 'some title\r\n==========\r\n\r\n'
    return output


# https://github.com/wilsonzlin/minify-html
import minify_html


def minify_html_lib(html):
    return minify_html.minify(html, minify_js=True, remove_processing_instructions=True)


import readabilipy


def readable_html(html):
    jsn = readabilipy.simple_json_from_html_string(html)
    tree = readabilipy.simple_tree_from_html_string(html)
    return jsn, tree


def html2text(html: str) -> dict:
    minified_html = minify_html_lib(html)
    jsn, tree = readable_html(minified_html)
    simple_html = jsn["plain_content"]
    return simple_html


def html2text_basic(html):
    soup = BeautifulSoup(html)
    plain = [text for text in soup.stripped_strings]
    return "\n".join(plain)


def parse_html(html: str, include_tables: bool = False) -> dict:
    minified_html = minify_html_lib(html)
    jsn, _ = readable_html(minified_html)
    simplified_html = jsn["plain_content"]
    markdown = html2md(simplified_html)
    dct = {
        "minified": minified_html,
        "simplified": simplified_html,
        "text": html2text_basic(simplified_html),
        "markdown": markdown,
    }
    if include_tables:
        dct["tables"] = extract_tables_from_html(simplified_html)
    return dct


if __name__ == "__main__":
    from higgins.automation.email import email_utils

    emails = email_utils.search_local_emails([], dataset_dir="data/emails")
    # email = email_utils.load_email(email_id)
    email = emails[0]
    html = email["html"]

    # Save minified html
    minified_html = minify_html_lib(html)
    with open("email.minified.html", "w") as f:
        f.write(minified_html)

    # Extract simplified HTML
    jsn, tree = readable_html(minified_html)

    # Save plain text JSON
    with open("email.json", "w") as f:
        json.dump(jsn["plain_text"], f, indent=2)

    # Save readable html
    simple_html = jsn["plain_content"]
    with open("email.html", "w") as f:
        f.write(simple_html)

    # Print pretty html
    # pretty_html = tree.prettify()

    # Save email markdown
    md = html2md(simple_html)
    with open("email.md", "w") as f:
        f.write(md)

    # Save email plain text
    plain = html2text_basic(simple_html)
    with open("email.plain2", "w") as f:
        f.write(plain)

    tables = extract_tables_from_html(simple_html)
    for table in tables:
        if "Depart" in table:
            print(table + "\n\n\n")
            md = html2md(table)
            print(md)
            with open("table.md", "w") as f:
                f.write(md)
            with open("table.html", "w") as f:
                f.write(table)
            print(table_to_list(table))

            # dfs = pd.read_html(table.prettify())
            # print(dfs[0].head())

    import pprint
    import extruct

    # https://github.com/scrapinghub/extruct
    pp = pprint.PrettyPrinter(indent=2)
    for email in emails:
        if bool(email["html"]):
            minified_html = minify_html_lib(email["html"])
            data = extruct.extract(
                email["html"],
                uniform=True,  # syntaxes=["microdata", "opengraph", "rdfa"], uniform=True
            )
            if (
                data["json-ld"]
                or data["microdata"]
                or data["microformat"]
                or data["opengraph"]
                or data["rdfa"]
            ):
                print(email["subject"])
                pp.pprint(data)
                print("-" * 20)
