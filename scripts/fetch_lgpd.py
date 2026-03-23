import os
import re

import httpx
from bs4 import BeautifulSoup


def fetch_lgpd_to_markdown():
    url = "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"  # noqa: E501
    }

    print(f"Fetching LGPD from {url}...")
    try:
        response = httpx.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()
        content = response.content.decode("windows-1252")
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    print("Parsing HTML and converting to Markdown...")
    soup = BeautifulSoup(content, "lxml")

    # Simple extraction logic: everything is mostly in <p> tags
    markdown_lines = []
    markdown_lines.append("# LEI Nº 13.709, DE 14 DE AGOSTO DE 2018\n")

    paragraphs = soup.find_all("p")

    for p in paragraphs:
        text = p.get_text().strip()
        if not text:
            continue

        # Ignore revoked parts
        if p.find("strike") or p.find("font", {"color": "#800000"}):
            continue

        # 1. Chapters/Sections -> # (H1)
        if "CAPÍTULO" in text.upper() or "SEÇÃO" in text.upper():
            markdown_lines.append(f"\n# {text}\n")
            continue

        # 2. Articles -> ## (H2)
        art_match = re.match(r"^(Art\.\s*\d+[^a-zA-Z]*)", text)
        if art_match:
            art_title = art_match.group(1).strip()
            art_content = text[len(art_title) :].strip()
            markdown_lines.append(f"\n## {art_title}\n{art_content}\n")
            continue

        # 3. Incisions, Paragraphs, Items -> ### (H3)
        # Matches: I -, II -, § 1º, a), Parágrafo único.
        incision_match = re.match(
            r"^(Parágrafo único\.|§\s*\d+[^a-zA-Z]*|[IVXLCDM]+\s*-|[a-z]\)\s*)",
            text,
        )
        if incision_match:
            inc_title = incision_match.group(1).strip()
            inc_content = text[len(inc_title) :].strip()
            markdown_lines.append(f"\n### {inc_title}\n{inc_content}\n")
            continue

        # 4. Standard text (often introductory sentences of an article)
        markdown_lines.append(f"{text}\n")

    # Final cleanup: join and write
    full_markdown = "".join(markdown_lines)

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    output_path = "data/lgpd.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)

    print(f"Success! LGPD saved to {output_path}")


if __name__ == "__main__":
    fetch_lgpd_to_markdown()
