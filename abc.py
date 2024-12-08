from transformers import pipeline

text_translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", max_length=400)

    
def translate_text(text, src_lang="hin", tgt_lang="eng_Latn", max_length=400):
    # Translate the text using NLLB-200
    translated = text_translator(text, src_lang=src_lang, tgt_lang=tgt_lang, max_length=max_length)
    return translated[0]['translation_text']