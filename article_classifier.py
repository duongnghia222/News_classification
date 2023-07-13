import torch
from torch import nn
from transformers import AutoModelForSequenceClassification
import pytorch_lightning as pl


class ArticleClassifier(pl.LightningModule):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.bert = AutoModelForSequenceClassification.from_pretrained(config['model_name'],
                                                                       num_labels=config['n_labels'])
        self.loss = nn.CrossEntropyLoss()

    def forward(self, input_ids, attention_mask):
        x = self.bert(input_ids, attention_mask).logits
        return x

