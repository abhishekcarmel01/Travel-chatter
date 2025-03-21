import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from opentrip import get_place_info


model = SentenceTransformer("all-MiniLM-L6-v2")
def travel_embeddings(city):
    travel_data = []
    features=[]
    kinds=["accomodations", "architecture", "cultural", "natural", "religion", "banks", "foods", "shops", "transport"]
    for kind in kinds:
        response = get_place_info(city, kind)
        features.extend(response.get("features", []))
    for feature in features:
        properties=feature.get("properties")
        name=properties.get("name")
        kind=properties.get("kinds")
        description= f"{name}, Category: {kind}."
        travel_data.append(
            {
                "city": city,
                "description": description
            }
        )

    descriptions = [data["description"] for data in travel_data]
    embeddings = model.encode(descriptions)
    id=[str(i) for i in range(len(descriptions))]
    # dimension = embeddings.shape[1] # 1 dimensional array
    # index = faiss.IndexFlatL2(dimension) # L2 is Euclidean distance is used
    # index.add(np.array(embeddings))
    # faiss.write_index(index, "test_travel_index.faiss")
    # return index, travel_data
    client = chromadb.Client(settings=Settings(persist_directory="./chroma_db"))
    try:
        collection = client.get_collection(name="travel_data")
    except Exception as e:
        collection = client.create_collection(name="travel_data")
    collection.add(ids=id, documents=descriptions, embeddings=embeddings)
    return collection

def query_input(collection, query_text):
    query_embedding = model.encode([query_text])
    # k = 5  
    # distances, indices = index.search(np.array(query_embedding), k)
    # return [travel_data[i]["description"] for i in indices[0]]
    results = collection.query(query_embeddings=query_embedding, n_results=5)
    return results['documents'][0]

# if __name__ == "__main__":

#  query_text = "A famous tower in France"
#  query_embedding = model.encode([query_text])

#  k = 1  #returns a single result whjich is the most similar to the query
#  distances, indices = index.search(np.array(query_embedding), k)

#  print("Query:", query_text)
#  print("Most relevant result:", travel_data[indices[0][0]]["description"])

