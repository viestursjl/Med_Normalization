import torch
from transformers import MT5Tokenizer, MT5ForConditionalGeneration
from datasets import load_dataset

model_dir = "./results/base-1/checkpoint-161670"
model_type = "google/mt5-base"

# Load the model
model = MT5ForConditionalGeneration.from_pretrained(model_dir)
# Tokenize the dataset
tokenizer = MT5Tokenizer.from_pretrained(model_type)
# Load dataset
testing = load_dataset('csv', data_files={'test': 'dataset/test.csv'})
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

correct = 0
for x in range(len(testing['test']['source'])):
    # Set the text to be transformed
    task_prefix = ""
    text_to_rewrite = testing['test']['source'][x]
    text_to_rewrite = task_prefix + text_to_rewrite 

    # Tokenize the input text
    input_text = tokenizer(text_to_rewrite, return_tensors="pt").to(device)
    # Generate transformation
    translation = model.generate(input_text["input_ids"], max_length=128, num_beams=4, early_stopping=True)
    # Decode the translation
    decoded_translation = tokenizer.decode(translation[0], skip_special_tokens=True)

    if decoded_translation.replace(" ","") == testing['test']['target'][x].replace(" ",""):
        correct += 1
    else:
        print("\n{}\n{}".format(decoded_translation, testing['test']['target'][x]))

print("\nFully correct: {}% ({}/{})".format(correct*100/len(testing['test']['source']), correct, len(testing['test']['source'])))