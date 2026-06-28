


import re
import json

with open("extracted_text1.json","r",encoding="utf-8") as file:
        data=json.load(file)
def get_context_around_match(text, match, word_limit=100):
    before_text = text[:match.start()]
    after_text = text[match.end():]

    before_words = before_text.split()
    after_words = after_text.split()

    before_context = before_words[-word_limit:]
    after_context = after_words[:word_limit]

    matched_text = text[match.start():match.end()]

    context_words = before_context + [matched_text] + after_context

    return " ".join(context_words)        
        

def extract():
    dict_topic = {}
    

    pattern_top = r"(?m)(\d+(?:\.\d+)+)\s*\n+\s*([A-Z][A-Za-z\s\-]{3,})"
    pattern_equation = r"(?i)(?:\b(?:eq\.?|equation)\s*\(?\s*(\d+(?:\.\d+)*)\s*\)?|\(\s*(\d+(?:\.\d+)*)\s*\))"
    pattern_figure = r"(?i)\b(?:fig\.?|figure)\s*(\d+(?:\.\d+)*)\b"
    pattern_figure_caption = r"(?i)\b(?:fig\.?|figure)\s*(\d+(?:\.\d+)*)[:.\s-]+([^\n]+)"

    for page_no in sorted(data.keys(), key=int):
        page_text = data[page_no]
        matches = list(re.finditer(pattern_top, page_text))

        for i, match in enumerate(matches):
            number = match.group(1)
            title = match.group(2).strip()
            topic_key = f"{number} {title}"

            content_start = match.end()

            if i == len(matches) - 1:
                content_end = len(page_text)
            else:
                content_end = matches[i + 1].start()

            topic_text = page_text[content_start:content_end].strip()

            dict_topic[topic_key] = {
                "placement": number,
                "page": int(page_no),
                "type": "topic",
                "text": topic_text
            }



    for topic_key,topic_data in dict_topic.items():
        topic_text = topic_data["text"]

        related_top = re.findall(pattern_top, topic_text)
        related_equ = re.findall(pattern_equation, topic_text)
        related_fig = re.findall(pattern_figure, topic_text)

        topic_data["related_content"] = {
            "related_topics": related_top,
            "related_equations": related_equ,
            "related_figures": related_fig
        }
        related_equations = {}
        related_figures = {}
        

        for equation_match in re.finditer(pattern_equation, topic_text):
            equation_number = equation_match.group(1) or equation_match.group(2) or equation_match.group(3)
            equation_number = equation_number.replace(" ", "")

            equation_context = get_context_around_match(topic_text, equation_match, word_limit=100)

            related_equations[equation_number] = equation_context
            topic_data["related_content"] = {
    "related_topics": related_top,
    "related_equations": related_equations,
    "related_figures": related_figures}
            related_figures = {}
           

        for figure_match in re.finditer(pattern_figure_caption, topic_text):
            figure_number = figure_match.group(1)
            figure_caption = figure_match.group(2).strip()

            related_figures[figure_number] = figure_caption
            




    
    return dict_topic


result=extract()

if len(result)==0:

    with open("phase2_topics.json","w",encoding="utf-8") as file:
        json.dump({},file,indent=4,ensure_ascii=False)

    raise RuntimeError(
        "No topics could be extracted from this PDF. "
        "The document may not contain recognizable chapter headings."
    )

with open("phase2_topics.json","w",encoding="utf-8") as file:
    json.dump(result,file,indent=4,ensure_ascii=False)

print("Phase 2 extraction complete.")
              
                  



        

