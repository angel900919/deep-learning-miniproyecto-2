import re

def split_into_sentences(text):
    # Split by common sentence endings followed by space and capital letter, or just space
    # This is a naive splitter for Spanish
    text = text.replace('\n', ' ')
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

with open('Material/Lecture_Transcripts/main_lecture_about_RNN.txt', 'r', encoding='utf-8') as f:
    content = f.read()

sentences = split_into_sentences(content)

with open('Material/Lecture_Transcripts/main_lecture_about_RNN_lines.txt', 'w', encoding='utf-8') as f:
    for s in sentences:
        f.write(s.strip() + '\n')
