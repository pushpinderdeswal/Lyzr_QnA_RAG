from functools import lru_cache
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


@lru_cache()
def get_llm():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a friendly clinic assistant.

Use the provided context and conversation history to answer.

Context:
{context}

Conversation history:
{history}
""",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)


def get_rag_chain():
    return prompt | get_llm() | StrOutputParser()
