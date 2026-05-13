from llama_cpp import Llama


# Path to your local GGUF model
MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"


# Load model once (IMPORTANT: slow operation)
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,        # context window
    n_threads=8,       # adjust based on CPU
    n_gpu_layers=0     # keep 0 for CPU (change if GPU later)
)


def build_prompt(context, question):

    return f"""
<s>[INST]
You are a helpful AI assistant.

Answer ONLY from the provided context.

If the answer is not in the context, say:
"I could not find that in the provided context."

Context:
{context}

Question:
{question}
[/INST]
"""


def stream_response(prompt):

    output = llm(
        prompt,
        max_tokens=512,
        temperature=0.2,
        stop=["</s>"],
        stream=True
    )

    for token in output:

        text = token["choices"][0]["text"]

        if text:
            yield text

from services.vector_store import search_chunks
from services.embeddings import model


def ask_rag(question, session_id):

    # 1. Convert question → embedding
    query_embedding = model.encode(question)

    # 2. Retrieve relevant chunks
    relevant_chunks = search_chunks(
        query_embedding,
        session_id
    )

    # 3. Build context
    context = "\n\n".join(relevant_chunks)

    # 4. Build prompt
    prompt = build_prompt(context, question)

    # 5. Generate answer locally
    return stream_response(prompt)