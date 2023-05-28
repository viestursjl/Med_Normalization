import torch
from transformers import MT5Tokenizer, MT5ForConditionalGeneration, Adafactor, Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq, EarlyStoppingCallback
from transformers.training_args import IntervalStrategy
from datasets import load_dataset

model_type = "mT5-base"
output_dir = "./results/base-1"

# Load the dataset
dataset = load_dataset('csv', data_files={'train': 'dataset/train.csv', 'validation': 'dataset/valid.csv'})

# Tokenizer function
def tokenize_data(example):
    source = tokenizer(example['source'], truncation=True, padding='max_length', max_length=128)
    target = tokenizer(example['target'], truncation=True, padding='max_length', max_length=128)
    return {'input_ids': source['input_ids'], 'attention_mask': source['attention_mask'], 'labels': target['input_ids']}

# Tokenize the dataset
tokenizer = MT5Tokenizer.from_pretrained(model_type)
tokenized_datasets = dataset.map(tokenize_data, batched=True)

# Load the model
model = MT5ForConditionalGeneration.from_pretrained(model_type)

# Training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./results/small-2",
    evaluation_strategy=IntervalStrategy.EPOCH,
    save_strategy=IntervalStrategy.EPOCH,
    learning_rate=2e-5,
    warmup_steps=1000,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=16,
    num_train_epochs=20,
    weight_decay=0.01,
    save_total_limit=3,
    load_best_model_at_end=True,
    metric_for_best_model="loss",
)

# Initialize the trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)

# Train the model
trainer.train()

# Save the model after training
trainer.save_model("./results/small-2")
