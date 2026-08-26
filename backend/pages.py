pages = [
    {
        "page_number": 1,
        "text": "Introduction to machine learning."
    },
    {
        "page_number": 2,
        "text": "Machine learning allows computers to learn from data."
    },
    {
        "page_number": 3,
        "text": "Supervised learning uses labelled data."
    }
]


for page in pages:
    print(f"Page {page['page_number']}: {page['text']}")