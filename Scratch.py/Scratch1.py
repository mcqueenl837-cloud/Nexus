
# for i in range(1,101,10):
#     print(i)    
# for k in range(1,20):
#     print(k+1)
# while loop
# i=9
# while(i<=10):
# #     print(i)
# for i in range(12):
#     print(i)
#     if(i==10):
#         break
# i=0
# # while True:
# #     print(i)
# #     i=i+1
# #     if(i%101 == 0):
# #         break


# def calcgmean(a,b):
#     mean=(a*b)/(a+b)
#     print(mean)
# a=7
# b=8
# calcgmean(a,b)



# def addmean():
#     t=0
#     for i in range(1,101):
#         t+=i
#     return t
# print(addmean())



# def ave(a,b):
#     print("the" , a+b/2)
# ave(2,3)
# l=[1,2,3,4,5,6,7,8,9,10]
# l.append(8)
# print(l.index(8))
# m=l
# m[3]=46
# print(m)
# m=l.copy()
# m[7]=90
# print(m)
# print(
# def multi(a,b):
    
#     return a*b
# multi(6,8)
# print(multi(6,8))
# def calc_area(r):
    
#     return 3.14*r**2
    
# calc_area(2)
# print(calc_area(2))

# def matrix(a,b,c,d):
#     x=a*d-b*c
    
    
#     if b==c:
#         print("symmetric matrix") 
#     else:
#         print("none")
#     return x
# x=matrix(6,8,9,0)
    


# print(x)

# def add(a,b):
#     return a+b
# result=add(5,10)
# print(result)
# print(add(result,20))


# def compute(a,b):
#     result=a+b
#     if result>10:
#         return result-3
#     return result+4
# print(compute(3,2))
# print(compute(5,3))
# print(doc.metadata)
# for page_num in range(len(doc)):
#     page=doc[page_num]
#     text=page.get_text()
#     print(f"\n---Page{page_num+1}---")
#     print(text)


# print("Pages:",len(doc)) 
# blocks=page.get_text("blocks",sort=True)
# print(page.get_text("blocks"))
# for block in blocks:
#     print(block,"\n")
#     print("block #",block[5])
# pgdict=page.get_text("dict")
# print(pgdict)
# def get_toc(doc):
#     # return doc.get_toc()
#     toc=doc.get_toc()
#     print(toc)
# get_toc(doc)
# print("Checking:", title)

        # if title not in ignore_keywords:

        #     start_page = entry[2]

        #     print("Found first content page:", start_page)

        #     return start_page

    
# def find_start_page(toc):
#     ignore_keywords = [
#     # Copyright and legal
#     "copyright", "rights reserved", "published by", "isbn", 
#     "library of congress", "cataloging", "publisher",
    
#     # Preliminary pages
#     "preface", "foreword", "introduction to the", 
#     "about the author", "about the book", "acknowledgement",
#     "acknowledgment", "dedication", "to my", "in memory of",
    
#     # Navigation pages  
#     "contents", "table of contents", "index", "bibliography",
#     "references", "appendix", "list of figures", "list of tables",
#     "list of symbols", "notation","cover","Title page","adverstisement",
    
#     # Publisher boilerplate
#     "printed in", "manufactured in", "edition", "reprint",
#     "all rights", "no part of this"
# ]
#     for entry in toc:
#         print(entry[1])
#         toc=entry[1].lowercase()
#         name=entry[1]
#         if name not in ignore_keywords:
#             print("found valid keywords")
#             number=entry[2]
#             print(number)
#             break 
# find_start_page(toc)
# ignore_keywords = ["cover","title page","advertisement","copyright","rights reserved","published by","isbn","library of congress","cataloging","publisher","preface","foreword","introduction to the","about the author","about the book","acknowledgement","acknowledgment","dedication","to my","in memory of","contents","table of contents","index","bibliography","references","appendix","list of figures","list of tables","list of symbols","notation","printed in","manufactured in","edition","reprint","all rights","no part of this"]
# cap=list(map(str.capitalize,ignore_keywords))
# # print(cap)
# import re
# pattern=r"[a-z]"
# text="shivam jha is going to turn 23"
# match=re.search(pattern,text)
# if match:
#     print("yes")
#     print(match)
# else:
#     print("no")
# #re.search for verification
# matx=re.finditer(pattern,text)
# #for loop is used for search in entire text
# for match in matx:
#     print(matx)
#     # span for specific searching as span[0]


student_notes = {
    "Physics": {
        "chapter": "Motion",
        "page": 12,
        "text": "Velocity is the rate of change of displacement with time."},
    "Math": {
        "chapter": "Algebra",
        "page": 25,
        "text": "A quadratic equation has the form ax squared plus bx plus c."
    },
    "Chemistry": {
        "chapter": "Atoms",
        "page": 40,
        "text": "Atoms are made of protons, neutrons, and electrons."
    }
}
def prepare_student_notes(student_notes):
    ids = []
    documents = []
    metadatas = []

    for subject_key, subject_data in student_notes.items():#here subject_key is the first thing that gets checked than subject_data gets checked in students_notes.items()
        chapter = subject_data["chapter"]
        page = subject_data["page"]
        text = subject_data["text"]

        document_text = f"""Subject: {subject_key}, Chapter: {chapter}, Page: {page}, Content:{text}"""
        record_id = f"{subject_key}"

        metadata = {"page": page}
        

        # ids.append(record_id)
        documents.append(document_text)
        metadatas.append(metadata)

        return  ids,documents,metadatas
ids, documents, metadatas = prepare_student_notes(student_notes)

print(documents)
# print(documents)
#print(metadatas)