import math
import re
from collections import Counter

import spacy

PASSWORD_PATTERN = re.compile(r'\b\S{8,}\b')
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'(?<!\d)(?:\+7|8)\s*(?:\(?\d{3}\)?)[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?!\d)')
CARD_PATTERN = re.compile(r'(?<!\d)(?:\d[ -]?){13,19}(?!\d)')

nlp = spacy.load("ru_core_news_md")
nlp_en = spacy.load("en_core_web_md")


class Anonymizer:
    def anonymize(self, message: str) -> str:
        message = self._anonymize_card(message)
        message = self._anonymize_email(message)
        message = self._anonymize_phone(message)
        message = self._anonymize_passwords(message)
        message = self._anonymize_pers(message)
        message = self._anonymize_nlp_en(message)
        return message

    @staticmethod
    def _shannon_entropy(text: str) -> float:
        counts = Counter(text)
        length = len(text)
        return -sum(
            (count / length) * math.log2(count / length)
            for count in counts.values()
        )

    @staticmethod
    def _anonymize_passwords(text: str) -> str:
        def replace(match):
            token = match.group()
            entropy = Anonymizer._shannon_entropy(token)

            if entropy >= 2.4:
                return '[PASSWORD]'
            return token

        return PASSWORD_PATTERN.sub(replace, text)

    @staticmethod
    def _anonymize_email(text: str) -> str:
        return EMAIL_PATTERN.sub('[EMAIL]', text)

    @staticmethod
    def _anonymize_phone(text: str) -> str:
        return PHONE_PATTERN.sub('[PHONE]', text)

    @staticmethod
    def _anonymize_card(text: str) -> str:
        return CARD_PATTERN.sub('[CARD]', text)

    @staticmethod
    def _anonymize_pers(text: str) -> str:
        doc = nlp(text)
        for ent in reversed(doc.ents):
            text = text[:ent.start_char] + f'[{ent.label_}]' + text[ent.end_char:]
        return text

    @staticmethod
    def _anonymize_nlp_en(text: str) -> str:
        doc = nlp_en(text)
        for ent in reversed(doc.ents):
            text = text[:ent.start_char] + f'[{ent.label_}]' + text[ent.end_char:]
        return text

anonymizer = Anonymizer()
