from pypdf import PdfReader


def extract_text_from_pdf():
    # creating a pdf reader object
    reader = PdfReader(
        "/Users/christianl/repos/CS7646/Readings/intro_to_statistical_learning.pdf"
    )

    # store the text for writing to a txt file line by line
    text = []
    for page in reader.pages:
        text.append(page.extract_text())

    # write the text to a txt file
    with open("intro_to_statistical_learning.txt", "w") as f:
        for line in text:
            f.write(line)
            f.write("\n")


if __name__ == "__main__":
    extract_text_from_pdf()
