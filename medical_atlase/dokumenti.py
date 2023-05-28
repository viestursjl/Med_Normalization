# Import the defined input/output file names or routes
import constants
import xml.etree.ElementTree as ET


# -------------------------------
# Beginning of defining functions
# -------------------------------
def get_tezaurs_medical_terms():
    terms = []

    clear_output_file()
    output = open(constants.output_terms, 'a', encoding="utf-8")

    tree = ET.parse(constants.tezaurs_file)
    root = tree.getroot()

    for entry in root.findall("./body/"):
        if entry.get('n') == "1":
            for gram in entry.findall('./gramGrp/gramGrp/gram'):
                if gram.get('type') == "Joma" and gram.text == "Medicīna":
                    output.write(entry.get('sortKey') + "\n")
                    terms.append(entry.get('sortKey'))
            for gram in entry[0].findall('./gramGrp/gramGrp/gram'):
                if gram.get('type') == "Joma" and gram.text == "Medicīna":
                    output.write(entry.get('sortKey') + "\n")
                    terms.append(entry.get('sortKey'))

    output.close()
    print("Medicīniskie termini atrasti!")
    return terms


medical_terms = get_tezaurs_medical_terms()


# Append single source text to end of text file.
def append_file(text):
    output = open(constants.output_text, 'a', encoding="utf-8")
    for sentence in text:
        output.write(sentence + "\n")
    output.write("\n")


# Check if the text contains medical terminology
def is_medical(source, lemmas, terms):
    score = 0
    for word in lemmas:
        if word in terms:
            score += 1
    if score >= 1:
        return True
    else:
        return False


# Read the document splitting it by sentences.
# @param text - list of strings, each corresponding to a sentence, from one source
def read_doc(corpus, source):
    text = []
    lemmas = []
    sentence = ""
    while True:
        # Get next line from file
        line = corpus.readline()

        if line[0] == "<" and line[1] != "\t":
            if line[:6] == "</doc>":
                if sentence[:-1] == " ":
                    sentence = sentence[:-1]
                break
            elif line[:5] == "<g />" and len(sentence) > 1:
                if sentence[-1] == " ":
                    sentence = sentence[:-1]
            elif line[:3] == "<s>":
                sentence = ""
            elif line[:4] == "</s>":
                if sentence[-1] == " ":
                    sentence = sentence[:-1]
                text.append(sentence)
                sentence = ""
            else:
                continue
        else:
            sentence = sentence + line.split("\t")[0] + " "
            lemmas.append(line.split("\t")[2].strip("\n"))

    if is_medical(source, lemmas, medical_terms):
        append_file(text)


# Clear previous data
def clear_output_file():
    out = open(constants.output_text, 'w', encoding="utf-8")
    out.write("")
    out.close()


# Atlasam tikai dokumentus, kas satur medicīnisku terminu
def conjoiner():

    print("Reading documents...")
    # Clear the output file of previous data
    clear_output_file()

    # Read the corpus vert file
    corpus = open(constants.vert_file, 'r', encoding="utf-8")

    # Read file line by line
    line = corpus.readline()
    while line:
        # Get next line from file
        if line[:12] == "<doc source=":
            source = line.split("\"")[1]
            read_doc(corpus, source)
        line = corpus.readline()

    corpus.close()
    print("Document reading complete!")


conjoiner()
