import requests
from minsearch import Index

def load_faq_data():
    
    docs_url = "https://datatalks.club/faq/json/courses.json"
    response = requests.get(docs_url)
    courses_raw = response.json()
    
    documents = []
    base_url = "https://datatalks.club/faq"

    for course_faq in courses_raw:
        faq_path = f"{base_url}{course_faq['path']}"
        course_faq_response = requests.get(faq_path)
        course_faq_response.raise_for_status()
        course_faq_data = course_faq_response.json()
        documents.extend(course_faq_data)

    return documents 


def build_index(documents):
    index = Index(
    text_fields=["question", "section", "answer"],
    keyword_fields=["course"]
    )
    index.fit(documents)
    return index