class KnowledgeBaseRetriever:
    def __init__(self, retriever) -> None:
        self.retriever = retriever

    def retrieve_kb_level_1(self, inputs):
        docs = self.retriever.invoke(inputs["question"])
        return "\n\n".join(doc.page_content for doc in docs)

    def retrieve_kb_level_2(self, inputs):
        docs = self.retriever.invoke(inputs["question"])
        return "\n\n".join(doc.page_content for doc in docs)
