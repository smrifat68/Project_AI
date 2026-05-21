import gradio as gr
from deep_translator import GoogleTranslator

# Call on an instance to get supported languages
SUPPORTED_LANGUAGES = GoogleTranslator(source="auto", target="en").get_supported_languages(as_dict=True)

# Capitalize for display in UI
all_languages = sorted([name.capitalize() for name in SUPPORTED_LANGUAGES.keys()])


def perform_translation(text: str, target_lang: str) -> str:
    #Translate input text into the chosen target language.
    if not text.strip():
        return " Please enter some text to translate."
    try:
        target_key = target_lang.lower()
        translated = GoogleTranslator(source="auto", target=target_key).translate(text)
        return translated
    except Exception as e:
        return f"Translation Error: {str(e)}"



# theme moved to launch() in Gradio 6.0, not Blocks()
with gr.Blocks() as demo:

    gr.Markdown("  AI Universal Translator")
    gr.Markdown("Enter text and pick a target language — translation is instant.")

    with gr.Row():

        with gr.Column():
            input_box = gr.Textbox(
                label="Source Text",
                placeholder="Type or paste text here…",
                lines=7,
            )
            lang_dropdown = gr.Dropdown(
                choices=all_languages,
                label="Target Language",
                value="Bengali",
                filterable=True,
            )
            submit_btn = gr.Button("Translate 🚀", variant="primary")

        with gr.Column():
            # show_copy_button removed in Gradio 6.0 — use a separate button
            output_box = gr.Textbox(
                label="Translated Result",
                lines=7,
                interactive=False,
            )
            copy_btn = gr.Button("📋 Copy to Clipboard")

    # Translate on button click
    submit_btn.click(
        fn=perform_translation,
        inputs=[input_box, lang_dropdown],
        outputs=output_box,
    )

    # Also translate on Enter key
    input_box.submit(
        fn=perform_translation,
        inputs=[input_box, lang_dropdown],
        outputs=output_box,
    )

    # Copy to clipboard via JavaScript
    copy_btn.click(
        fn=None,
        inputs=output_box,
        js="(text) => { navigator.clipboard.writeText(text); alert('Copied!'); }"
    )


if __name__ == "__main__":
    # theme is now passed here in Gradio 6.0
    demo.launch(share=True, theme=gr.themes.Soft())