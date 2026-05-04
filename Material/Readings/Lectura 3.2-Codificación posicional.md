# Positional Encoding in Transformers for NLP

In any language, the order and position of words inside a sentence carry meaning. Reordering the words can change the meaning entirely. Recurrent neural networks have a built-in mechanism for handling sequence order, but Transformers use neither recurrence nor convolution and treat each token independently. Therefore, positional information must be injected explicitly so the model knows the order of the input tokens. **Positional encoding** is the method used to preserve information about the position of each element in a sequence.

This reading explains what positional encoding is, why it matters, and how it works inside the Transformer.

## What is positional encoding?

Positional encoding assigns a unique location representation to every entity in a sequence. A single scalar (such as the index value) is not used, for two reasons:

- For long sequences, indices grow large.
- Normalising indices to the range [0, 1] is unstable when sequence lengths vary, since the same position would receive a different normalised value depending on the sequence length.

Instead, Transformers assign each position its own vector. The output of the positional encoding layer is therefore a matrix in which each row represents an encoded element of the sequence combined with its positional information.

## The positional encoding layer in Transformers

In the original Transformer paper, positional encoding is the last preprocessing step applied to the input before it enters the encoder block. By the time the data reaches the encoder, it already carries semantic information from the input embedding and positional information from the positional embedding.

Suppose our input sequence consists of seven vectors $e_0, e_1, e_2, e_3, e_4, e_5, e_6$. Each vector has dimension $d$ because they have already passed through the input embedding into a high-dimensional space. To each vector $e_{pos}$ we add another vector $P_{pos}$ of the same dimension $d$. This vector $P_{pos}$ encodes the fact that $e_{pos}$ is located at position $pos$ in the sequence. The vectors are computed as:

$$P_{(pos,\,2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right)$$

$$P_{(pos,\,2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)$$

The first equation produces the entries at even indices ($2i$) and the second produces those at odd indices ($2i+1$).

### Why these functions?

If we fix $i$ to a constant (say $i=2$) and treat $pos$ as a continuous variable, the first equation traces a sinusoidal curve over $pos$. Evaluating it at $pos = 0, 1, 2, \dots, 6$ gives the corresponding entry of the position vector for each element of the sequence. The height of the sine curve encodes the position.

There is a problem, though: a single sine wave repeats periodically, so two different positions can collide on the same value. For instance, $P_{1,4}$ and $P_{4,4}$ may share the same encoding even though they correspond to positions 1 and 4. This is where the index $i$ in the equation comes in.

Varying $i$ produces sinusoidal curves of different frequencies. The intuition: when two elements lie close together in the sequence, only high-frequency sines distinguish them clearly. At low frequencies, nearby positions are assigned almost identical values; at high frequencies, those same positions land on clearly distinct values. Each frequency contributes information at a different scale, so combining them resolves collisions and lets the model tell positions apart.

In this way, every input vector $e_{pos}$ receives a positional vector $P_{pos}$ that uniquely encodes its position in the sequence.

## Positional encoding in practice

In practice, the input embedding dimension is large — hundreds or thousands of sinusoidal components are needed to build the positional vector for a single element. The result is commonly visualised as a **positional encoding matrix**:

- The x-axis represents the position of the element in the sequence (e.g., 100 tokens).
- The y-axis represents the entry of the position vector (e.g., embedding dimension 300).
- The colour at $(x, y)$ shows the value of the corresponding sinusoidal function, which lies between $-1$ and $1$.

## Bibliography

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., … & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30.
- Saeed, M. (2023). *A gentle introduction to positional encoding in transformer models, part 1*. https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1/

---
