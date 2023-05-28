
from keybert import KeyBERT

in_file = "data/medical_documents.txt"
out_file = "output/texts_basic.txt"
out_file2 = "output/texts_medic.txt"
medical_terms = "data/medical_terms_full.txt"


# Clear previous data
def clear_file(file):
    out = open(file, 'w', encoding="utf-8")
    out.write("")
    out.close()


# Parsing the Tēzaurs data set
def get_medical_terms():
    terms = []
    term_list = open(medical_terms, 'r', encoding="utf-8")
    line2 = term_list.readline()

    while line2:
        terms.append(line2.strip("\n"))
        line2 = term_list.readline()
    term_list.close()
    print("Medicīniskie termini atrasti!")
    return terms


def medical(n):
    med_terms = get_medical_terms()
    clear_file(out_file)
    clear_file(out_file2)

    input_file = open(in_file, "r", encoding="utf-8")
    output_file = open(out_file, "a", encoding="utf-8")
    output_file2 = open(out_file2, "a", encoding="utf-8")
    kw_model = KeyBERT()

    line = input_file.readline()
    document_count = 0
    medic_doc_count = 0
    while line:
        document_count += 1
        doc = line
        keywords = kw_model.extract_keywords(doc, top_n=n)

        keys = [item[0] for item in keywords]
        medical = False
        if any(x in med_terms for x in keys):
            medical = True
            medic_doc_count += 1
            output_file2.write(line)
        else:
            # medic_doc_count += 1
            output_file.write(line)

        text = "(" + str(medic_doc_count) + ") " + str(medical) + ":" + str(keys) + "\n"
        print(text)
        line = input_file.readline()

        # if medic_doc_count > 5000:
        #     break

    print("Finished analysing documents!")
    print("Medical terms as keywords found in {} / {} documents!".format(medic_doc_count, document_count))
    # keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words=None)


medical(10)
