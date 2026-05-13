import chromadb


client = chromadb.PersistentClient(
    path="data/vector_db"
)

collection = client.get_or_create_collection(
    name="rag_collection"
)


def store_chunks(
    chunks,
    embeddings,
    session_id
):

    ids = []
    metadatas = []

    for i in range(len(chunks)):

        ids.append(
            f"{session_id}_chunk_{i}"
        )

        metadatas.append(
            {
                "session_id": session_id,
                "chunk_index": i
            }
        )

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids,
        metadatas=metadatas
    )


def search_chunks(
    query_embedding,
    session_id,
    top_k=3
):

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=top_k,

        where={
            "session_id": session_id
        }
    )

    return results["documents"][0]