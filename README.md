# Miniproyecto 3 — Clasificación de Artículos de Noticias de la BBC con Transformers

Curso: **MAIA-4213 Técnicas de Deep Learning** (Maestría en Inteligencia Artificial, Uniandes).
Modalidad: **parejas**.
Fecha de elaboración del README: 2026-05-04.

---

## 1. ¿De qué trata el proyecto?

El objetivo es construir un **clasificador de artículos de noticias de la BBC** que asigne a cada artículo la categoría temática a la que pertenece (por ejemplo *Sport*, *Business*, *Politics*, *Tech*, *Entertainment*), aprovechando la capacidad de los **modelos transformer preentrenados** para capturar relaciones contextuales complejas en texto.

Aunque el enunciado menciona en el título "multi-etiqueta", la **Actividad 3** aclara explícitamente que el problema es de **clasificación multi-clase** (una sola etiqueta por artículo) y que la función de activación de salida debe ser **softmax**. Trabajaremos por tanto el problema como **multi-clase de etiqueta única** (no multi-label), lo que es consistente con el dataset estándar de BBC News.

### Dataset

- BBC Articles Dataset (Kaggle, autor *jacopoferretti*).
- Descarga sugerida en Python:

  ```python
  import kagglehub
  path = kagglehub.dataset_download("jacopoferretti/bbc-articles-dataset")
  ```

- Categorías típicas: *business*, *entertainment*, *politics*, *sport*, *tech*.

### Modelo recomendado

- Transformer preentrenado tipo **BERT** o **RoBERTa**.
- Cabezal de clasificación vía `BertForSequenceClassification` de la librería `transformers` (Hugging Face), tal como se usó en el laboratorio de la semana.
- Entrenamiento de **2 a 5 épocas** sobre **GPU**.

### Relación con el laboratorio previo

El laboratorio de transformers (`Material/Labs/LaboratorioTransformersDeLenguajeV3.ipynb`) usaba **DistilBERT** como *encoder* fijo + una **regresión logística** clásica para clasificación binaria de sentimientos (SST2, 2 clases). Este proyecto exige dar el siguiente paso:

| Aspecto | Laboratorio (sentimientos) | Miniproyecto 3 (BBC) |
|---|---|---|
| Tarea | Binaria (positivo/negativo) | Multi-clase (≈5 categorías) |
| Encoder | DistilBERT (congelado) | BERT/RoBERTa (preferiblemente fine-tuning) |
| Cabeza | Regresión logística externa (sklearn) | Capa lineal + softmax dentro del modelo (`BertForSequenceClassification`) |
| Pérdida | Logística (sklearn) | CrossEntropy (PyTorch) |
| Optimización | No aplica al transformer | AdamW + scheduler, fine-tuning end-to-end |

Conviene **reutilizar el pipeline de tokenización, padding y máscaras de atención** del laboratorio, pero **dejar atrás la regresión logística** y entrenar la cabeza de clasificación dentro del propio transformer para aprovechar el fine-tuning.

---

## 2. Entregables

Según `Generalidades sobre los miniproyectos` y la rúbrica `202611_Rubrica_MNP_MAIA_4213.md`:

1. **Informe en PDF** — máximo **2 páginas** (sin contar bibliografía), formato **IEEE simplificado** (estilo CVPR), siguiendo la plantilla de `Project/report_template/main.tex`. Penalización del **-20%** si excede 2 páginas.
2. **Jupyter Notebook (`.ipynb`)** con todo el código que produjo los resultados del informe. Debe estar **ordenado, documentado y reproducible**, y los resultados que se muestren deben **coincidir** con los del informe.

Frameworks: libre (PyTorch o TensorFlow). El equipo docente **recomienda PyTorch** por ser el estándar de las electivas de la maestría y de la industria — y además es lo que usa la librería `transformers` en sus ejemplos canónicos.

### Estructura obligatoria del informe (plantilla IEEE)

1. **Introducción** — contexto, problema, relevancia, objetivos, ≥2 referencias en Deep Learning, breve descripción del enfoque.
2. **Metodología** — dataset, preprocesamiento, arquitectura, hiperparámetros, métricas, justificación de decisiones, reproducibilidad.
3. **Resultados** — cuantitativos (tablas/gráficos: precisión, recall, F1 macro y por clase, matriz de confusión) y cualitativos (ejemplos de aciertos/errores con texto + etiqueta real + predicción).
4. **Discusión** — análisis profundo, conexión con teoría del curso (overfitting, sesgo-varianza, capacidad del modelo), limitaciones, mejoras propuestas, citas a literatura.
5. **Referencias** — formato IEEE (`[1]`, `[2]`...).

---

## 3. ¿Qué espera el profesor? (Rúbrica resumida)

Distribución de la calificación:

