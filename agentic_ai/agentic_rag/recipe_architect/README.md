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

### Sample Queries and Routing

| Query Type | Route | Example |
| :--- | :--- | :--- |
| **Recipe Search** | Vector Store (RAG) | "Quick, healthy breakfast" |
| **Culinary Science** | Generic Search | "What is the smoking point of oil?" |
| **Basic Cooking Techniques** | Generic Search | "How to boil an egg?" |

### System Reasoning Examples

<details>
<summary><b>Scenario: Constraint Relaxation (Click to expand)</b></summary>

**Input:** "Quick vegan gluten free pasta nut free"

**Process:** 

1. Routing: vectorstore.
   
2. Meta data extraction: {'category': 'Grains and Pasta', 'is_nut_free': 1, 'is_gluten_free': 1, 'is_quick': 1}
   
3. Retrieve and re-rank: 10 documents were retrieved and re-ranked.
   
4. Grading: None of the documents passed the grader.
   
   Sample Grading output: Grader output:
   
   [Grade(title='Vegetarian Lasagna', analysis='Meets dietary constraints (vegan, gluten-free, nut-free) but contains non-vegan ingredients (egg, cheese).', score=2),    Grade(title='Spinach, Tomato, And Pine Nut Fettuccine', analysis='Contains pine nuts which violates nut-free requirement, though otherwise meets dietary needs.', score=0), Grade(title='Cheese Noodles', analysis='Meets dietary constraints (gluten-free, nut-free) but contains dairy, violating vegan requirement.', score=2)]
   
5. Query Reformulation: The re_query, identified that is_quick is the most restrictive constraint and removed it.
   
   Sample output: Requery Reasoning: The original query required all four constraints: category, nut-free, gluten-free, and quick. The most restrictive among them is the quick constraint, which limits the result set to only recipes that can be prepared quickly. By relaxing this constraint (removing is_quick), we broaden the search while still enforcing the mandatory dietary safety rules (nut-free and gluten-free) and the category requirement. This adjustment should yield more matching results for a quick vegan gluten‑free pasta nut‑free query.
   
   Requery relaxed_filters: {'category': 'Grains and Pasta', 'is_nut_free': 1, 'is_gluten_free': 1}

6. Grading Attempt 2: Here the grader threshold is lowered to 3 to let recipes that meets mosts of the user's constraints pass through
   
7. Answer Generation: The node outputs the recipe but with dietery and typo notes.
   
                  1) Vegetarian Soba Noodle Salad\n'
      
                  '- **[DIETARY NOTE]:** This recipe is gluten-free and nut-free. '
                  'However, it contains honey (not vegan) and soy sauce (check '
                  'for gluten-free certification). For vegan version, '
                  'substitute honey with maple syrup or agave nectar.\n'
      
                  '- Prep/Cook Time: Not specified\n'
                  '- Ingredients:\n'
                  '  - 2 Tablespoons Prepared Ponzu Sauce\n'
                  '  - 1 Tablespoon Low Sodium Soy Sauce (ensure gluten-free)\n'
                     ....
      
                  '  - 18 teaspoons Toasted Sesame Seeds\n'
                  '  - **[TYPO NOTE]:** Context says 18 teaspoons sesame seeds, '
                  'likely 1.5-2 tablespoons\n'
                  '\n'
                  '- Directions:\n'
                  '  1. Whisk together the vinaigrette ingredients in a small '
                  'bowl.\n'
                  '  2. Season with additional kosher salt and black pepper as '
                  'needed.\n'
</details>

<details>
<summary><b>Scenario: Use of an ingredient in a recipe (Click to expand)</b></summary>


**Input:** "What is the use of corn in Tamale Bake?"

**Process:** 

1. Routing: vectorstore.
   
2. Meta data extraction: {'category': 'Mains'}
   
3. Retrieve and re-rank: Although 10 docs were retrieved only 1 document passed through the re-ranker with score threshold
   
4. Grading: None of the documents passed the grader.
   
   Grading output: 
   
   Grader output: [Grade(title='Roasted Corn on the Cob With Chilli Lime Butter', analysis="The document discusses a corn dish but is about roasted corn on the cob, not tamale bake, and doesn't address the use of corn in tamale bake.", score=1)]
   
5. Query Reformulation: The re_query, identified that category is most restrictive constraint and removed it.
   
   Requery Reasoning: The original query failed because the category filter was too restrictive, limiting results to Mains only, which excluded relevant information about corn usage in Tamale Bake that may appear in other categories. The category constraint is removed to broaden the search while keeping dietary safety rules intact.
Requery relaxed_filters: {}

6. Retreiver and Re-Ranker attempt 2: With the category constraint removed, the retriever was able to retrieve the specific "Tamale Bake" recipe with 9 other recipes. However the re-ranker correctly identified only "Tamale Bake" matches. It filtered out all the other recipes and let only Tamale Bake pass through.
   
7. Grading Attempt 2:
   [Grade(title='Tamale Bake', analysis='The document directly addresses the use of corn in Tamale Bake, listing it as an ingredient and showing its incorporation in the recipe.', score=5)]
   
9. Answer Generation: The node outputs the use of corn in Tamale Bake.
   
                  1. 'In the Tamale Bake recipe, corn is used in two ways:\n'
                  '\n'
                  '1. As an ingredient in the meat mixture:\n'
                  '   - 1 c. corn is added to the browned beef, onions, and '
                  'tomatoes mixture along with half of the olives (steps '
                  '9-11)\n'
                  '\n'
                  '2. As part of the corn muffin topping:\n'
                  '   - The Jiffy corn muffin mix (which contains cornmeal) is '
                  'prepared separately and used as a topping for the casserole '
                  '(steps 12-17)'

</details>

