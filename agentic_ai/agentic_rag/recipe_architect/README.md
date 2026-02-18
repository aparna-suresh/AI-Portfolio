### Agentic Recipe Intelligence System (Self-RAG)
Adaptive Agentic RAG system with self-correction loop that provides recipe recommendations and culinary insights 
from a dataset of 77,000 recipes.

### Key Features

**Intelligent Routing**: Automatically distinguishes between recipe-specific queries and general culinary knowledge 
(food science, food history, basic cooking techniques) using a specialized router node.

**Multi-Stage Retrieval & Reranking:** Employs a hybrid retriever (BM25 + Semantic Search) with a Cross-Encoder reranker 
to ensure the most relevant recipes are prioritized.

**Adaptive Metadata Filtering:** Dynamically extracts and applies rule-based filters such as dietary constraints (GF, Vegan, Nut-free), 
equipment (Air Fryer, Slow Cooker, one-pot), meal times, food preferences (light, hearty, healthy, comfort, spicy) and cook time(quick)

**Self-Correction Loop (Self-RAG):** Features a "Query Reformulation" node that relaxes non-critical constraints 
if initial results fail to meet thresholds.

**Handling Dietary restrictions and typos:** The generation node identifies potential data typos (e.g., 12 tsp vs 1/2 tsp pepper) 
and provides mandatory dietary safety notes.

### Technical Architecture
1. **Data Engineering & Processing**
   
      The system was distilled from an initial dataset of 2 million recipes.
      
      _Sampling_: 7,000 recipes were sampled from 11 broad categories (Baking, Mains, Vegan, etc.) to create a balanced 77k dataset.
      
      _Rule-Based Enrichment_: Applied deterministic rules to flag recipes for dietary needs, flavor profiles, and cooking equipment.
      
     _Vector Store_: Recipes are stored in ChromaDB using all-MiniLM-L12-v2 embeddings.     
      To maintain context integrity, recipes are stored as whole documents rather than chunks.

2. **The Agentic Workflow**
   
   _Analyze & Route:_ Mistral-Small determines if the query requires the vector_store or a generic_search.
   
   _Metadata Extraction:_ GPT-OSS-20B extracts structured metadata filters from the query.
   
   _Retrieve & Rerank:_ Hybrid search followed by a score-based reranking (threshold > 0).
   
   _Chain-of-Thought Grading:_ A large-scale model (Cogito-2.1) grades documents on a 0-5 scale with reasoning.
   
   _Query Reformulation:_ If no "perfect" (Score 5) matches are found, the system removes the most restrictive filter
     and retries with a lowered score threshold (Score >= 3).
   
    _Answer Generation:_ The final answer is generated with integrated typo-correction notes and dietary warnings.
   
### Tech Stack

Models: Cogito-2.1 (671B), GPT-OSS-20B, Mistral-Small.

Vector Database: ChromaDB.

Embeddings: Sentence Transformer all-MiniLM-L12-v2.

Frameworks: LangGraph / LangChain (Adaptive RAG).

