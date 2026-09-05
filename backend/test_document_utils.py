from backend.document_utils import count_words


def test_count_words():

    text = "DocuMind is a document question answering system."

    result = count_words(text)

    assert result == 7