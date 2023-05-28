import csv
import pandas as pd
from split_data import split_main
from random import random, randint

input_corpus = "data/medical_documents.vert"
input_medical_csv = "data/rakus_terms.csv"

output_dir = "output/dataset/generated/"
short = "abbr"
fullt = "full"
output_shorttext = output_dir + short + ".txt"
output_fulltext = output_dir + fullt + ".txt"


# Clear previous data
def clear_output_file(file):
    out = open(file, 'w', encoding="utf-8")
    out.write("")
    out.close()


# Append single source text to end of text file.
def append_file(text, file):
    output = open(file, 'a', encoding="utf-8")
    for sentence in text:
        output.write(sentence)
    output.close()


# RAKUS saīsinājumu ieguve
def get_medical_csv():
    terms = []
    abbrevs = []
    medical = pd.read_csv(input_medical_csv)
    for x in medical["lemma"]:
        terms.append(x)
    for y in medical["vārds"]:
        abbrevs.append(y)
    print("Medicīniskie termini atrasti!")
    return terms, abbrevs


# Check if text contains a Tēzaurs medical term
def is_medical(lemmas, terms):
    score = 0
    for word in lemmas:
        if word in terms:
            score += 1
    if score >= 1:
        return True
    else:
        return False


medical_terms, medical_abbrevs = get_medical_csv()


# Read document by sentence
def read_doc(corpus, line):
    add_to_csv = False
    skip_chance = 0.2
    text = []
    forms = []
    lemmas = []
    copy = []
    text.append(line)

    # Continue reading text until end of sentence
    while True:
        line = corpus.readline()
        text.append(line)
        if line[0] == "<" and line[1] != "\t":
            if line[:4] == "</s>":
                break
            else:
                continue
        else:
            forms.append(line.split("\t")[0].strip("\n"))
            lemmas.append(line.split("\t")[2].strip("\n"))

    # Ja oriģinālais teikums satur jau savērstu RAKUS saīsinājumu, teikums tiek ignorēts
    for form in forms:
        if form in medical_abbrevs:
            return

    # Šeit tiek definēta teksta savēršana.
    og_text = text.copy()
    for x in range(len(text)):
        if x > len(text) - 1:
            break
        if len(text[x].split("\t")) == 3:
            lemma = text[x].split("\t")[2].strip("\n")
            randomizer = random()
            for c in medical_terms:
                # Vispirms meklējam vairākvārdu terminus
                if len(c.split(" ")) > 1:
                    term_split = c.split(" ")
                    all_match = True
                    for d in range(len(term_split)):
                        if len(text[x + d].split("\t")) != 3:
                            all_match = False
                            break
                        lemma = text[x + d].split("\t")[2].strip("\n")
                        if term_split[d] != lemma:
                            all_match = False
                            break
                    if all_match:
                        add_to_csv = True
                        if randomizer > (skip_chance / len(term_split)):
                            lemma_occur = []
                            for index, y in enumerate(medical_terms):
                                if y == c:
                                    lemma_occur.append(index)
                            chosen = lemma_occur[randint(0, len(lemma_occur)-1)]
                            copy = text.copy()
                            contracted = medical_abbrevs[chosen]
                            text = copy[:x] + [contracted + "\ty\t" + contracted + "\n"] + copy[x+d+1:]
            # Pēc vairākvārdu terminu pārlases meklējam vienvārdīgus terminus
            if lemma in medical_terms:
                add_to_csv = True
                if randomizer > skip_chance:
                    # chosen = medical_terms.index(lemma)
                    lemma_occur = []
                    for index, y in enumerate(medical_terms):
                        if y == lemma:
                            lemma_occur.append(index)
                    chosen = lemma_occur[randint(0, len(lemma_occur)-1)]
                    contracted = medical_abbrevs[chosen]
                    # Randomizing capitalization and punctuation
                    randomizer = random()
                    if contracted[0].islower() and randomizer > 0.5:
                        contracted = contracted[0].upper() + contracted[1:]
                    randomizer = random()
                    if contracted[-1] == "." and randomizer > 0.5:
                        contracted = contracted[:-1]
                    # End of randomization
                    text[x] = contracted + "\ty\t" + contracted + "\n"

    # CSV failā rakstām saīsināto un oriģinālo teikumu kā pāri
    if add_to_csv:
        append_file(text, output_shorttext)
        append_file(og_text, output_fulltext)


# Reads input corpus, calls other functions from here
def conjoiner():
    print("Reading documents...")
    # Clear the output file of previous data
    clear_output_file(output_shorttext)
    clear_output_file(output_fulltext)

    # Read the corpus vert file
    corpus = open(input_corpus, 'r', encoding="utf-8")

    print("Starting search of medical documents...")
    # Read file line by line
    line = corpus.readline()
    while line:
        if line[:3] == "<s>":
            read_doc(corpus, line)
        line = corpus.readline()

    corpus.close()
    print("Document reading complete!")


# Merge sentences in vert file format to one line string
def merge_file_text(file, output_loc):
    # Change this between [0, 1, 2]
    output_type = 0

    print("Reading document: " + file)
    text = open(file, 'r', encoding="utf-8")
    print("Starting sentence merging...")
    output = open(output_loc, 'a', encoding="utf-8")
    sentence = ""

    line = text.readline()
    while line:
        # Get next line from file
        if line[:3] == "<s>":
            sentence = ""
        elif line[:4] == "</s>":
            sentence = sentence[:-1]
            output.write(sentence + "\n")
            sentence = ""
        elif line[0] == "<":
            pass
        else:
            sentence += line.split("\t")[output_type].strip("\n") + " "
        line = text.readline()
    print("Merge completed succesfully!")


# Pilnā savēršana visiem train, valid un train datu failiem.
def merge_both(out_dir, out_short, out_fullt, data_set):
    input_abbr = "{}div/{}/{}.txt".format(out_dir, data_set, out_short)
    input_full = "{}div/{}/{}.txt".format(out_dir, data_set, out_fullt)

    output_abbr = "{}div/{}_{}.txt".format(out_dir, data_set, out_short)
    output_full = "{}div/{}_{}.txt".format(out_dir, data_set, out_fullt)
    output_join = "{}csv/{}.csv".format(out_dir, data_set)

    clear_output_file(output_abbr)
    clear_output_file(output_full)
    clear_output_file(output_join)

    merge_file_text(input_abbr, output_abbr)
    merge_file_text(input_full, output_full)

    join_csv(output_abbr, output_full, output_join)


def join_csv(file_a, file_b, outfile):
    print("Reading document: " + file_a)
    text_a = open(file_a, 'r', encoding="utf-8")
    print("Reading document: " + file_b)
    text_b = open(file_b, 'r', encoding="utf-8")

    outputy = open(outfile, 'w', newline='', encoding='utf-8-sig')
    csvout = csv.writer(outputy, quoting=csv.QUOTE_ALL)
    csvout.writerow(['source', 'target'])

    line_a = text_a.readline()
    line_b = text_b.readline()
    while line_a:
        csvout.writerow([line_a.strip("\n"), line_b.strip("\n")])
        line_a = text_a.readline()
        line_b = text_b.readline()
    outputy.close()
    text_a.close()
    text_b.close()


def main():
    conjoiner()
    split_main(output_shorttext, output_fulltext, output_dir + "div/", short, fullt)
    merge_both(output_dir, short, fullt, "test")
    merge_both(output_dir, short, fullt, "train")
    merge_both(output_dir, short, fullt, "valid")


if __name__ == '__main__':
    main()
