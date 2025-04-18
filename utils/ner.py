import spacy

nlp = spacy.load("en_core_web_sm")

def extract_named_entities(texts):
    results = []
    for text in texts:
        doc = nlp(text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        results.append(entities)
    return results
