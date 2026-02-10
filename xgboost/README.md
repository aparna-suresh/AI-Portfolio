### Efficient classification using embedding models in a resource constrained environment

This project demonstrates an end-to-end pipeline for predicting Amazon product ratings from text reviews. 

Faced with local hardware constraints, I implemented advanced model optimization techniques—including ONNX Runtime, INT8 Quantization,
and PCA—to achieve high-performance inference on a standard machine without sacrificing significant accuracy.

#### Key Highlights

**Model Optimization:** Converted bert-base-uncased to ONNX format, and applied 8-bit integer quantization that reduced the model size 
by 4x ( 425 MB to 107MB), while also speeding up the inference time.

**Dimensionality Reduction:** Used PCA to reduce embedding dimensions from 768 to 400, which significantly 
reduced the computational load for the classification head, while maintaing the performance.

### Dataset & Challenges

**Source:** Amazon Reviews 2023 (Handmade Products subset) containing ~600k reviews.

**Class Imbalance:** Highly skewed data where 79% of reviews are 5-star ratings, while 2-star and 3-star ratings comprise only 3% each.

**Data Cleaning:** Implemented a custom pipeline to handle repeated punctuation, emoji removal (de-emojized), 
HTML tag stripping, and deduplication of common generic reviews (e.g., "Good product").

### Technical Stack
Embeddings: BERT (bert-base-uncased) via Hugging Face.

Inference Engine: ONNX Runtime with OptimizationConfig.

Classifier: XGBoost with a weighted DMatrix to handle class imbalance.

Tuning: Hyperopt for Bayesian hyperparameter optimization.

EDA and model evaluation: Pandas, PyArrow, Scikit-Learn.

### Performance Results

Despite the significant reduction in model size and complexity, the system achieved a Weighted F1-Score of 0.80.

| Metric | Score |
| :--- | :--- |
| Accuracy | 53.9% |
| Precision (Weighted) | 	0.841 | 
| Recall (Weighted) |  0.778 | 
| F1-Score (Weighted) |  0.804 | 

**Note on PCA:** Reducing the embedding size from 768 to 400 resulted in a negligible accuracy drop of < 0.3 %,
proving that lower-dimensional representations can significantly speed up training without compromising on quality.
