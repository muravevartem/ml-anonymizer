import spacy

def anonymize(source_text):
    nlp = spacy.load('ru_core_news_sm')
    doc = nlp(source_text)
    anon_text = source_text
    for ent in reversed(doc.ents):
        anon_text = anon_text[:ent.start_char] + f'[{ent.label_}]' + anon_text[ent.end_char:]
    return anon_text

text = "Привет, Иван! Как дела? Ты звонил Андрею? Он недавно устроился в Яндекс"
print(anonymize(text)) # Привет, [PER]! Как дела? Ты звонил [PER]? Он недавно устроился в [ORG]
