import torch
from transformers import MT5Tokenizer, MT5ForConditionalGeneration
from datasets import load_dataset
from timeit import default_timer as timer

model_dir = "./results/base-1/checkpoint-161670"
model_type = "google/mt5-base"


def run_cpu_1000(model, tokenizer, testing):
    device = torch.device('cpu')
    model = model.to(device)
    
    for x in range(1000):
        task_prefix = ""
        text_to_rewrite = testing['test']['source'][x]
        text_to_rewrite = task_prefix + text_to_rewrite 

        input_text = tokenizer(text_to_rewrite, return_tensors="pt").to(device)
        translation = model.generate(input_text["input_ids"], max_length=128, num_beams=4, early_stopping=True)
        decoded_translation = tokenizer.decode(translation[0], skip_special_tokens=True)


def run_gpu_1000(model, tokenizer, testing):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    for x in range(1000):
        task_prefix = ""
        text_to_rewrite = testing['test']['source'][x]
        text_to_rewrite = task_prefix + text_to_rewrite 

        input_text = tokenizer(text_to_rewrite, return_tensors="pt").to(device)
        translation = model.generate(input_text["input_ids"], max_length=128, num_beams=4, early_stopping=True)
        decoded_translation = tokenizer.decode(translation[0], skip_special_tokens=True)
        

def speed_test():
    # Load the model
    model = MT5ForConditionalGeneration.from_pretrained(model_dir)
    # Tokenize the dataset
    tokenizer = MT5Tokenizer.from_pretrained(model_type)
    # Load dataset
    testing = load_dataset('csv', data_files={'test': 'dataset/test.csv'})

    start = timer()
    run_cpu_1000(model, tokenizer, testing)
    print("without GPU:", timer() - start)

    start = timer()
    run_gpu_1000(model, tokenizer, testing)
    print("with GPU:", timer() - start)
    
    
speed_test()
