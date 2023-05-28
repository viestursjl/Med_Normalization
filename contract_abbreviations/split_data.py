# Import sklearn to handle the splitting of dataset into training testing
from sklearn.model_selection import train_test_split

# Split values
training = 0.9
valid = 0.1
testing = 0.1


# This function writes the split dataset sentences as a VERT formatted file
def write_txt(data, file):
    out = open(file, 'a', encoding="utf-8")
    for sentence in data:
        for word in sentence:
            out.write(word)
    out.close()


# This function splits the dataset sentences into train/test
def splitter(data_abbrev, data_fulltext, o_d, s, f):
    # Using scikit-learn library to split dataset
    x_train, x_test, y_train, y_test = train_test_split(data_abbrev, data_fulltext, test_size=testing,
                                                        train_size=training)
    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=valid, train_size=training)

    # Write all split data to txt files
    write_txt(x_train, o_d + "train/" + s + ".txt")
    write_txt(x_valid, o_d + "valid/" + s + ".txt")
    write_txt(x_test, o_d + "test/" + s + ".txt")

    write_txt(y_train, o_d + "train/" + f + ".txt")
    write_txt(y_valid, o_d + "valid/" + f + ".txt")
    write_txt(y_test, o_d + "test/" + f + ".txt")


# Clear previous data
def clear_output_file(file):
    out = open(file, 'w', encoding="utf-8")
    out.write("")
    out.close()


# Clear previous data
def clear_files(o_d, s, f):
    clear_output_file(o_d + "train/" + s + ".txt")
    clear_output_file(o_d + "valid/" + s + ".txt")
    clear_output_file(o_d + "test/" + s + ".txt")
    clear_output_file(o_d + "train/" + f + ".txt")
    clear_output_file(o_d + "valid/" + f + ".txt")
    clear_output_file(o_d + "test/" + f + ".txt")
    return


# Read chunk of sentences (max 10_000 sentences)
def read_sentences(file):
    sentences = []
    sentence = []
    # Perform dataset chunking otherwise too much data to store in memory
    while len(sentences) < 10_000:
        # Get next line from file
        line = file.readline()
        if line[:3] == "<s>":
            sentence = [line]
        elif line[:4] == "</s>":
            sentence.append(line)
            sentences.append(sentence)
        elif line:
            sentence.append(line)
        # if line is empty
        # end of file is reached
        elif not line:
            break

    # Split all the sentences into train/test (validation?)
    return sentences


# Read full dataset and call each individual dataset chunk
def read_full(file1, file2, o_d, s, f):
    count = 0
    print("Beginning to split full dataset!")
    while True:
        # Read chunk of sentences (max 10_000 sentences)
        # print("Chunk " + str(count))
        sentences1 = read_sentences(file1)
        sentences2 = read_sentences(file2)
        # Continue reading file by chunk until no more sentences to read
        # if len(sentences1) == 0:
        if not sentences1:
            break
        splitter(sentences1, sentences2, o_d, s, f)
        count += 1
    print("Dataset split successfully!")


# Main splitting function handles file storage & locations
def split_main(i_a, i_f, o_d, s, f):
    print("Reading documents...")
    # Clear the output file of previous data
    clear_files(o_d, s, f)
    # Read the corpus vert file
    corpus_abbrev = open(i_a, 'r', encoding="utf-8")
    corpus_fulltext = open(i_f, 'r', encoding="utf-8")

    # Read file line by line
    read_full(corpus_abbrev, corpus_fulltext, o_d, s, f)

    corpus_abbrev.close()
    corpus_fulltext.close()
    print("Document reading complete!")
