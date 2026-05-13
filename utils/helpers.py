import os


DOCUMENTS_DIR = "data/documents"


def save_uploaded_file(uploaded_file):

    os.makedirs(
        DOCUMENTS_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        DOCUMENTS_DIR,
        uploaded_file.name
    )

    with open(file_path, "wb") as file:

        file.write(uploaded_file.getbuffer())

    return file_path