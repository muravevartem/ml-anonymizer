import re

import math
import spacy
from collections import Counter

EMAIL_PATTERN = re.compile(
    r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
)

PHONE_PATTERN = re.compile(
    r'(?<!\d)(?:\+7|8)\s*(?:\(?\d{3}\)?)[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?!\d)'
)

CARD_PATTERN = re.compile(
    r'(?<!\d)(?:\d[ -]?){13,19}(?!\d)'
)

def shannon_entropy(s: str) -> float:
    counts = Counter(s)
    length = len(s)
    return -sum(
        (count / length) * math.log2(count / length)
        for count in counts.values()
    )

PASSWORD_PATTERN = re.compile(r'\b\S{8,}\b')

def anonymize_passwords(source_text, min_entropy=3.0):
    def replace(match):
        token = match.group()
        entropy = shannon_entropy(token)

        if entropy >= min_entropy:
            return '[PASSWORD]'
        return token

    return PASSWORD_PATTERN.sub(replace, source_text)

def anonymize(source_text):
    anon_text = source_text

    # регулярка
    anon_text = EMAIL_PATTERN.sub('[EMAIL]', anon_text)
    anon_text = PHONE_PATTERN.sub('[PHONE]', anon_text)
    anon_text = CARD_PATTERN.sub('[CARD]', anon_text)

    # анализ случайности
    anon_text = anonymize_passwords(anon_text)

    # NER
    doc = nlp(source_text)
    for ent in reversed(doc.ents):
        anon_text = anon_text[:ent.start_char] + f'[{ent.label_}]' + anon_text[ent.end_char:]
    return anon_text

nlp = spacy.load('ru_core_news_md')

text = """
Логин: ivan
Пароль: Xy9!kQ2$LmP
Email: ivan@mail.main
Телефон: +7 999 123-45-67
Карта: 4276 3800 1234 5678
Работает в Яндекс
"""

print(anonymize(text))  # Привет, [PER]! Как дела? Ты звонил [PER]? Он недавно устроился в [ORG]
