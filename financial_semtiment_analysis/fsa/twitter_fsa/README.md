Financial Sentiment Analysis
Project Overview
This project classifies financial tweets into Bearish (0), Bullish (1), or Neutral (2) sentiments. In a real-life scenario, most of the tweets remain neutral and very few tweets indicate rare market signals. This implementation is specifically optimized for such scenarios to detect rare but important Bearish or Bullish signals in a highly imbalanced environment.
Key Objectives
•	Contextual Nuance: Moving beyond keyword matching to understand financial metaphors (e.g., distinguishing between "rising prices" as a success vs. "rising crisis").
•	Handle Data Imbalance: Addressing a dataset where 64% of instances are Neutral, ensuring rare signals are not ignored.
•	Interpretability: Using SHAP to audit the model's "internal attention" and verify it focuses on financial keywords rather than noise.
Tech Stack
•	Language: Python
•	Embedding model: Fine-tuned DistilBERT (Hugging Face)
•	Explainable AI: SHAP 
•	Data Processing: Pandas, NumPy, Scikit-learn
Data & EDA
The project uses the zeroshot/twitter-financial-news-sentiment dataset, consisting of 9,543 training and 2,388 validation samples.
Text Preprocessing
•	Ticker Normalization: Replaced stock tickers with generic tags to prevent the model from associating specific company names with fixed sentiments.
•	URL Sanitization: Replaced URLs with HTTPS_URL to reduce token consumption and force the model to look at the tweet's actual meaning.
Model Performance & Optimization
Standard models often achieve high accuracy by simply guessing the major class, which in this case is "Neutral". 
To overcome, this project uses weighted Cross Entropy loss that gives more weight to the minority classes, forcing the model to learn the nuances in the minority classes.
The project also employs a rigorous evaluation metrics that reflects both the real-world performance of the model and the efficiency of the model in identifying minority classes.
Metric		Baseline score – TF-IDF + Logistic regression	PEFT - Distilbert
F1 - Weighted	Mimics the real-world performance, where most of the tweets are neutral	0.808	0.8685
F1 - Macro	Ensures the model can identify the rare “Bearish” and “Bullish” signals	0.751	0.822

Model Interpretability (SHAP)
We used SHAP to visualize how specific words push a prediction toward a specific sentiment.
Success Cases:
For eg: in the correctly classified Bearish tweet, “Trade, U.S. Elections Are Top Market Risks, Says Goldman Sachs s Moe”, the model correctly placed more emphasis on “risks” than any other word, thereby correctly predicting it as “Bearish”.
Similarly in the correctly classified bullish sample “The number of customers canceling Netflix hasn t accelerated around the debut of rival services from Disney and App  HTTPS_URL”, although the model places a significant emphasis on “canceling”, it is outweighed by the attention on words “hasn’t accelerated”, thereby correctly predicting it as “Bullish”.
Edge Cases:
 However, it was observed that the model in general struggles with the generic meaning of the word in the financial context.
For eg: In the Bearish tweet, “Spanish Farmers Rise Up Against Unfair Prices Amidst Thee Worst Agri Food Crisis In Decades”, the model inadvertently placed more emphasis on “Rise up” rather than “Crisis”. This resulted in the tweet being misclassified as “Bullish”.
Similarly, in the Bullish tweet, “Stock Traders Are Dumping Virus Hedges After Peak Fear Passes”, the model places more emphasis on “Dumping Virus Fear”, resulting in the tweet being misclassified as Bearish.
 Future Improvements
•	Using Domain Specific Models: Further fine-tuning the model on domain specif corpus to better handle jargons like “Dumping Virus Hedges”.
•	Real-time API: Transitioning the model into a streaming service for live market monitoring.

