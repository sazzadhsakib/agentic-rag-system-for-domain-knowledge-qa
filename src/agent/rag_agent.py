# src/agent/rag_agent.py
from agent.prompts import SYSTEM_PROMPT, REFLECTION_PROMPT, QUERY_REWRITE_PROMPT


class RAGAgent:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    def answer(self, question: str, top_k: int = 5, max_retries: int = 2):
        current_query = question
        last_docs = []

        for attempt in range(max_retries + 1):
            print(f"--- Attempt {attempt + 1}: Searching for '{current_query}' ---")

            docs = self.retriever.retrieve(current_query, top_k)
            last_docs = docs

            context_str = "\n\n".join(
                f"[Source: {d['source']}]\n{d['text']}" for d in docs
            )
            reflection_msg = [
                {"role": "system", "content": "You are a strict evaluator."},
                {
                    "role": "user",
                    "content": REFLECTION_PROMPT.format(
                        question=question,
                        context=context_str if context_str else "No documents found.",
                    ),
                },
            ]
            reflection = self.llm.chat(reflection_msg)
            print(f"--- Reflection: {reflection} ---")

            if "YES" in reflection.upper():
                answer_msg = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Question: {question}\nContext: {context_str}\nAnswer:",
                    },
                ]
                return self.llm.chat(answer_msg), docs

            if attempt < max_retries:
                print("--- Context insufficient. Rewriting query... ---")
                rewrite_msg = [
                    {
                        "role": "user",
                        "content": QUERY_REWRITE_PROMPT.format(
                            question=question,
                            current_query=current_query,
                        ),
                    }
                ]
                current_query = self.llm.chat(rewrite_msg).strip()

        fallback_msg = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Question: {question}\nContext: {context_str}\nAnswer (state what is missing):",
            },
        ]
        return self.llm.chat(fallback_msg), last_docs
