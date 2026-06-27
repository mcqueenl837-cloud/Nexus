

# match=re.search(pattern,text)
# print(match)
# matx=re.finditer(pattern,text)
# print(matx)
# pattern=r"[A-za-z]+"
# match=re.findall(pattern,page_text)
# print(match[:20])
# pattern_eq = r"(?:Equation|equation|Eq\.|eq\.)\s*\d+\.\d+"
# pattern_top=r"\d+(?:\.\d+)+\s+[A-z][A-Za-z\s\-]+"
# search_eq=re.findall(pattern_eq,data)
# search_top=re.findall(pattern_top,data)

# for page_number, page_text in data.items():

#     search_eq = re.findall(pattern_eq, page_text)
#     search_top = re.findall(pattern_top, page_text)

#     if search_eq:
#         print("Page:", page_number)
#         print("Equations:", search_eq)

#     if search_top:
#         print("Page:", page_number)
#         print("Topics:", search_top)
# import re
# import json

# with open("extracted_text1.json","r",encoding="utf-8") as file:
#         data=json.load(file)
    
# def extract():
   
    
#     dict_topic={}
    # pattern_top = r"(\d+(?:\.\d+)+)"

    # for page_no in sorted(data.keys(), key=int):

    #     page_text = data[page_no]

    #     matches = list(re.finditer(pattern_top, page_text))

    #     for i, match in enumerate(matches):

    #         placement = match.group()

    #         start = match.start()

    #         if i < len(matches) - 1:
    #             end = matches[i + 1].start()
    #         else:
    #             end = len(page_text)

    #         topic_content = page_text[start:end]

    #         dict_topic[placement] = {
    #         "placement": placement,
    #         "page": int(page_no),
    #         "text": topic_content
    #     }
    #     return dict_topic    #"page":int(page_no)# def extract():
   
    
#     dict_topic={}    
#     pattern_top = r"(\d+(?:\.\d+)+)\s*\n+\s*([A-Z][A-Za-z\s\-]{3,})"#"\d+(?:\.\d+)+\s+[A-z][A-Za-z\s\-]+"
#     for page_no in sorted(data.keys(),key=int):#universal command for page sorting,since key was not in int value we had convert it into int by key=int

#         page_text=data[page_no]
#         topics=re.findall(pattern_top,page_text)# here we use use page_text as , page_text is filled in the order of sorted page_no by for loop
#         for topic in topics:
#              if topic  in dict_topic:
#                   continue
#              else:
#                   dict_topic[topic]={"placement":topic,"page":int(page_no),"text":page_text}
                       
#                   #building dictionary
#         return dict_topic
    
# print(extract())
# def extract():
#     dict_topic = {}



     

#     for page_no in sorted(data.keys(), key=int):
#         page_text = data[page_no]
#         matches = list(re.finditer(pattern_top, page_text))

#         for i, match in enumerate(matches):#enumerate for indexing
#             number = match.group(1)#group is used for placement of variables which they are assigned to,such as title and number
#             title = match.group(2).strip()# here strip is just used to divide and a better way to show the output
#             topic_key = f"{title}"

#             content_start = match.end()#here end is used to define where atual content ends. So, for contenet_start it uses for a boundary

#             if i==len(matches):#here i+1 means if there are more than one match or title in that for loop( here for loop, sees in the each page)
#                 content_end = matches[i].start()#here i+1 is used as python. The last value is often ignored, so by adding 1 . We can get one more. Since we are using len then we also need to get at last value
#             else:#here, with i==len means that iteration(i) would have length equal to length of matches.Here, matches is the entire iterated loop through content. Mtaches are split for topic wise.
#                 content_end = len(page_text)
               
                     

#             topic_text = page_text[content_start:content_end]
            
    
            

#     dict_topic[topic_key] = {"placement": number,"page": int(page_no),"type": "topic","text": topic_text}
#     related_top=re.findall(pattern_top,topic_text) 
#     related_equ=re.findall(pattern_equation,topic_text)
#     related_fig=re.findall(pattern_figure,topic_text)

#     # for topic_text in dict_topic.items():
         
#     #     if related_top in topic_text:
#     #         dict_topic[topic_key]={"related_topic":related_top,}
#     #     if related_equ in topic_text:
#     #         dict_topic[topic_key]={"related_equation":related_equ}
#     #     if related_fig in topic_text:
#     #         dict_topic[topic_key]={"related_figure":related_fig}
    
    

            
            
                 

#     return dict_topic
# # print(extract())

# result=extract()
# print(result)
# def extract():
#     dict_topic = {}
#     #"\d+(?:\.\d+)+\s+[A-z][A-Za-z\s\-]+"
#     pattern_top = r"(?m)(\d+(?:\.\d+)+)\s*\n+\s*([A-Z][A-Za-z\s\-]{3,})"
#     pattern_equation = r"(?i)(?:\b(?:eq\.?|equation)\s*\(?\s*(\d+(?:\.\d+)*)\s*\)?|\(\s*(\d+(?:\.\d+)*)\s*\))"
#     pattern_figure = r"(?i)\b(?:fig\.?|figure)\s*(\d+(?:\.\d+)*)\b"


#     for page_no in sorted(data.keys(), key=int):
#         page_text = data[page_no]
#         matches = list(re.finditer(pattern_top, page_text))
#         content_start = match.end()

#         if i == len(matches) - 1:
#             content_end = len(page_text)
#         else:
#             content_end = matches[i + 1].start()
#     if i==len(matches)-1:
#         content_end = len(page_text)
#     else:
#         content_end = matches[i+1].start()

#     topic_text = page_text[content_start:content_end].strip()

#     dict_topic[topic_key] = {
#         "placement": number,
#         "page": int(page_no),
#         "type": "topic",
#         "text": topic_text
#     }

#         # for i, match in enumerate(matches):
#         #     number = match.group(1)#group is used for placement of variables which they are assigned to,such as title and number
#         #     title = match.group(2).strip()# here strip is just used to divide and a better way to show the output
#         #     topic_key = f"{title}"
#         #     topic_text = page_text[content_start:content_end].strip()
#         #     # create topic_key
#         #     # create topic_text

#         #     dict_topic[topic_key] = {
#         #         "placement": number,
#         #         "page": int(page_no),
#         #         "type": "topic",
#         #         "text": topic_text
#         #     }

#     for topic_key, topic_data in dict_topic.items():
#         topic_text = topic_data["text"]

#         related_top = re.findall(pattern_top, topic_text)
#         related_equ = re.findall(pattern_equation, topic_text)
#         related_fig = re.findall(pattern_figure, topic_text)

#         topic_data["related_content"] = {
#             "related_topics": related_top,
#             "related_equations": related_equ,
#             "related_figures": related_fig
#         }



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
with open("phase2_topics.json", "w", encoding="utf-8") as file:
    json.dump(result, file, indent=4, ensure_ascii=False)

print("Phase 2 extraction complete.")

              
                  



        

