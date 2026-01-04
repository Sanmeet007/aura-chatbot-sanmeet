from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from .prompts import level_1_prompt, level_2_prompt
from .kb_retrivers import KnowledgeBaseRetriever
from .chroma import ChromaVectorStore
from .farm_context import build_farm_context
from .diagnostic_rules import build_rule_context
from .llm import llm

vector_store = ChromaVectorStore.build_vector_store()
base_retriever = ChromaVectorStore.get_retriever(vector_store)
kb_retriever = KnowledgeBaseRetriever(base_retriever)


level_2_chain = (
    {
        "kb_context": RunnableLambda(kb_retriever.retrieve_kb),
        "farm_context": RunnableLambda(build_farm_context),
        "rule_context": RunnableLambda(build_rule_context),
        "question": RunnablePassthrough(),
    }
    | level_2_prompt
    | llm
)

level_1_chain = (
    {
        "kb_context": RunnableLambda(kb_retriever.retrieve_kb),
        "question": RunnablePassthrough(),
    }
    | level_1_prompt
    | llm
)


class Orchesterator:
    @staticmethod
    def answer_level_1(question: str) -> str:
        response = level_1_chain.invoke(
            {
                "question": question,
            }
        )

        return str(response.content)

    @staticmethod
    def answer_level_2(question: str, farm_id: str) -> str:

        response = level_2_chain.invoke(
            {
                "question": question,
                "farm_id": farm_id,
            }
        )

        return str(response.content)
