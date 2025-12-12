KoBERT-Based Text Classification

This project trains a Korean text classification model using KoBERT.
Given an input sentence, the model predicts one of several predefined categories.
Training data is provided as a CSV file containing sentences and their labels.

Overview

Model: KoBERT (Korean BERT variant)

Task: Sentence classification

Input Format: CSV (sentence, label)

Output: Fine-tuned KoBERT model capable of predicting categories for new sentences

Training Pipeline
1. Tokenization

Each sentence is tokenized into subword units using the BERT tokenizer.

Example sentence:
"숙소가 깨끗하고 서비스가 좋았습니다."

Tokenized output:
["[CLS]", "숙소", "가", "깨끗", "##하", "고", "서", "##비", "##스", "가", "좋", "##았", "##습", "##니다", ".", "[SEP]"]

Generated features:

input_ids

attention_mask

token_type_ids

2. Transformer Encoder (KoBERT)

The tokenized sequence is processed by the KoBERT encoder.
Through self-attention and feed-forward layers, each token becomes a contextualized embedding.
For classification, the model uses the [CLS] token vector or a pooled output.

3. Classification Head

A linear classifier is added on top of the KoBERT output.

Structure:
Linear (hidden_size → num_categories)

The output consists of logits representing the score for each category.

4. Training Procedure

Forward pass

Sentence → KoBERT → [CLS] vector → Classifier → Logits

Loss calculation

Cross-Entropy Loss comparing logits and CSV labels

Backpropagation and optimization

Updates both the KoBERT encoder and the classification layer

Epoch iteration

Repeats over the full dataset to improve performance
