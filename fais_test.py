import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from opentrip import get_place_info

def travel_embeddings(city):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    travel_data = []
    places = get_place_info(city)
    for place in places:
        name=place.get("name", "unknown")
        kind=place.get("kinds","unknown")
        description= f"{city}: {name}, Category: {kind}."
        travel_data.append(
            {
                "city": city,
                "description": description
            }
        )

    descriptions = [data["description"] for data in travel_data]
    embeddings = model.encode(descriptions)
    dimension = embeddings.shape[1] # 1 dimensional array
    index = faiss.IndexFlatL2(dimension) # L2 is Euclidean distance is used
    index.add(np.array(embeddings))
    faiss.write_index(index, "test_travel_index.faiss")
    return index, travel_data

def query_input(index, travel_data, query_text):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query_text])
    k = 1  
    distances, indices = index.search(np.array(query_embedding), k)
    return travel_data[indices[0][0]]["description"]   

# if __name__ == "__main__":

#  query_text = "A famous tower in France"
#  query_embedding = model.encode([query_text])

#  k = 1  #returns a single result whjich is the most similar to the query
#  distances, indices = index.search(np.array(query_embedding), k)

#  print("Query:", query_text)
#  print("Most relevant result:", travel_data[indices[0][0]]["description"])

