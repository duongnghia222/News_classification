from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import torch
from transformers import AutoTokenizer
import numpy as np
from article_classifier import ArticleClassifier


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Load your tokenizer

checkpoint_model = "vinai/phobert-base-v2"
tokenizer = AutoTokenizer.from_pretrained(checkpoint_model)

config = {
    'model_name': checkpoint_model,
    'n_labels': 156,

}

# Load your model and LabelEncoder
model = ArticleClassifier(config)
model.load_state_dict(torch.load('NPL_news_classification_best_model.pt', map_location=device))
model.eval()
le = joblib.load('label_encoder.joblib')

app = FastAPI()


class Item(BaseModel):
    text: str

@app.get("/")
async def home():
    return "News Classification"


@app.post("/predict")
async def predict(item: Item):
    # Tokenize your data
    encoding = tokenizer.encode_plus(
        item.text,
        add_special_tokens=True,
        truncation=True,
        max_length=256,
        return_token_type_ids=False,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt',  # Return PyTorch tensors
    )

    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad():
        logits = model(input_ids, attention_mask)

    logits = logits.detach().cpu().numpy()

    # Get the predicted label
    predicted_label = np.argmax(logits, axis=1)
    output_label = le.inverse_transform(predicted_label)

    return {"prediction": output_label[0]}



