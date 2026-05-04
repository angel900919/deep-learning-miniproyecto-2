# Clasificación Multi-Etiqueta de Artículos de Noticias de la BBC usando Transformers

Los artículos de noticias contienen una gran cantidad de información categórica y temática, con temas que abarcan desde política y tecnología hasta deportes y cultura. Muchos artículos pueden abarcar varios temas a la vez. Este proyecto tiene como objetivo desarrollar un sistema de clasificación multi-clase que pueda asignar una categoría a cada artículo de noticias de la BBC, utilizando la potencia de los modelos transformer para capturar el contexto y asignar etiquetas múltiples de manera precisa.

## Introducción a los Transformers

Los modelos basados en transformers, como BERT, son especialmente adecuados para analizar texto debido a su capacidad para entender relaciones contextuales complejas entre palabras y frases. Esto permite a los transformers abordar de manera efectiva la clasificación multi-clase, capturando de manera simultánea la pertenencia de un artículo a múltiples temas sin necesidad de procesar secuencialmente, como ocurre en los modelos recurrentes.

## Objetivo

• Desarrollar un modelo de clasificación multi-clase basado en transformers que

identifique la categoría de artículos de noticias de la BBC. Conjunto de Datos

- • Utilizaremos un dataset de artículos de la BBC etiquetados con múltiples categorías temáticas, como "Sport", "Bussiness", "Politics", "Tech", entre otros.
- • Los datos los pueden obtener usando la siguiente línea de código en Python: kagglehub.dataset_download("jacopoferretti/bbc-articles-dataset")


## Actividades por Realizar

- 1. Preprocesamiento del Texto: Crear un pipeline para procesar los artículos, incluyendo la limpieza del texto, tokenización y la preparación de secuencias utilizando embeddings derivados de un modelo preentrenado como BERT. En


- este paso se debe garantizar que el texto y las etiquetas estén en el formato adecuado para ser interpretado por el modelo de clasificación multi-clase.
- 2. Implementación de la Arquitectura de Transformers: Usar un modelo de transformers preentrenado, como BERT o RoBERTa, y adaptarlo a la clasificación multi-clase. Esto implicará añadir una capa de salida que permita al modelo generar una predicción de la categoría. Para ello, puede utilizar el método BertForSequenceClassification, disponible en la librería “transformers” vista en el laboratorio de la semana. Recuerde justificar la elección del modelo y de las capas adicionales, explicando cómo cada ajuste facilita la tarea de clasificación multi-clase.
- 3. Entrenamiento y Evaluación del Modelo: Dividir el dataset en conjuntos de entrenamiento, validación y prueba. Entrenar el modelo en el conjunto de entrenamiento y evaluar su rendimiento con el conjunto de prueba. Reportar métricas como precisión, recall, F1-score, y también un análisis de precisión para cada categoría, resaltando las categorías en las que el modelo presenta un mejor o peor rendimiento. Puede utilizar una GPU para entrenar el modelo durante 2 a 5 épocas, recuerde que el problema es un problema de clasificación multi-clase, donde la función de activación debería ser softmax.


