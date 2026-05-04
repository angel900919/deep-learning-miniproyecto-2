# BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

## Abstract

We introduce a new language representation model called **BERT** — Bidirectional Encoder Representations from Transformers. Unlike recent language representation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks — such as question answering and language inference — without substantial task-specific architecture modifications.

BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to **80.5%** (7.7% absolute improvement), MultiNLI accuracy to **86.7%** (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to **93.2** (1.5 point absolute improvement), and SQuAD v2.0 Test F1 to **83.1** (5.1 point absolute improvement).

## 1. Introduction

Language model pre-training has been shown to be effective for improving many natural language processing tasks (Dai and Le, 2015; Peters et al., 2018a; Radford et al., 2018; Howard and Ruder, 2018). These include sentence-level tasks such as natural language inference (Bowman et al., 2015; Williams et al., 2018) and paraphrasing (Dolan and Brockett, 2005), which aim to predict the relationships between sentences by analysing them holistically, as well as token-level tasks such as named entity recognition and question answering, where models are required to produce fine-grained output at the token level (Tjong Kim Sang and De Meulder, 2003; Rajpurkar et al., 2016).

There are two existing strategies for applying pre-trained language representations to downstream tasks: **feature-based** and **fine-tuning**. The feature-based approach, such as ELMo (Peters et al., 2018a), uses task-specific architectures that include the pre-trained representations as additional features. The fine-tuning approach, such as the Generative Pre-trained Transformer (OpenAI GPT) (Radford et al., 2018), introduces minimal task-specific parameters and is trained on the downstream tasks by simply fine-tuning all pre-trained parameters. The two approaches share the same objective function during pre-training, where they use unidirectional language models to learn general language representations.

We argue that current techniques restrict the power of the pre-trained representations, especially for the fine-tuning approaches. The major limitation is that standard language models are unidirectional, which limits the choice of architectures that can be used during pre-training. For example, in OpenAI GPT the authors use a left-to-right architecture where every token can only attend to previous tokens in the self-attention layers of the Transformer (Vaswani et al., 2017). Such restrictions are sub-optimal for sentence-level tasks and can be very harmful when applying fine-tuning-based approaches to token-level tasks such as question answering, where it is crucial to incorporate context from both directions.

In this paper, we improve the fine-tuning-based approaches by proposing **BERT**: Bidirectional Encoder Representations from Transformers. BERT alleviates the previously mentioned unidirectionality constraint by using a **"masked language model" (MLM)** pre-training objective, inspired by the Cloze task (Taylor, 1953). The masked language model randomly masks some of the tokens from the input, and the objective is to predict the original vocabulary id of the masked word based only on its context. Unlike left-to-right language model pre-training, the MLM objective enables the representation to fuse the left and right context, which allows us to pre-train a deep bidirectional Transformer. In addition to the masked language model, we also use a **"next sentence prediction"** task that jointly pre-trains text-pair representations.

The contributions of our paper are as follows:

- We demonstrate the importance of bidirectional pre-training for language representations. Unlike Radford et al. (2018), which uses unidirectional language models for pre-training, BERT uses masked language models to enable pre-trained deep bidirectional representations. This is also in contrast to Peters et al. (2018a), which uses a shallow concatenation of independently trained left-to-right and right-to-left LMs.
- We show that pre-trained representations reduce the need for many heavily-engineered task-specific architectures. BERT is the first fine-tuning-based representation model that achieves state-of-the-art performance on a large suite of sentence-level and token-level tasks, outperforming many task-specific architectures.
- BERT advances the state of the art for eleven NLP tasks. The code and pre-trained models are available at <https://github.com/google-research/bert>.

## 2. Related Work

There is a long history of pre-training general language representations; we briefly review the most widely used approaches.

### 2.1 Unsupervised Feature-based Approaches

Learning widely applicable representations of words has been an active area of research for decades, including non-neural (Brown et al., 1992; Ando and Zhang, 2005; Blitzer et al., 2006) and neural (Mikolov et al., 2013; Pennington et al., 2014) methods. Pre-trained word embeddings are an integral part of modern NLP systems, offering significant improvements over embeddings learned from scratch (Turian et al., 2010). To pre-train word-embedding vectors, left-to-right language modelling objectives have been used (Mnih and Hinton, 2009), as well as objectives that discriminate correct from incorrect words in left and right context (Mikolov et al., 2013).

These approaches have been generalised to coarser granularities, such as sentence embeddings (Kiros et al., 2015; Logeswaran and Lee, 2018) or paragraph embeddings (Le and Mikolov, 2014). To train sentence representations, prior work has used objectives to rank candidate next sentences (Jernite et al., 2017; Logeswaran and Lee, 2018), left-to-right generation of next-sentence words given a representation of the previous sentence (Kiros et al., 2015), or denoising auto-encoder-derived objectives (Hill et al., 2016).

ELMo and its predecessor (Peters et al., 2017, 2018a) generalise traditional word-embedding research along a different dimension. They extract context-sensitive features from a left-to-right and a right-to-left language model. The contextual representation of each token is the concatenation of the two. When integrating contextual word embeddings with existing task-specific architectures, ELMo advances the state of the art for several major NLP benchmarks (Peters et al., 2018a) including question answering (Rajpurkar et al., 2016), sentiment analysis (Socher et al., 2013), and named entity recognition (Tjong Kim Sang and De Meulder, 2003). Melamud et al. (2016) proposed learning contextual representations through a task to predict a single word from both left and right context using LSTMs. Similar to ELMo, their model is feature-based and not deeply bidirectional. Fedus et al. (2018) shows that the cloze task can be used to improve the robustness of text generation models.

### 2.2 Unsupervised Fine-tuning Approaches

As with the feature-based approaches, the first works in this direction only pre-trained word-embedding parameters from unlabeled text (Collobert and Weston, 2008).

More recently, sentence or document encoders that produce contextual token representations have been pre-trained from unlabeled text and fine-tuned for a supervised downstream task (Dai and Le, 2015; Howard and Ruder, 2018; Radford et al., 2018). The advantage of these approaches is that few parameters need to be learned from scratch. Partly because of this, OpenAI GPT (Radford et al., 2018) achieved previously state-of-the-art results on many sentence-level tasks from the GLUE benchmark (Wang et al., 2018a). Left-to-right language modelling and auto-encoder objectives have been used for pre-training such models (Howard and Ruder, 2018; Radford et al., 2018; Dai and Le, 2015).

### 2.3 Transfer Learning from Supervised Data

There has also been work showing effective transfer from supervised tasks with large datasets, such as natural language inference (Conneau et al., 2017) and machine translation (McCann et al., 2017). Computer-vision research has also demonstrated the importance of transfer learning from large pre-trained models, where an effective recipe is to fine-tune models pre-trained with ImageNet (Deng et al., 2009; Yosinski et al., 2014).

## 3. BERT

We introduce BERT and its detailed implementation in this section. There are two steps in our framework: **pre-training** and **fine-tuning**. During pre-training, the model is trained on unlabeled data over different pre-training tasks. For fine-tuning, the BERT model is first initialised with the pre-trained parameters, and all of the parameters are fine-tuned using labeled data from the downstream tasks. Each downstream task has separate fine-tuned models, even though they are initialised with the same pre-trained parameters. The question-answering example in Figure 1 will serve as a running example for this section.

![Figure 1: Pre-training and fine-tuning of BERT](BERT-%20Pre-training%20of%20Deep%20Bidirectional%20Transformers%20for%20Language%20Understanding_images/Screenshot%202026-05-04%20at%206.20.48%E2%80%AFpm.png)

*Figure 1: Overall pre-training and fine-tuning procedures for BERT. Apart from output layers, the same architectures are used in both pre-training and fine-tuning. The same pre-trained model parameters are used to initialise models for different downstream tasks. During fine-tuning, all parameters are fine-tuned. `[CLS]` is a special symbol added in front of every input example, and `[SEP]` is a special separator token (e.g. separating questions/answers).*

A distinctive feature of BERT is its unified architecture across different tasks. There is minimal difference between the pre-trained architecture and the final downstream architecture.

### Model Architecture

BERT's model architecture is a multi-layer bidirectional Transformer encoder based on the original implementation described in Vaswani et al. (2017) and released in the tensor2tensor library. Because the use of Transformers has become common and our implementation is almost identical to the original, we refer readers to Vaswani et al. (2017) and to excellent guides such as "The Annotated Transformer".

We denote:
- $L$ — number of layers (Transformer blocks)
- $H$ — hidden size
- $A$ — number of self-attention heads

We primarily report results on two model sizes:
- **BERT_BASE**: $L = 12$, $H = 768$, $A = 12$, total parameters = 110M.
- **BERT_LARGE**: $L = 24$, $H = 1024$, $A = 16$, total parameters = 340M.

BERT_BASE was chosen to have the same model size as OpenAI GPT for comparison purposes. Critically, however, the BERT Transformer uses bidirectional self-attention, while the GPT Transformer uses constrained self-attention where every token can only attend to context to its left. *Note: in the literature the bidirectional Transformer is often referred to as a "Transformer encoder", while the left-context-only version is referred to as a "Transformer decoder" since it can be used for text generation.*

### Input/Output Representations

To make BERT handle a variety of downstream tasks, our input representation is able to unambiguously represent both a single sentence and a pair of sentences (e.g., $\langle$Question, Answer$\rangle$) in one token sequence. Throughout this work, a "sentence" can be an arbitrary span of contiguous text, rather than an actual linguistic sentence. A "sequence" refers to the input token sequence to BERT, which may be a single sentence or two sentences packed together.

We use **WordPiece** embeddings (Wu et al., 2016) with a 30 000 token vocabulary. The first token of every sequence is always a special classification token (`[CLS]`). The final hidden state corresponding to this token is used as the aggregate sequence representation for classification tasks. Sentence pairs are packed together into a single sequence, and we differentiate the sentences in two ways: first, we separate them with a special token (`[SEP]`); second, we add a learned embedding to every token indicating whether it belongs to sentence A or sentence B. As shown in Figure 1, we denote input embedding as $E$, the final hidden vector of the `[CLS]` token as $C \in \mathbb{R}^{H}$, and the final hidden vector for the $i$-th input token as $T_i \in \mathbb{R}^{H}$.

For a given token, its input representation is constructed by summing the corresponding token, segment, and position embeddings.

![Figure 2: BERT input representation](BERT-%20Pre-training%20of%20Deep%20Bidirectional%20Transformers%20for%20Language%20Understanding_images/Screenshot%202026-05-04%20at%206.21.55%E2%80%AFpm.png)

*Figure 2: BERT input representation. The input embeddings are the sum of the token embeddings, the segmentation embeddings, and the position embeddings.*

### 3.1 Pre-training BERT

Unlike Peters et al. (2018a) and Radford et al. (2018), we do not use traditional left-to-right or right-to-left language models to pre-train BERT. Instead, we pre-train BERT using two unsupervised tasks.

#### Task #1: Masked LM

A deep bidirectional model is intuitively more powerful than either a left-to-right model or the shallow concatenation of left-to-right and right-to-left models. Unfortunately, standard conditional language models can only be trained left-to-right or right-to-left, since bidirectional conditioning would let each word indirectly "see itself", and the model could trivially predict the target word in a multi-layered context.

To train a deep bidirectional representation, we simply mask some percentage of the input tokens at random and then predict those masked tokens. We refer to this procedure as a **masked LM (MLM)**, although it is often called a Cloze task in the literature (Taylor, 1953). The final hidden vectors corresponding to the mask tokens are fed into an output softmax over the vocabulary, as in a standard LM. In all our experiments, we mask **15%** of all WordPiece tokens in each sequence at random. Unlike denoising auto-encoders (Vincent et al., 2008), we only predict the masked words rather than reconstructing the entire input.

Although this allows us to obtain a bidirectional pre-trained model, a downside is that we are creating a mismatch between pre-training and fine-tuning, since the `[MASK]` token does not appear during fine-tuning. To mitigate this, we do not always replace "masked" words with the actual `[MASK]` token. The training-data generator chooses 15% of the token positions at random for prediction. If the $i$-th token is chosen, we replace it with:

1. the `[MASK]` token 80% of the time,
2. a random token 10% of the time, or
3. the unchanged $i$-th token 10% of the time.

Then $T_i$ is used to predict the original token with cross-entropy loss.

#### Task #2: Next Sentence Prediction (NSP)

Many important downstream tasks such as Question Answering (QA) and Natural Language Inference (NLI) are based on understanding the relationship between two sentences, which is not directly captured by language modelling. To train a model that understands sentence relationships, we pre-train for a binarised next-sentence-prediction task that can be trivially generated from any monolingual corpus. Specifically, when choosing the sentences A and B for each pre-training example, 50% of the time B is the actual next sentence that follows A (labeled `IsNext`), and 50% of the time it is a random sentence from the corpus (labeled `NotNext`). As shown in Figure 1, $C$ is used for next-sentence prediction (NSP). Despite its simplicity, we demonstrate in Section 5.1 that pre-training towards this task is very beneficial to both QA and NLI.

#### Pre-training data

The pre-training procedure largely follows the existing literature on language model pre-training. For the pre-training corpus we use the **BooksCorpus** (800M words; Zhu et al., 2015) and **English Wikipedia** (2 500M words). For Wikipedia we extract only the text passages and ignore lists, tables, and headers. It is critical to use a document-level corpus rather than a shuffled sentence-level corpus such as the Billion Word Benchmark (Chelba et al., 2013) in order to extract long contiguous sequences.

### 3.2 Fine-tuning BERT

Fine-tuning is straightforward since the self-attention mechanism in the Transformer allows BERT to model many downstream tasks — whether they involve single text or text pairs — by swapping out the appropriate inputs and outputs. For applications involving text pairs, a common pattern is to independently encode text pairs before applying bidirectional cross attention, such as in Parikh et al. (2016) and Seo et al. (2017). BERT instead uses the self-attention mechanism to unify these two stages, as encoding a concatenated text pair with self-attention effectively includes bidirectional cross-attention between two sentences.

For each task, we simply plug in the task-specific inputs and outputs into BERT and fine-tune all the parameters end-to-end. At the input, sentence A and sentence B from pre-training are analogous to:

1. sentence pairs in paraphrasing,
2. hypothesis–premise pairs in entailment,
3. question–passage pairs in question answering, and
4. a degenerate text–$\emptyset$ pair in text classification or sequence tagging.

At the output, the token representations are fed into an output layer for token-level tasks (such as sequence tagging or question answering), and the `[CLS]` representation is fed into an output layer for classification tasks (such as entailment or sentiment analysis).

Compared with pre-training, fine-tuning is relatively inexpensive. All the results in the paper can be replicated in at most 1 hour on a single Cloud TPU, or a few hours on a GPU, starting from the same pre-trained model.

## 4. Experiments

In this section we present BERT fine-tuning results on 11 NLP tasks.

### 4.1 GLUE

The General Language Understanding Evaluation (GLUE) benchmark (Wang et al., 2018a) is a collection of diverse natural language understanding tasks. To fine-tune on GLUE, we represent the input sequence (for single sentence or sentence pairs) as described in Section 3 and use the final hidden vector $C \in \mathbb{R}^{H}$ corresponding to the first input token (`[CLS]`) as the aggregate representation. The only new parameters introduced during fine-tuning are classification-layer weights $W \in \mathbb{R}^{K \times H}$, where $K$ is the number of labels. We compute a standard classification loss with $C$ and $W$, i.e. $\log(\text{softmax}(CW^{T}))$.

We use a batch size of 32 and fine-tune for 3 epochs over the data for all GLUE tasks. For each task, we selected the best fine-tuning learning rate (among 5e-5, 4e-5, 3e-5, and 2e-5) on the Dev set. For BERT_LARGE we found that fine-tuning was sometimes unstable on small datasets, so we ran several random restarts and selected the best model on the Dev set.

*Table 1: GLUE Test results, scored by the evaluation server. The "Average" column is slightly different from the official GLUE score, since we exclude the problematic WNLI set. F1 scores are reported for QQP and MRPC, Spearman correlations for STS-B, and accuracy for the other tasks.*

| System | MNLI-(m/mm) | QQP | QNLI | SST-2 | CoLA | STS-B | MRPC | RTE | Average |
|---|---|---|---|---|---|---|---|---|---|
| Pre-OpenAI SOTA | 80.6 / 80.1 | 66.1 | 82.3 | 93.2 | 35.0 | 81.0 | 86.0 | 61.7 | 74.0 |
| BiLSTM+ELMo+Attn | 76.4 / 76.1 | 64.8 | 79.8 | 90.4 | 36.0 | 73.3 | 84.9 | 56.8 | 71.0 |
| OpenAI GPT | 82.1 / 81.4 | 70.3 | 87.4 | 91.3 | 45.4 | 80.0 | 82.3 | 56.0 | 75.1 |
| **BERT_BASE** | 84.6 / 83.4 | 71.2 | 90.5 | 93.5 | 52.1 | 85.8 | 88.9 | 66.4 | 79.6 |
| **BERT_LARGE** | **86.7 / 85.9** | **72.1** | **92.7** | **94.9** | **60.5** | **86.5** | **89.3** | **70.1** | **82.1** |

Both BERT_BASE and BERT_LARGE outperform all systems on all tasks by a substantial margin, obtaining 4.5% and 7.0% respective average accuracy improvement over the prior state of the art. Note that BERT_BASE and OpenAI GPT are nearly identical in terms of model architecture apart from the attention masking. For MNLI, BERT obtains a 4.6% absolute accuracy improvement. On the official GLUE leaderboard, BERT_LARGE obtains a score of **80.5**, compared to OpenAI GPT, which obtained 72.8 as of the date of writing.

We find that BERT_LARGE significantly outperforms BERT_BASE across all tasks, especially those with very little training data.

### 4.2 SQuAD v1.1

The Stanford Question Answering Dataset (SQuAD v1.1) is a collection of 100K crowd-sourced question/answer pairs (Rajpurkar et al., 2016). Given a question and a passage from Wikipedia containing the answer, the task is to predict the answer text span in the passage.

In question answering, we represent the input question and passage as a single packed sequence, with the question using the A embedding and the passage using the B embedding. We only introduce a start vector $S \in \mathbb{R}^{H}$ and an end vector $E \in \mathbb{R}^{H}$ during fine-tuning. The probability of word $i$ being the start of the answer span is computed as:

$$P_i = \frac{e^{S \cdot T_i}}{\sum_j e^{S \cdot T_j}}$$

The analogous formula is used for the end of the answer span. The score of a candidate span from position $i$ to position $j$ is defined as $S \cdot T_i + E \cdot T_j$, and the maximum scoring span where $j \geq i$ is used as a prediction. The training objective is the sum of the log-likelihoods of the correct start and end positions. We fine-tune for 3 epochs with a learning rate of 5e-5 and a batch size of 32.

We use modest data augmentation by first fine-tuning on TriviaQA (Joshi et al., 2017) before fine-tuning on SQuAD.

*Table 2: SQuAD 1.1 results. The BERT ensemble is 7× systems which use different pre-training checkpoints and fine-tuning seeds.*

| System | Dev EM | Dev F1 | Test EM | Test F1 |
|---|---|---|---|---|
| Human | – | – | 82.3 | 91.2 |
| #1 Ensemble — nlnet | – | – | 86.0 | 91.7 |
| #2 Ensemble — QANet | – | – | 84.5 | 90.5 |
| BiDAF + ELMo (Single) | – | 85.6 | – | 85.8 |
| R.M. Reader (Ensemble) | 81.2 | 87.9 | 82.3 | 88.5 |
| BERT_BASE (Single) | 80.8 | 88.5 | – | – |
| BERT_LARGE (Single) | 84.1 | 90.9 | – | – |
| BERT_LARGE (Ensemble) | 85.8 | 91.8 | – | – |
| BERT_LARGE (Single + TriviaQA) | 84.2 | 91.1 | 85.1 | 91.8 |
| **BERT_LARGE (Ensemble + TriviaQA)** | **86.2** | **92.2** | **87.4** | **93.2** |

Our best-performing system outperforms the top leaderboard system by **+1.5 F1** in ensembling and **+1.3 F1** as a single system. Without TriviaQA fine-tuning data, we only lose 0.1–0.4 F1, still outperforming all existing systems by a wide margin.

### 4.3 SQuAD v2.0

SQuAD 2.0 extends SQuAD 1.1 by allowing for the possibility that no short answer exists in the provided paragraph, making the problem more realistic.

We treat questions that do not have an answer as having an answer span with start and end at the `[CLS]` token. The probability space for the start and end answer-span positions is extended to include the position of the `[CLS]` token. For prediction, we compare the score of the no-answer span $s_{\text{null}} = S \cdot C + E \cdot C$ with the score of the best non-null span $\hat{s}_{i,j} = \max_{j \geq i} S \cdot T_i + E \cdot T_j$. We predict a non-null answer when $\hat{s}_{i,j} > s_{\text{null}} + \tau$, where the threshold $\tau$ is selected on the dev set to maximise F1. We did not use TriviaQA data for this model. We fine-tuned for 2 epochs with a learning rate of 5e-5 and a batch size of 48.

*Table 3: SQuAD 2.0 results. We exclude entries that use BERT as one of their components.*

| System | Dev EM | Dev F1 | Test EM | Test F1 |
|---|---|---|---|---|
| Human | 86.3 | 89.0 | 86.9 | 89.5 |
| #1 Single — MIR-MRC (F-Net) | – | – | 74.8 | 78.0 |
| #2 Single — nlnet | – | – | 74.2 | 77.1 |
| unet (Ensemble) | – | – | 71.4 | 74.9 |
| SLQA+ (Single) | – | 71.4 | – | 74.4 |
| **BERT_LARGE (Single)** | 78.7 | 81.9 | **80.0** | **83.1** |

We observe a **+5.1 F1** improvement over the previous best system.

### 4.4 SWAG

The Situations With Adversarial Generations (SWAG) dataset contains 113K sentence-pair completion examples that evaluate grounded commonsense inference (Zellers et al., 2018). Given a sentence, the task is to choose the most plausible continuation among four choices.

When fine-tuning on SWAG, we construct four input sequences, each containing the concatenation of the given sentence (sentence A) and a possible continuation (sentence B). The only task-specific parameter introduced is a vector whose dot product with the `[CLS]` token representation $C$ denotes a score for each choice, normalised with a softmax layer.

We fine-tune the model for 3 epochs with a learning rate of 2e-5 and a batch size of 16.

*Table 4: SWAG Dev and Test accuracies. †Human performance is measured with 100 samples, as reported in the SWAG paper.*

| System | Dev | Test |
|---|---|---|
| ESIM + GloVe | 51.9 | 52.7 |
| ESIM + ELMo | 59.1 | 59.2 |
| OpenAI GPT | – | 78.0 |
| BERT_BASE | 81.6 | – |
| **BERT_LARGE** | **86.6** | **86.3** |
| Human (expert)† | – | 85.0 |
| Human (5 annotations)† | – | 88.0 |

BERT_LARGE outperforms the authors' baseline ESIM+ELMo system by **+27.1%** and OpenAI GPT by **8.3%**.

## 5. Ablation Studies

We perform ablations over a number of facets of BERT to better understand their relative importance.

### 5.1 Effect of Pre-training Tasks

We evaluate two pre-training objectives using exactly the same pre-training data, fine-tuning scheme, and hyperparameters as BERT_BASE:

- **No NSP** — a bidirectional model trained using the masked-LM (MLM) but without the next-sentence-prediction (NSP) task.
- **LTR & No NSP** — a left-context-only model trained as a standard left-to-right (LTR) LM rather than an MLM. The left-only constraint was also applied at fine-tuning, because removing it introduced a pre-train/fine-tune mismatch that degraded downstream performance. This model was also pre-trained without the NSP task, making it directly comparable to OpenAI GPT (but using our larger training dataset, our input representation, and our fine-tuning scheme).

*Table 5: Ablation over the pre-training tasks using the BERT_BASE architecture.*

| Tasks | MNLI-m (Acc) | QNLI (Acc) | MRPC (Acc) | SST-2 (Acc) | SQuAD (F1) |
|---|---|---|---|---|---|
| BERT_BASE | 84.4 | 88.4 | 86.7 | 92.7 | 88.5 |
| No NSP | 83.9 | 84.9 | 86.5 | 92.6 | 87.9 |
| LTR & No NSP | 82.1 | 84.3 | 77.5 | 92.1 | 77.8 |
| LTR & No NSP + BiLSTM | 82.1 | 84.1 | 75.7 | 91.6 | 84.9 |

Removing NSP hurts performance significantly on QNLI, MNLI, and SQuAD 1.1. The LTR model performs worse than the MLM model on all tasks, with large drops on MRPC and SQuAD. For SQuAD it is intuitively clear that an LTR model will perform poorly at token predictions, since the token-level hidden states have no right-side context. Adding a randomly initialised BiLSTM on top significantly improves results on SQuAD, but the results are still far worse than those of the pre-trained bidirectional models, and the BiLSTM hurts performance on the GLUE tasks.

We could also train separate LTR and RTL models and represent each token as the concatenation of the two — as ELMo does — but: (a) this is twice as expensive as a single bidirectional model; (b) it is non-intuitive for tasks like QA, since the RTL model would not be able to condition the answer on the question; (c) it is strictly less powerful than a deep bidirectional model, since a bidirectional model can use both left and right context at every layer.

### 5.2 Effect of Model Size

We trained a number of BERT models with differing numbers of layers, hidden units, and attention heads, while otherwise using the same hyperparameters and training procedure as described previously.

*Table 6: Ablation over BERT model size. #L = number of layers; #H = hidden size; #A = number of attention heads. "LM (ppl)" is the masked-LM perplexity of held-out training data.*

| #L | #H | #A | LM (ppl) | MNLI-m | MRPC | SST-2 |
|---|---|---|---|---|---|---|
| 3 | 768 | 12 | 5.84 | 77.9 | 79.8 | 88.4 |
| 6 | 768 | 3 | 5.24 | 80.6 | 82.2 | 90.7 |
| 6 | 768 | 12 | 4.68 | 81.9 | 84.8 | 91.3 |
| 12 | 768 | 12 | 3.99 | 84.4 | 86.7 | 92.9 |
| 12 | 1024 | 16 | 3.54 | 85.7 | 86.9 | 93.3 |
| 24 | 1024 | 16 | **3.23** | **86.6** | **87.8** | **93.7** |

Larger models lead to a strict accuracy improvement across all four datasets, even for MRPC, which only has 3 600 labeled training examples and is substantially different from the pre-training tasks. We believe this is the first work to demonstrate convincingly that scaling to extreme model sizes also leads to large improvements on very small-scale tasks, provided that the model has been sufficiently pre-trained.

### 5.3 Feature-based Approach with BERT

All of the BERT results presented so far have used the fine-tuning approach. The feature-based approach, where fixed features are extracted from the pre-trained model, has certain advantages: not all tasks can be easily represented by a Transformer encoder architecture, and there are major computational benefits to pre-computing an expensive representation of the training data once and then running many cheaper experiments on top of it.

We compare the two approaches on the CoNLL-2003 Named Entity Recognition (NER) task (Tjong Kim Sang and De Meulder, 2003). In the input to BERT, we use a case-preserving WordPiece model and include the maximal document context provided by the data. Following standard practice, we formulate this as a tagging task but do not use a CRF layer in the output. We use the representation of the first sub-token as the input to the token-level classifier over the NER label set.

To ablate the fine-tuning approach, we apply the feature-based approach by extracting the activations from one or more layers without fine-tuning any parameters of BERT. These contextual embeddings are used as input to a randomly initialised two-layer 768-dimensional BiLSTM before the classification layer.

*Table 7: CoNLL-2003 Named Entity Recognition results.*

| System | Dev F1 | Test F1 |
|---|---|---|
| ELMo (Peters et al., 2018a) | 95.7 | 92.2 |
| CVT (Clark et al., 2018) | – | 92.6 |
| CSE (Akbik et al., 2018) | – | 93.1 |
| **Fine-tuning** | | |
| BERT_LARGE | 96.6 | 92.8 |
| BERT_BASE | 96.4 | 92.4 |
| **Feature-based (BERT_BASE)** | | |
| Embeddings | 91.0 | – |
| Second-to-Last Hidden | 95.6 | – |
| Last Hidden | 94.9 | – |
| Weighted Sum Last Four Hidden | 95.9 | – |
| Concat Last Four Hidden | 96.1 | – |
| Weighted Sum All 12 Layers | 95.5 | – |

BERT_LARGE performs competitively with state-of-the-art methods. The best-performing feature-based method concatenates the token representations from the top four hidden layers of the pre-trained Transformer, which is only 0.3 F1 behind fine-tuning the entire model. This demonstrates that BERT is effective for both fine-tuning and feature-based approaches.

## 6. Conclusion

Recent empirical improvements due to transfer learning with language models have demonstrated that rich, unsupervised pre-training is an integral part of many language-understanding systems. In particular, these results enable even low-resource tasks to benefit from deep unidirectional architectures. Our major contribution is further generalising these findings to **deep bidirectional architectures**, allowing the same pre-trained model to successfully tackle a broad set of NLP tasks.

## References

Akbik, A., Blythe, D., & Vollgraf, R. (2018). Contextual string embeddings for sequence labeling. *Proceedings of the 27th International Conference on Computational Linguistics*, 1638–1649.

Al-Rfou, R., Choe, D., Constant, N., Guo, M., & Jones, L. (2018). Character-level language modeling with deeper self-attention. arXiv:1808.04444.

Ando, R. K., & Zhang, T. (2005). A framework for learning predictive structures from multiple tasks and unlabeled data. *Journal of Machine Learning Research*, 6 (Nov), 1817–1853.

Bentivogli, L., Magnini, B., Dagan, I., Trang Dang, H., & Giampiccolo, D. (2009). The fifth PASCAL recognizing textual entailment challenge. In *TAC*.

Blitzer, J., McDonald, R., & Pereira, F. (2006). Domain adaptation with structural correspondence learning. In *EMNLP*, 120–128.

Bowman, S. R., Angeli, G., Potts, C., & Manning, C. D. (2015). A large annotated corpus for learning natural language inference. In *EMNLP*.

Brown, P. F., Desouza, P. V., Mercer, R. L., Della Pietra, V. J., & Lai, J. C. (1992). Class-based n-gram models of natural language. *Computational Linguistics*, 18(4), 467–479.

Cer, D., Diab, M., Agirre, E., Lopez-Gazpio, I., & Specia, L. (2017). SemEval-2017 task 1: Semantic textual similarity. In *SemEval-2017*, 1–14.

Chelba, C., Mikolov, T., Schuster, M., Ge, Q., Brants, T., Koehn, P., & Robinson, T. (2013). One billion word benchmark for measuring progress in statistical language modeling. arXiv:1312.3005.

Chen, Z., Zhang, H., Zhang, X., & Zhao, L. (2018). Quora question pairs.

Clark, C., & Gardner, M. (2018). Simple and effective multi-paragraph reading comprehension. In *ACL*.

Clark, K., Luong, M.-T., Manning, C. D., & Le, Q. (2018). Semi-supervised sequence modeling with cross-view training. In *EMNLP*, 1914–1925.

Collobert, R., & Weston, J. (2008). A unified architecture for natural language processing. In *ICML*, 160–167.

Conneau, A., Kiela, D., Schwenk, H., Barrault, L., & Bordes, A. (2017). Supervised learning of universal sentence representations. In *EMNLP*, 670–680.

Dai, A. M., & Le, Q. V. (2015). Semi-supervised sequence learning. In *NeurIPS*, 3079–3087.

Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., & Fei-Fei, L. (2009). ImageNet: A large-scale hierarchical image database. In *CVPR*.

Dolan, W. B., & Brockett, C. (2005). Automatically constructing a corpus of sentential paraphrases. In *IWP*.

Fedus, W., Goodfellow, I., & Dai, A. M. (2018). MaskGAN: Better text generation via filling in the _____. arXiv:1801.07736.

Hendrycks, D., & Gimpel, K. (2016). Bridging nonlinearities and stochastic regularizers with Gaussian error linear units. arXiv:1606.08415.

Hill, F., Cho, K., & Korhonen, A. (2016). Learning distributed representations of sentences from unlabelled data. In *NAACL*.

Howard, J., & Ruder, S. (2018). Universal language model fine-tuning for text classification. In *ACL*.

Hu, M., Peng, Y., Huang, Z., Qiu, X., Wei, F., & Zhou, M. (2018). Reinforced mnemonic reader for machine reading comprehension. In *IJCAI*.

Jernite, Y., Bowman, S. R., & Sontag, D. (2017). Discourse-based objectives for fast unsupervised sentence representation learning. arXiv:1705.00557.

Joshi, M., Choi, E., Weld, D. S., & Zettlemoyer, L. (2017). TriviaQA: A large scale distantly supervised challenge dataset for reading comprehension. In *ACL*.

Kiros, R., Zhu, Y., Salakhutdinov, R., Zemel, R., Urtasun, R., Torralba, A., & Fidler, S. (2015). Skip-thought vectors. In *NeurIPS*, 3294–3302.

Le, Q., & Mikolov, T. (2014). Distributed representations of sentences and documents. In *ICML*, 1188–1196.

Levesque, H. J., Davis, E., & Morgenstern, L. (2011). The Winograd schema challenge. In *AAAI Spring Symposium*.

Logeswaran, L., & Lee, H. (2018). An efficient framework for learning sentence representations. In *ICLR*.

McCann, B., Bradbury, J., Xiong, C., & Socher, R. (2017). Learned in translation: Contextualized word vectors. In *NeurIPS*.

Melamud, O., Goldberger, J., & Dagan, I. (2016). context2vec: Learning generic context embedding with bidirectional LSTM. In *CoNLL*.

Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S., & Dean, J. (2013). Distributed representations of words and phrases and their compositionality. In *NeurIPS 26*, 3111–3119.

Mnih, A., & Hinton, G. E. (2009). A scalable hierarchical distributed language model. In *NeurIPS 21*, 1081–1088.

Parikh, A. P., Täckström, O., Das, D., & Uszkoreit, J. (2016). A decomposable attention model for natural language inference. In *EMNLP*.

Pennington, J., Socher, R., & Manning, C. D. (2014). GloVe: Global vectors for word representation. In *EMNLP*, 1532–1543.

Peters, M., Ammar, W., Bhagavatula, C., & Power, R. (2017). Semi-supervised sequence tagging with bidirectional language models. In *ACL*.

Peters, M., Neumann, M., Iyyer, M., Gardner, M., Clark, C., Lee, K., & Zettlemoyer, L. (2018a). Deep contextualized word representations. In *NAACL*.

Peters, M., Neumann, M., Zettlemoyer, L., & Yih, W.-t. (2018b). Dissecting contextual word embeddings: Architecture and representation. In *EMNLP*, 1499–1509.

Radford, A., Narasimhan, K., Salimans, T., & Sutskever, I. (2018). Improving language understanding with unsupervised learning. Technical report, OpenAI.

Rajpurkar, P., Zhang, J., Lopyrev, K., & Liang, P. (2016). SQuAD: 100,000+ questions for machine comprehension of text. In *EMNLP*, 2383–2392.

Seo, M., Kembhavi, A., Farhadi, A., & Hajishirzi, H. (2017). Bidirectional attention flow for machine comprehension. In *ICLR*.

Socher, R., Perelygin, A., Wu, J., Chuang, J., Manning, C. D., Ng, A., & Potts, C. (2013). Recursive deep models for semantic compositionality over a sentiment treebank. In *EMNLP*, 1631–1642.

Sun, F., Li, L., Qiu, X., & Liu, Y. (2018). U-Net: Machine reading comprehension with unanswerable questions. arXiv:1810.06638.

Taylor, W. L. (1953). Cloze procedure: A new tool for measuring readability. *Journalism Bulletin*, 30(4), 415–433.

Tjong Kim Sang, E. F., & De Meulder, F. (2003). Introduction to the CoNLL-2003 shared task: Language-independent named entity recognition. In *CoNLL*.

Turian, J., Ratinov, L., & Bengio, Y. (2010). Word representations: A simple and general method for semi-supervised learning. In *ACL*, 384–394.

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention is all you need. In *NeurIPS*, 6000–6010.

Vincent, P., Larochelle, H., Bengio, Y., & Manzagol, P.-A. (2008). Extracting and composing robust features with denoising auto-encoders. In *ICML*, 1096–1103.

Wang, A., Singh, A., Michael, J., Hill, F., Levy, O., & Bowman, S. (2018a). GLUE: A multi-task benchmark and analysis platform for natural language understanding. In *EMNLP Workshop BlackboxNLP*, 353–355.

Wang, W., Yan, M., & Wu, C. (2018b). Multi-granularity hierarchical attention fusion networks for reading comprehension and question answering. In *ACL*.

Warstadt, A., Singh, A., & Bowman, S. R. (2018). Neural network acceptability judgments. arXiv:1805.12471.

Williams, A., Nangia, N., & Bowman, S. R. (2018). A broad-coverage challenge corpus for sentence understanding through inference. In *NAACL*.

Wu, Y., Schuster, M., Chen, Z., Le, Q. V., Norouzi, M., Macherey, W., et al. (2016). Google's neural machine translation system: Bridging the gap between human and machine translation. arXiv:1609.08144.

Yosinski, J., Clune, J., Bengio, Y., & Lipson, H. (2014). How transferable are features in deep neural networks? In *NeurIPS*, 3320–3328.

Yu, A. W., Dohan, D., Luong, M.-T., Zhao, R., Chen, K., Norouzi, M., & Le, Q. V. (2018). QANet: Combining local convolution with global self-attention for reading comprehension. In *ICLR*.

Zellers, R., Bisk, Y., Schwartz, R., & Choi, Y. (2018). SWAG: A large-scale adversarial dataset for grounded commonsense inference. In *EMNLP*.

Zhu, Y., Kiros, R., Zemel, R., Salakhutdinov, R., Urtasun, R., Torralba, A., & Fidler, S. (2015). Aligning books and movies: Towards story-like visual explanations by watching movies and reading books. In *ICCV*, 19–27.

## Appendix A: Additional Details for BERT

### A.1 Illustration of the Pre-training Tasks

#### Masked LM and the Masking Procedure

Suppose the unlabeled sentence is *"my dog is hairy"* and during the random masking procedure we choose the 4th token (corresponding to *hairy*). The masking procedure can be illustrated as follows:

- **80% of the time** — Replace the word with the `[MASK]` token, e.g. *my dog is hairy → my dog is `[MASK]`*.
- **10% of the time** — Replace the word with a random word, e.g. *my dog is hairy → my dog is apple*.
- **10% of the time** — Keep the word unchanged, e.g. *my dog is hairy → my dog is hairy*. The purpose is to bias the representation towards the actual observed word.

The advantage of this procedure is that the Transformer encoder does not know which words it will be asked to predict or which have been replaced by random words, so it is forced to keep a distributional contextual representation of every input token. Random replacement only occurs for 1.5% of all tokens (10% of 15%), which does not seem to harm the model's language-understanding capability.

Compared to standard language model training, the masked LM only makes predictions on 15% of tokens in each batch, which suggests that more pre-training steps may be required to converge.

#### Next Sentence Prediction

The next-sentence-prediction task can be illustrated by the following examples:

```
Input  = [CLS] the man went to [MASK] store [SEP]
         he bought a gallon [MASK] milk [SEP]
Label  = IsNext

Input  = [CLS] the man [MASK] to the store [SEP]
         penguin [MASK] are flight ##less birds [SEP]
Label  = NotNext
```

### A.2 Pre-training Procedure

To generate each training input sequence, we sample two spans of text from the corpus (referred to as "sentences" even though they are typically much longer than single sentences). The first sentence receives the A embedding and the second receives the B embedding. 50% of the time, B is the actual next sentence that follows A, and 50% of the time it is a random sentence — the basis of the next-sentence-prediction task. Sentences are sampled such that the combined length is $\leq 512$ tokens. LM masking is applied after WordPiece tokenisation with a uniform masking rate of 15%.

We train with batch size of 256 sequences (256 sequences × 512 tokens = 128 000 tokens/batch) for 1 000 000 steps, which is approximately 40 epochs over the 3.3 billion-word corpus. We use Adam with learning rate 1e-4, $\beta_1 = 0.9$, $\beta_2 = 0.999$, L2 weight decay 0.01, learning-rate warmup over the first 10 000 steps, and linear decay thereafter. Dropout probability is 0.1 on all layers. We use a GeLU activation (Hendrycks and Gimpel, 2016) rather than the standard ReLU, following OpenAI GPT. The training loss is the sum of the mean masked-LM likelihood and the mean next-sentence-prediction likelihood.

Training of BERT_BASE was performed on 4 Cloud TPUs in Pod configuration (16 TPU chips total). Training of BERT_LARGE was performed on 16 Cloud TPUs (64 TPU chips total). Each pre-training took 4 days to complete.

Longer sequences are disproportionately expensive because attention is quadratic in the sequence length. To speed up pre-training, we pre-train the model with sequence length of 128 for 90% of the steps, then for the remaining 10% with sequence length 512 to learn the positional embeddings.

### A.3 Fine-tuning Procedure

For fine-tuning, most model hyperparameters are the same as in pre-training, with the exception of batch size, learning rate, and number of training epochs. The dropout probability was always kept at 0.1. The optimal hyperparameter values are task-specific, but the following ranges work well across all tasks:

- **Batch size**: 16, 32
- **Learning rate (Adam)**: 5e-5, 3e-5, 2e-5
- **Number of epochs**: 2, 3, 4

Large datasets (e.g., 100K+ labeled training examples) are far less sensitive to hyperparameter choice than small ones. Fine-tuning is typically very fast, so it is reasonable to run an exhaustive search over the above parameters and choose the model that performs best on the development set.

### A.4 Comparison of BERT, ELMo, and OpenAI GPT

The most comparable existing pre-training method to BERT is OpenAI GPT, which trains a left-to-right Transformer LM on a large text corpus. Many of BERT's design decisions were intentionally made to make it as close to GPT as possible so that the two methods could be minimally compared. Differences:

- **Corpus**: GPT is trained on the BooksCorpus (800M words); BERT is trained on the BooksCorpus (800M words) **and** Wikipedia (2 500M words).
- **Special tokens**: GPT uses a sentence separator (`[SEP]`) and classifier token (`[CLS]`) introduced only at fine-tuning time; BERT learns `[SEP]`, `[CLS]`, and sentence A/B embeddings during pre-training.
- **Batch size**: GPT was trained for 1M steps with a batch size of 32 000 words; BERT was trained for 1M steps with a batch size of 128 000 words.
- **Learning rate**: GPT used the same learning rate of 5e-5 for all fine-tuning experiments; BERT chooses a task-specific fine-tuning learning rate that performs the best on the development set.

Ablation experiments in Section 5.1 demonstrate that the majority of the improvements come from the two pre-training tasks and the bidirectionality they enable.

### A.5 Illustrations of Fine-tuning on Different Tasks

Task-specific models are formed by incorporating BERT with one additional output layer, so a minimal number of parameters need to be learned from scratch. Sequence-level tasks use the `[CLS]` representation; token-level tasks use the per-token representations $T_i$.

## Appendix B: Detailed Experimental Setup

### B.1 GLUE Benchmark Datasets

- **MNLI** — Multi-Genre Natural Language Inference: a large-scale, crowd-sourced entailment-classification task (Williams et al., 2018). Predict whether the second sentence is entailment, contradiction, or neutral with respect to the first.
- **QQP** — Quora Question Pairs: binary classification task — are two Quora questions semantically equivalent? (Chen et al., 2018)
- **QNLI** — Question Natural Language Inference: a binary classification version of SQuAD (Rajpurkar et al., 2016) recast by Wang et al. (2018a). Positive examples are (question, sentence) pairs containing the correct answer; negatives are pairs from the same paragraph that do not.
- **SST-2** — Stanford Sentiment Treebank: binary single-sentence classification of movie-review sentiment (Socher et al., 2013).
- **CoLA** — Corpus of Linguistic Acceptability: predict whether an English sentence is linguistically "acceptable" (Warstadt et al., 2018).
- **STS-B** — Semantic Textual Similarity Benchmark: sentence pairs annotated with a similarity score from 1 to 5 (Cer et al., 2017).
- **MRPC** — Microsoft Research Paraphrase Corpus: sentence pairs annotated for semantic equivalence (Dolan and Brockett, 2005).
- **RTE** — Recognising Textual Entailment: a binary entailment task similar to MNLI but with much less training data (Bentivogli et al., 2009).
- **WNLI** — Winograd NLI: a small natural-language-inference dataset (Levesque et al., 2011). Excluded due to known issues with dataset construction.

## Appendix C: Additional Ablation Studies

### C.1 Effect of Number of Training Steps

- **Q**: Does BERT really need such a large amount of pre-training (128 000 words/batch × 1 000 000 steps) to achieve high fine-tuning accuracy?
  **A**: Yes. BERT_BASE achieves almost 1.0% additional accuracy on MNLI when trained for 1M steps compared with 500K steps.

- **Q**: Does MLM pre-training converge slower than LTR pre-training, since only 15% of words are predicted in each batch?
  **A**: The MLM model converges slightly slower than the LTR model. However, in absolute accuracy the MLM model begins to outperform the LTR model almost immediately.

### C.2 Ablation for Different Masking Procedures

The purpose of the masking strategies is to reduce the mismatch between pre-training and fine-tuning, since the `[MASK]` symbol never appears at fine-tuning time.

*Table 8: Ablation over different masking strategies.*

| MASK | SAME | RND | MNLI Fine-tune | NER Fine-tune | NER Feature-based |
|---|---|---|---|---|---|
| 80% | 10% | 10% | 84.2 | 95.4 | 94.9 |
| 100% | 0% | 0% | 84.3 | 94.9 | 94.0 |
| 80% | 0% | 20% | 84.1 | 95.2 | 94.6 |
| 80% | 20% | 0% | 84.4 | 95.2 | 94.7 |
| 0% | 20% | 80% | 83.7 | 94.8 | 94.6 |
| 0% | 0% | 100% | 83.6 | 94.9 | 94.6 |

- **MASK** — replace the target token with `[MASK]`.
- **SAME** — keep the target token unchanged.
- **RND** — replace the target token with a random token.

Fine-tuning is surprisingly robust to different masking strategies. However, using only the MASK strategy is problematic when applying the feature-based approach to NER. Using only the RND strategy also performs much worse than the chosen mix.
