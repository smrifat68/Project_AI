from deep_translator import GoogleTranslator
SUPPORTED_LANGUAGES = GoogleTranslator(source="auto", target="en").get_supported_languages(as_dict=True)
# print(SUPPORTED_LANGUAGES)
all_languages = sorted([name.capitalize() for name in SUPPORTED_LANGUAGES.keys()])
print(all_languages)