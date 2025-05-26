from datasets import load_dataset
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments

# Load dataset
dataset = load_dataset("cnn_dailymail", "3.0.0")

# Load model & tokenizer
model_name = "google/pegasus-cnn_dailymail"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

# Tokenize function
def preprocess(data):
    inputs = tokenizer(data["article"], truncation=True, padding="max_length", max_length=512)
    with tokenizer.as_target_tokenizer():
        targets = tokenizer(data["highlights"], truncation=True, padding="max_length", max_length=128)
    inputs["labels"] = targets["input_ids"]
    return inputs

# Tokenize datasets
tokenized_dataset = dataset.map(preprocess, batched=True)

# Training args
training_args = TrainingArguments(
    output_dir="./pegasus_cnn_dailymail_finetuned",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=1,
    logging_steps=10,
    evaluation_strategy="steps",
    save_steps=500,
    save_total_limit=1,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
)

# Train
trainer.train()

# Save
trainer.save_model("./pegasus_cnn_dailymail_finetuned")
tokenizer.save_pretrained("./pegasus_cnn_dailymail_finetuned")
