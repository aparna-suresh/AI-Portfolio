import chromadb
from langchain_chroma import Chroma
from langchain_classic.retrievers import EnsembleRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
import pickle


class RecipeRetriever:
    def __init__(self):
        self.re_rank_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.chroma_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2",
                                                       model_kwargs={'device': "cuda"},
                                                       encode_kwargs={'normalize_embeddings': False})
        self.bm25_retriever = self.get_bm25_retriever()
        self.semantic_retriever = self.get_semantic_retriever()
        self.hybrid_retriever = self.get_hybrid_retriever()
        self.filter_names = {
            'is_nut_free': ["Contains nuts", "Nut free"],
            'is_gluten_free': ["Contains Gluten", "Gluten free"],
            'is_dairy_free': ["Contains Dairy", "Dairy free"],
            'is_spicy_food': ["Not spicy food", "Spicy food"],
            'is_comfort_food': ["Not comfort food", "Comfort food"],
            'is_light_food': ["Not light food", "Light food"],
            'is_hearty_food': ["Not hearty food", "Hearty food"],
            'is_healthy': ["Not healthy food", "Healthy food"],
            'is_breakfast': ["Not breakfast", "Breakfast"],
            'is_lunch': ["Not lunch", "Lunch"],
            'is_dinner': ["Not Dinner", "Dinner"],
            'is_no_oven': ["Uses Oven", "No oven"],
            'is_slow_cooker': ["Uses Slow Cooker", "No slow cooker"],
            'is_air_fryer': ["Uses air fryer", "No air fryer"],
            'is_one_pot': ["Uses One pot", "No One pot"],
            'is_quick': ["Not quick", "Quick"],
        }

    def get_bm25_retriever(self, path="data/bm25_retriever.pkl"):
        with open(path, "rb") as f:
            bm25_retriever = pickle.load(f)
        print("Retriever loaded from disk.")
        return bm25_retriever

    def get_semantic_retriever(self):
        client_settings = chromadb.config.Settings(
            anonymized_telemetry=False,
            is_persistent=True
        )
        vector_store = Chroma(
            collection_name="recipe_dataset",
            embedding_function=self.chroma_embeddings,
            persist_directory="data",
            client_settings=client_settings,
        )

        semantic_retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        return semantic_retriever

    def get_hybrid_retriever(self, top_k=5, bm25_weight=0.4):
        self.bm25_retriever.k = top_k
        self.semantic_retriever.search_kwargs["k"] = top_k
        semantic_weight = 1 - bm25_weight
        hybrid_retriever = EnsembleRetriever(
            retrievers=[self.semantic_retriever, self.bm25_retriever],
            weights=[semantic_weight, bm25_weight]
        )
        return hybrid_retriever

    def get_results(self, question, meta_data_filters):
        print(f"get results: {meta_data_filters}")
        self.semantic_retriever.search_kwargs["filter"] = meta_data_filters
        docs = self.hybrid_retriever.invoke(question)
        formatted_docs = []
        for doc in docs:
            filtered_data = ""
            if meta_data_filters is not None and len(meta_data_filters) > 0:
                if "$and" in meta_data_filters:
                    and_query = meta_data_filters["$and"]
                else:
                    and_query = [meta_data_filters]
                for meta_data in and_query:
                    for f_key in meta_data.keys():
                        if f_key in self.filter_names:
                            filtered_data += f"{self.filter_names[f_key][doc.metadata[f_key]]}, "
                        else:
                            filtered_data += f"{f_key} : {doc.metadata[f_key]}, "
            header = f"--- STATUS: {filtered_data} ---"
            formatted_content = f"{header}\n{doc.page_content}"
            print(header + "\n" + doc.metadata["title"])
            formatted_docs.append(formatted_content)
        return formatted_docs

    def re_rank(self, query, query_result, check_score=True):
        # cross-encoder re-ranker
        ranks = self.re_rank_model.rank(query, query_result)
        if ranks[0]["score"] < 0:
            return [query_result[ranks[0]["corpus_id"]]]
        reranked_docs = []
        for rank_score in ranks:
            if check_score and rank_score["score"] < 0:
                continue
            else:
                reranked_docs.append(query_result[rank_score["corpus_id"]])
        return reranked_docs
