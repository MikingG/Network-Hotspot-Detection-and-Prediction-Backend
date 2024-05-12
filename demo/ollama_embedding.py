import ollama


# res = ollama.embeddings(
#     model="qwen:4b",
#     prompt="Represent this sentence for searching relevant passages: The sky is blue because of Rayleigh scattering",
# )
def getEmbedding(text):
    res = ollama.embeddings(
        model="mxbai-embed-large",
        prompt=text,
    )
    return res["embedding"]


print(getEmbedding("The sky is blue because of Rayleigh scattering"))
