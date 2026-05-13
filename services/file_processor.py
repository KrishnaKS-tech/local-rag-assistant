from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted + "\n"

    return text


def extract_text_from_txt(txt_file):

    return txt_file.read().decode("utf-8")