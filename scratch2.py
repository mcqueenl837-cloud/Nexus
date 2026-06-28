import pymupdf as fitz
import json


def get_toc(doc):
    return doc.get_toc()


def is_text_pdf(doc):
    """
    Returns True if the PDF contains extractable text.
    Returns False if it is likely a scanned/image PDF.
    """

    pages_to_check=min(5,len(doc))

    for page_num in range(pages_to_check):

        text=doc[page_num].get_text().strip()

        if text:
            return True

    return False


def find_start_page(toc):

    ignore_keywords=[
        "cover","title page","advertisement","copyright",
        "rights reserved","published by","isbn",
        "library of congress","cataloging","publisher",
        "preface","foreword","introduction to the",
        "about the author","about the book",
        "acknowledgement","acknowledgment",
        "dedication","to my","in memory of",
        "contents","table of contents",
        "index","bibliography","references",
        "appendix","list of figures",
        "list of tables","list of symbols",
        "notation","printed in",
        "manufactured in","edition",
        "reprint","all rights",
        "no part of this"
    ]

    for entry in toc:

        title=entry[1].lower()

        found_keyword=False

        for keyword in ignore_keywords:

            if keyword in title:
                found_keyword=True
                break

        if not found_keyword:

            return entry[2]

    return None


def build_dict(doc,start_page):

    if start_page is None:
        start_page=1

    book_dict={}

    for page_num in range(start_page-1,len(doc)):

        page=doc[page_num]

        text=page.get_text()

        book_dict[page_num+1]=text

    return book_dict


def process_pdf(pdf_path, output_directory="."):

    os = __import__("os")
    os.makedirs(output_directory, exist_ok=True)

    doc = fitz.open(pdf_path)

    if not is_text_pdf(doc):
        print("This is not a text-based PDF file.")
        doc.close()
        return None

    toc = get_toc(doc)

    if len(toc) == 0:
        print("No TOC found. Starting extraction from page 1.")
        start_page = 1
    else:
        start_page = find_start_page(toc)

    if start_page is None:
        print("Could not determine the first chapter. Starting from page 1.")
        start_page = 1

    print("=" * 40)
    print("TOC:", toc)
    print("Length of TOC:", len(toc))
    print("start_page:", start_page)
    print("=" * 40)

    book_dict = build_dict(doc, start_page)

    output_path = os.path.join(output_directory, "extracted_text1.json")

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(book_dict, file, indent=4, ensure_ascii=False)

    doc.close()

    return book_dict