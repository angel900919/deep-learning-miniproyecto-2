# Transformers: Text Encoding

When feeding a fragment of text into a Transformer or any neural network, it must first be converted into a format the machine can process. Different methods have emerged so that this representation is not only machine-readable but also preserves the semantic meaning of the original text.

## One-hot encoding

One of the simplest ways to convert categorical information into numbers is one-hot encoding. Each categorical value (for example, each word) is mapped to a binary vector in which a single position is active.

While one-hot encoding is straightforward, it preserves no semantic meaning. From the encoded vector you cannot tell whether a word is a noun, an adjective, a verb, an article, or whether it refers to an animal. This limitation motivates **embedding models**, also called encoding models.

## Embedding

Embedding is a numerical representation of information that can be applied to images, audio, documents, text, code, and more. The technique converts data into a format that lets the model understand the relationships between items. For text, embeddings capture the semantic meaning of what is being encoded.

For example, an embedding model produces a vector representation for the word "dog". If we apply this process to many words and measure the distances between vectors in an arbitrary space, words with similar semantic meaning end up closer together. A classic example is **Word2vec**: words encoded in a 300-dimensional space can be projected to two dimensions, and semantically related words cluster nearby.

## Embedding models

Unlike one-hot encoding, embeddings are usually produced by a pre-trained model. Examples include Instructor, Sentence Transformers, and OpenAI's models such as Ada, Davinci, Curie, and Babbage.

Once an embedding vector is obtained, it can be used for many tasks:

- Measure the distance between two sentence embeddings to assess semantic similarity.
- Compare an image embedding against a text embedding to determine whether they are related — commonly used by search engines that retrieve images matching a text query.
- Drive recommendation and ad-targeting systems on social networks.

## Conclusions

Embeddings convert data into a numerical representation that preserves semantic meaning and the relationships between items. They apply to multiple data types and are widely used in natural language processing. Related vectors lie closer together in the representation space — a property exploited by search engines and automated advertising systems.

## Bibliography

- Muennighoff, N., Tazi, N., Magne, L., & Reimers, N. (2022). *MTEB: Massive Text Embedding Benchmark*. arXiv preprint arXiv:2210.07316. doi:10.48550/ARXIV.2210.07316
- OpenAI. (2022). *New and Improved Embedding Model*. https://openai.com/blog/new-and-improved-embedding-model
- Espejel, O. (2022). *Getting Started With Embeddings*. https://huggingface.co/blog/getting-started-with-embeddings

---
