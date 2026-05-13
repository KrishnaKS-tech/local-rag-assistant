from services.embeddings import model
from services.vector_store import search_chunks

query = input("Enter query: ")

query_embedding = model.encode(query)

results = search_chunks(query_embedding)

print("\nResults:\n")

for r in results:
    print(r)