# import pymupdf as fitz
# import json
# doc=fitz.open(r"C:\Users\Kajal\Downloads\David J. Griffiths-Introduction to Electrodynamics-Addison-Wesley (2012).pdf")
# # Output JSON file)
# def get_toc(doc):
#     toc = doc.get_toc()
#     return toc
# toc=get_toc(doc)
# print(toc)


# def find_start_page(toc):
#     ignore_keywords = ["cover","title page","advertisement","copyright","rights reserved","published by","isbn","library of congress","cataloging","publisher","preface","foreword","introduction to the","about the author","about the book","acknowledgement","acknowledgment","dedication","to my","in memory of","contents","table of contents","index","bibliography","references","appendix","list of figures","list of tables","list of symbols","notation","printed in","manufactured in","edition","reprint","all rights","no part of this",'Cover', 'Title page', 'Advertisement', 'Copyright', 'Rights reserved', 'Published by', 'Isbn', 'Library of congress', 'Cataloging', 'Publisher', 'Preface', 'Foreword', 'Introduction to the', 'About the author', 'About the book', 'Acknowledgement', 'Acknowledgment', 'Dedication', 'To my', 'In memory of', 'Contents', 'Table of contents', 'Index', 'Bibliography', 'References', 'Appendix', 'List of figures', 'List of tables', 'List of symbols', 'Notation', 'Printed in', 'Manufactured in', 'Edition', 'Reprint', 'All rights', 'No part of this']
#     for entry in toc:
#         title = entry[1].lower()

#         found_keyword = False

#         for keyword in ignore_keywords:

#             if keyword in title:

#                 found_keyword= True
#                 break

#         print("Checking:", title, "| Skip:", found_keyword)

#         if not found_keyword: 

#             print("Found first content page:", entry[2])

#             return entry[2]

#     return None
# toc=get_toc(doc)
# start_page=find_start_page(toc)
# print("start page=",start_page)

                 
# def build_dict(doc,start_page):
    

#     book_dict = {}

#     for page_num in range(start_page - 1, len(doc)):

#         page = doc[page_num]

#         text = page.get_text()

#         book_dict[page_num + 1] = text

#     return book_dict
# toc=get_toc(doc)
# start_page=find_start_page(toc)
# book_dict=build_dict(doc,start_page)
# print(book_dict)
# with open("extracted_text1.json", "w", encoding="utf-8") as file:

#     json.dump(book_dict, file, indent=4, ensure_ascii=False)
    
import pymupdf as fitz
import json


def get_toc(doc):
    return doc.get_toc()


def is_text_pdf(doc):
    """
    Returns True if the PDF contains extractable text.
    Returns False if it is likely a scanned/image PDF.
    """

    pages_to_check = min(5, len(doc))

    for page_num in range(pages_to_check):
        text = doc[page_num].get_text().strip()

        if text:
            return True

    return False


def find_start_page(toc):

    ignore_keywords = [
        "cover", "title page", "advertisement", "copyright",
        "rights reserved", "published by", "isbn",
        "library of congress", "cataloging", "publisher",
        "preface", "foreword", "introduction to the",
        "about the author", "about the book",
        "acknowledgement", "acknowledgment",
        "dedication", "to my", "in memory of",
        "contents", "table of contents",
        "index", "bibliography", "references",
        "appendix", "list of figures",
        "list of tables", "list of symbols",
        "notation", "printed in",
        "manufactured in", "edition",
        "reprint", "all rights",
        "no part of this"
    ]

    for entry in toc:

        title = entry[1].lower()

        found_keyword = False

        for keyword in ignore_keywords:

            if keyword in title:
                found_keyword = True
                break

        print("Checking:", title, "| Skip:", found_keyword)

        if not found_keyword:

            print("Found first content page:", entry[2])

            return entry[2]

    return None


def build_dict(doc, start_page):

    book_dict = {}

    for page_num in range(start_page - 1, len(doc)):

        page = doc[page_num]

        text = page.get_text()

        book_dict[page_num + 1] = text

    return book_dict


def process_pdf(pdf_path):

    # Open the uploaded PDF
    doc = fitz.open(pdf_path)

    # Check if it is a text-based PDF
    if not is_text_pdf(doc):
        print("This is not a text-based PDF file.")
        doc.close()
        return None

    # Extract table of contents
    toc = get_toc(doc)

    # Find the first actual content page
    start_page = find_start_page(toc)

    # Build the page dictionary
    book_dict = build_dict(doc, start_page)

    # Save as JSON
    with open("extracted_text1.json", "w", encoding="utf-8") as file:
        json.dump(book_dict, file, indent=4, ensure_ascii=False)

    doc.close()

    return book_dict
