YAI Toy Project: KoBERT-Based Text Classification Training Pipeline
Overview

This project uses a Korean BERT variant (KoBERT) to train a text classification model that assigns each input sentence to one of the predefined categories.
Training data is provided in CSV format, where each sentence is paired with its corresponding label.

Training Pipeline
1) Tokenization

Input sentences are tokenized into subword units using the BERT tokenizer.

Example sentence:
"숙소가 깨끗하고 서비스가 좋았습니다."

Tokenized output:
["[CLS]", "숙소", "가", "깨끗", "##하", "고", "서", "##비", "##스", "가", "좋", "##았", "##습", "##니다", ".", "[SEP]"]

Each token is converted into an integer index (input_ids), and additional features such as attention_mask (to distinguish padding) and token_type_ids (sentence segment information) are generated.

2) Transformer Encoder (KoBERT)

The tokenized sequence is processed by the KoBERT Transformer encoder.

Through self-attention and feed-forward layers, each token becomes a context-rich embedding.

For classification, the model uses either the [CLS] token embedding or a pooled representation.

3) Classification Head

A classification layer (Linear layer) is added on top of the KoBERT output.

Structure: Linear (Hidden Dimension → Number of Categories)

The output is a set of logits (scores) for each category.
Example: 0 = Scenery, 1 = Service, 2 = Cleanliness, ...

4) Training Procedure

Forward Pass

Sentence → KoBERT Encoder → Extract [CLS] Vector → Classification Layer → Logits

Loss Calculation

Predictions vs ground-truth labels from the CSV

Loss function: Cross-Entropy Loss

Backward Pass & Optimization

Backpropagation updates both KoBERT and the classifier weights

Epochs

The entire dataset is trained for multiple epochs to gradually improve performance

Summary

Input Format: CSV (sentence + category label)

Pipeline: Sentence → Tokenization → KoBERT Encoder → [CLS] Vector → Classifier → Category

Goal: Convert semantic characteristics of sentences into embeddings to accurately predict categories

Final Output: A trained model that assigns the most likely category to any new input sentence
