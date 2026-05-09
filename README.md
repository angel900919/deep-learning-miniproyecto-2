# Miniproyecto 3 — Clasificación de Artículos de la BBC con Transformers

**Curso:** MAIA-4213 Técnicas de Deep Learning · **Maestría en IA, Uniandes**
**Modalidad:** parejas

---

## 1. Qué hay que hacer

Construir un **clasificador multi-clase** que asigne a cada artículo del *BBC News Dataset* su categoría temática (`business`, `entertainment`, `politics`, `sport`, `tech`) usando un transformer preentrenado.

**Dataset:** `kagglehub.dataset_download("jacopoferretti/bbc-articles-dataset")`.

**Modelo:** transformer preentrenado (BERT o RoBERTa) con `BertForSequenceClassification` (Hugging Face `transformers`), cabeza lineal + softmax, entrenado **2–5 épocas** sobre GPU.

### Actividades obligatorias (enunciado)

1. **Preprocesamiento del texto** — limpieza, tokenización y secuencias listas para el modelo.
2. **Arquitectura de transformers** — adaptar BERT/RoBERTa a multi-clase con `BertForSequenceClassification`; justificar el modelo y la cabeza.
3. **Entrenamiento y evaluación** — split train/val/test; reportar precision, recall, F1 (global y por clase); identificar la clase con mejor y peor desempeño. Activación de salida: **softmax**.

---

## 2. Entregables

| # | Archivo | Contenido | Peso |
|---|---|---|---|
| 1 | **`.pdf`** | Informe en formato IEEE simplificado (estilo CVPR), **máximo 2 páginas** sin contar bibliografía | 90% |
| 2 | **`.ipynb`** | Notebook con el código implementado, ordenado y documentado, cuyos resultados deben coincidir con los del informe | 10% |

**Estructura obligatoria del informe:** Introducción · Metodología · Resultados (cuantitativos + cualitativos) · Discusión · Referencias (≥2, formato IEEE).

**Plantilla LaTeX:** `Project/report_template/main.tex`.

---

## 3. Rúbrica de evaluación

### Informe (90%)

| Criterio | Peso | Excelente |
|---|---|---|
| **Introducción** | 15% | Problema preciso, relevancia justificada, objetivos claros, ≥2 referencias relevantes con su rol explicado, estructura *contexto → problema → estado del arte → solución* |
| **Metodología** | 15% | Pipeline completo (datos → preprocesamiento → modelo → entrenamiento → evaluación) con hiperparámetros, métricas justificadas y nivel de detalle reproducible |
| **Resultados cuantitativos** | 15% | Métricas adecuadas (accuracy, precision, recall, F1 macro y por clase), tablas/figuras autocontenidas y referenciadas, comparaciones entre configuraciones |
| **Resultados cualitativos** | 10% | Ejemplos concretos de predicción vs etiqueta real, aciertos y errores ilustrativos |
| **Discusión** | 15% | Conexión con teoría (overfitting, capacidad, sesgo-varianza), comparaciones, limitaciones, mejoras propuestas con literatura |
| **Redacción y ortografía** | 10% | — |
| **Formato IEEE** | 10% | Estructura completa, citas correctas, ≤2 páginas estrictas |

### Código (10%)

| Criterio | Peso | Excelente |
|---|---|---|
| **Entrega `.ipynb`** | 5% | Archivo en formato `.ipynb` con el código del miniproyecto |
| **Orden y documentación** | 5% | Código documentado, ordenado, con resultados que reproducen exactamente las cifras del informe |

### Penalización

| Criterio | Peso |
|---|---|
| **Longitud del informe** | **−20%** si excede 2 páginas (sin contar bibliografía) |

---

## 4. Errores que destruyen calificación

- Pasar de 2 páginas (penalización fija del −20%).
- No incluir referencias o usarlas mal.
- Reportar números sin interpretarlos.
- Figuras sin numerar, describir ni referenciar.
- Notebook desordenado o cuyas cifras no cuadran con el informe.

---