| Bloque | Peso |
|---|---|
| **Informe** | **90%** |
| Introducción | 15% |
| Metodología | 15% |
| Resultados cualitativos | 10% |
| Resultados cuantitativos | 15% |
| Discusión | 15% |
| Redacción y ortografía | 10% |
| Formato IEEE | 10% |
| **Código** | **10%** |
| Entrega del `.ipynb` | 5% |
| Orden y documentación | 5% |
| **Penalización** | **-20%** si el informe excede 2 páginas |

### Criterios para puntaje "Excelente" (1.0–0.75)

- **Introducción**: problema definido con precisión, relevancia justificada, objetivos claros, ≥2 referencias relevantes con su rol explicado, y descripción del enfoque ubicada lógicamente en el flujo *contexto → problema → estado del arte → solución*.
- **Metodología**: pipeline completo (datos → preprocesamiento → modelo → entrenamiento → evaluación) con hiperparámetros relevantes, métricas justificadas y nivel de detalle suficiente para que un tercero pueda reproducir el experimento.
- **Resultados cuantitativos**: métricas adecuadas al problema (accuracy, precision, recall, F1 — en clasificación multi-clase: F1 macro **y** F1 por clase), tablas/figuras autocontenidas y referenciadas en el texto, comparaciones (por ejemplo entre modelos o configuraciones).
- **Resultados cualitativos**: ejemplos concretos de **predicción vs etiqueta real**, organizados con subplots/tablas, mostrando aciertos y errores ilustrativos.
- **Discusión**: ir más allá de describir números; conectar con teoría (overfitting, capacidad, sesgo-varianza), comparar configuraciones, identificar limitaciones, proponer mejoras y respaldar con literatura.
- **Formato**: estructura IEEE completa, citas en el texto correctamente referenciadas, ≤2 páginas estrictas (sin bibliografía).
- **Código**: limpio, documentado y con resultados que reproducen exactamente las cifras del informe.

### Errores que destruyen calificación (señalados explícitamente)

- Pasar de 2 páginas (penalización fija del -20%).
- No incluir referencias o usarlas mal.
- Reportar números sin interpretarlos.
- Figuras sin numerar, describir ni referenciar.
- Notebook desordenado o cuyas cifras no cuadran con el informe.

---

## 4. Fases sugeridas para el Jupyter Notebook

El enunciado en `Miniproyecto_3.md` plantea explícitamente **tres actividades** que se traducen en las fases 4–6 de abajo. Las fases 1–3 son la preparación habitual y las fases 7–9 son el cierre necesario para llenar las secciones de Resultados y Discusión del informe. Esta es una guía completa, no una rúbrica adicional.

> **Tip de portabilidad**: si vas a entrenar en Colab/Kaggle, separa el notebook en celdas pequeñas y guarda los pesos del modelo + métricas en disco al final de cada fase para no tener que reentrenar al revisar.

### Fase 0 — Setup del entorno

- Instalar dependencias: `transformers`, `datasets`, `kagglehub`, `torch`, `scikit-learn`, `pandas`, `matplotlib`, `seaborn`.
- Detectar GPU: `torch.cuda.is_available()`, fijar `device`.
- **Fijar semillas** (`torch`, `numpy`, `random`) — clave para reproducibilidad.

### Fase 1 — Carga y exploración del dataset (EDA)

- Descarga vía `kagglehub.dataset_download("jacopoferretti/bbc-articles-dataset")`.
- Cargar a `pandas.DataFrame`. Identificar columnas (texto y etiqueta).
- **EDA imprescindible para el informe**:
  - Distribución de clases (gráfico de barras → ¿está balanceado?).
  - Distribución de longitudes de texto en *tokens* — define `max_length`.
  - Ejemplos crudos de cada clase.
- **Guardar 2-3 figuras** que servirán para la sección de Metodología/Resultados.

### Fase 2 — Preprocesamiento

- Limpieza ligera (saltos de línea, espacios redundantes — **no** eliminar mayúsculas/puntuación; BERT las usa).
- **Codificación de etiquetas** (`LabelEncoder` o diccionario explícito `id2label`/`label2id`).
- **Tokenización** con el tokenizer del modelo elegido (`AutoTokenizer.from_pretrained(...)`):
  - `padding="max_length"` o dinámico,
  - `truncation=True`,
  - `max_length` típicamente 256–512 (BERT base soporta hasta 512). Justifica el valor según la distribución de la fase 1.
- Generar `input_ids`, `attention_mask`. Si usas BERT: opcionalmente `token_type_ids`.
- **Split estratificado** en train / validation / test (típico: 70/15/15 u 80/10/10).
- Convertir a `torch.utils.data.Dataset` o `datasets.Dataset` y empaquetar en `DataLoader`s con `batch_size` adecuado a la VRAM (16 o 32 suelen funcionar para BERT-base en una T4/V100).

### Fase 3 — Definición de la arquitectura

