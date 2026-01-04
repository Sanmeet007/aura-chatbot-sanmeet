from .prompts import symptom_prompt
from langchain_core.runnables import RunnablePassthrough


class SymptomDetector:
    BASE_SYMPTOMS = [
        "yellowing",
        "slow_growth",
        "tipburn",
        "elongation",
    ]

    def __init__(self, llm) -> None:

        self.symptom_chain = {"question": RunnablePassthrough()} | symptom_prompt | llm

    def detect_symptom_llm(self, question: str) -> str:
        response = self.symptom_chain.invoke({"question": question})
        symptom = response.content.strip().lower()  # type: ignore

        if symptom not in SymptomDetector.BASE_SYMPTOMS:
            return "slow_growth"  # safe fallback

        return symptom
