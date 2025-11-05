from fastapi import APIRouter, Form, Request, Response
from schemas.request import QnaResponse
from models.rag import get_rag_chain
from services.vector_store import get_retriever
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict
import uuid

router = APIRouter()

chat_history: Dict[str, List] = {}


def get_session_id(request: Request, response: Response) -> str:
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=3600 * 24 * 7,
            samesite="lax",
            secure=False,
        )
    return session_id


def dict_to_message(d: Dict):
    if d["role"] == "human":
        return HumanMessage(content=d["content"])
    elif d["role"] == "assistant":
        return AIMessage(content=d["content"])
    return None


@router.post("/ask", response_model=QnaResponse)
async def ask_qna(request: Request, response: Response, question: str = Form(...)):
    session_id = get_session_id(request, response)
    history = chat_history.get(session_id, [])

    lc_history = [dict_to_message(h) for h in history[-6:] if dict_to_message(h)]

    docs = get_retriever(k=1).invoke(question)
    source = docs[0].metadata.get("source") if docs else None

    chain = get_rag_chain()
    answer = chain.invoke(
        {
            "question": question,
            "history": lc_history,
            "context": "\n\n".join(
                [
                    f"Q: {d.page_content.split('Question: ')[1].split('Answer:')[0].strip()}\n"
                    f"A: {d.page_content.split('Answer: ')[-1].strip()}"
                    for d in docs
                ]
            ),
        }
    )

    history.append({"role": "human", "content": question})
    history.append({"role": "assistant", "content": answer})
    chat_history[session_id] = history[-10:]

    return QnaResponse(question=question, answer=answer, source=source)


@router.post("/clear")
async def clear_chat(request: Request, response: Response):
    session_id = get_session_id(request, response)
    chat_history.pop(session_id, None)
    return {"status": "cleared"}
