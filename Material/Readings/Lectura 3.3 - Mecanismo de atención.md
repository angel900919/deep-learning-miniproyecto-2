# Self-attention in Transformers for NLP

Transformers rely on a core mechanism known as **self-attention** (also called multi-head attention). It enables the model to capture dependency relationships between words in a sentence and is largely responsible for the quality and coherence of Transformer outputs. This reading explores self-attention in Transformers and its central role in natural language processing.

## How do we understand attention?

Attention is the human capability to focus on certain elements while filtering out the rest. In NLP, attention refers to the model's ability to assign different importance to different parts of a sentence in order to understand and generate text.

## The self-attention mechanism

Self-attention is built on the idea that every word in a sentence can "attend" to every other word to gather relevant information. Instead of relying on local context (e.g., a fixed context window), Transformers let each word attend to all the others in the same sentence, producing richer contextual representations.

### Queries, keys and values

Self-attention is defined by three elements:

- **Query (Q)** — the question each word asks of the rest of the sentence.
- **Key (K)** — the list of items each word can be compared against.
- **Value (V)** — the actual information each word carries.

For every word, the model computes its $Q$, $K$ and $V$ vectors via independent linear projections of the original token representation (which already includes both numerical and positional information).

For example, given the sentence "When you play many videogames", whose tokens form a 4×4 matrix, multiplying it by three separate 4×3 weight matrices yields the 4×3 matrices $Q$, $K$ and $V$ — one row per word.

### Computing the attention weights

Once $Q$, $K$ and $V$ are known for the whole sentence, we determine how the words relate to each other:

1. Compute the dot product $QK^{T}$ between the query matrix and the transpose of the keys matrix.
2. Apply a softmax to normalise the result.

The resulting matrix contains the **attention weights** — values that indicate how relevant each word is to every other word. Higher weights correspond to stronger relationships.

### Combining the values

In the third step, the attention weights are used to take a weighted sum of the value vectors:

$$\text{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{Q K^{T}}{\sqrt{d_k}}\right) V$$

where $d_k$ is the dimensionality of the keys and $\sqrt{d_k}$ is a scaling factor that keeps the dot products in a numerically stable range. The result is a contextualised representation of every word that captures the relevant information from its neighbours, weighted by importance.

## Multi-head attention

The self-attention mechanism is applied multiple times within a Transformer. Each pass is called an **attention head**. Transformers run several heads in parallel, allowing the model to learn different views of the relationships between words simultaneously. This enriches the model's ability to capture complex semantic and syntactic structure from multiple perspectives.

## Windowed attention

To address long-range dependencies more efficiently, **windowed attention** restricts the attention scope to a predefined neighbourhood of nearby words. Masks specify which words are allowed to influence which positions. This trades off computational cost against the ability to model very distant dependencies, while preserving local context.

## Conclusion

Self-attention allows every word in a sentence to interact with every other word, producing contextual representations that capture both syntactic and semantic relationships. It is the mechanism behind the success of Transformers across NLP tasks such as machine translation, text generation, and sentiment analysis. Understanding how self-attention operates is essential for anyone working on modern language models.

## Bibliography

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., … & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30.

---
