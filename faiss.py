import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
travel_data = [
    {"city": "Paris", "description": "Eiffel Tower, an iconic landmark in France."},
    {"city": "Tokyo", "description": "Shibuya Crossing, the busiest pedestrian crossing in the world."},
    {"city": "New York", "description": "Statue of Liberty, a symbol of freedom in America."},
]

descriptions = [f"{item['city']}: {item['description']}" for item in travel_data]
embeddings = model.encode(descriptions)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))
faiss.write_index(index, "test_travel_index.faiss")

query_text = "A famous tower in France"
query_embedding = model.encode([query_text])

k = 1  
distances, indices = index.search(np.array(query_embedding), k)

print("Query:", query_text)
print("Most relevant result:", travel_data[indices[0][0]]["description"])

#this needs to be tested