- Cargar `BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=N, id2label=..., label2id=...)` (o RoBERTa equivalente).
- **Justificar la elección en el informe**: por qué BERT/RoBERTa, por qué `bert-base-uncased` vs `cased`, por qué la cabeza lineal + softmax incluida en `*ForSequenceClassification` es suficiente para multi-clase.
- Mover a GPU.

### Fase 4 — Entrenamiento (Actividad 2 + 3 del enunciado)

- **Optimizador**: `AdamW`, `lr` típico para fine-tuning de BERT: `2e-5` a `5e-5`.
- **Scheduler**: linear warmup + decay (`get_linear_schedule_with_warmup`).
- **Pérdida**: `CrossEntropyLoss` (la trae integrada `BertForSequenceClassification`).
- **Épocas**: 2–5 (el enunciado lo dice explícitamente; más es habitualmente innecesario y arriesga overfitting).
- **Loop de entrenamiento**: por época, calcular pérdida y métricas en train **y** validation; guardar `best_model` por F1 de validación.
- Registrar **curvas de loss y F1** por época — figura clave para la discusión sobre overfitting.

### Fase 5 — Evaluación cuantitativa (Actividad 3 del enunciado)

- Sobre el conjunto de **test** (no validation):
  - **Accuracy global**.
  - **Precision, Recall, F1** — macro **y** por clase (`sklearn.metrics.classification_report`).
  - **Matriz de confusión** (con `seaborn.heatmap`).
- Identificar las clases con **mejor y peor desempeño** — el enunciado lo pide explícitamente.

### Fase 6 — Resultados cualitativos

- Mostrar al menos:
  - 3-5 ejemplos de predicciones **correctas** con probabilidad (softmax).
  - 3-5 ejemplos de predicciones **incorrectas**, con etiqueta real y predicción.
  - Si es posible, ejemplos cerca de la frontera de decisión (probabilidad máxima baja).
- Esta fase alimenta directamente la sección de *Resultados cualitativos* del informe (10%).

### Fase 7 — Análisis y discusión (insumo para la sección Discusión)

- Confrontar los hallazgos con teoría: ¿hay overfitting? (mirar curvas), ¿la capacidad del modelo es excesiva o limitada?, ¿hay sesgo por desbalance de clases?, ¿qué errores son sistemáticos?
- Comparar al menos **dos configuraciones** (por ejemplo BERT vs DistilBERT, o `lr=2e-5` vs `lr=5e-5`, o con/sin `warmup`) — la rúbrica de "Excelente" pide explícitamente comparaciones entre experimentos.
- Discutir limitaciones (tamaño del dataset, idioma, sesgos editoriales de la BBC, costo computacional) y proponer mejoras (ensembles, data augmentation textual, modelos más grandes).

### Fase 8 — Persistencia y reproducibilidad

- Guardar el mejor modelo y el tokenizer (`model.save_pretrained(...)`, `tokenizer.save_pretrained(...)`).
- Exportar las métricas finales a un JSON/CSV.
- Imprimir resumen final de hiperparámetros y resultados — eso es lo que copiarás a la tabla del informe.

### Checklist final antes de entregar

- [ ] El notebook **se ejecuta de principio a fin sin error** en un entorno limpio.
- [ ] Cada celda tiene una explicación corta de qué hace.
- [ ] Los **números del notebook coinciden** con los del informe (rúbrica explícita).
- [ ] El informe está en **≤2 páginas** sin contar bibliografía.
- [ ] Todas las figuras y tablas están **numeradas y referenciadas** en el texto en formato IEEE.
- [ ] ≥2 referencias en la bibliografía, ambas relevantes y citadas en el texto.
- [ ] Discusión incluye limitaciones y propuestas de mejora.
- [ ] PDF + `.ipynb` listos para entregar.

---

## 5. Mapa de archivos del proyecto

```
Project/
├── Generalidades sobre los miniproyectos _ Coursera.md   # reglas generales de entrega
├── Miniproyecto_3.md                                     # enunciado del miniproyecto
├── 202611_Rubrica_MNP_MAIA_4213.md                       # rúbrica de evaluación
├── README.md                                             # este archivo
└── report_template/
    ├── main.tex                                          # plantilla LaTeX IEEE
    ├── ieeeconf.cls                                      # clase IEEE
    └── Template_diffusion_models.png                     # figura de ejemplo
```

## 6. Referencias útiles para arrancar

- Devlin et al., *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*, NAACL 2019.
- Liu et al., *RoBERTa: A Robustly Optimized BERT Pretraining Approach*, 2019.
- Sanh et al., *DistilBERT, a distilled version of BERT*, 2019 (visto en el laboratorio).
- Documentación oficial de `transformers`: https://huggingface.co/docs/transformers
- Tutorial canónico de fine-tuning con `Trainer`: https://huggingface.co/docs/transformers/training
