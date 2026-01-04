from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import pandas as pd


class ChromaVectorStore:
    @staticmethod
    def build_vector_store(
        data_path: str = "./data/agricultural_knowledge_base.json",
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> Chroma:
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

        vector_store = Chroma(
            embedding_function=embeddings,
        )

        df = pd.read_json(data_path)

        df["combined_text"] = df.apply(
            lambda row: f"{row['question']}\n\n{row['answer']}",
            axis=1,
        )

        documents = []

        for _, row in df.iterrows():
            metadata = {
                "id": row["id"],
                "category": row["category"],
                "tags": (
                    ", ".join(row["tags"])
                    if isinstance(row["tags"], list)
                    else row["tags"]
                ),
                "related_sensor_checks": (
                    ", ".join(row["related_sensor_checks"])
                    if isinstance(row.get("related_sensor_checks"), list)
                    else None
                ),
            }

            documents.append(
                Document(
                    page_content=row["combined_text"],
                    metadata=metadata,
                )
            )

        vector_store.add_documents(documents)

        return vector_store

    @staticmethod
    def get_retriever(
        vector_store: Chroma,
        k: int = 5,
    ):
        """
        Returns a retriever from an existing vector store.
        """
        return vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
        )
