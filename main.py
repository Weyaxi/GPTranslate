from flask import Flask, render_template, request
from flask import jsonify
import openai
import json

openai.api_key = "<api_key>"

app = Flask(__name__)
language_dict = {"af": "Afrikaans", "sq": "Albanian", "am": "Amharic", "ar": "Arabic", "hy": "Armenian",
                 "az": "Azerbaijani", "eu": "Basque", "be": "Belarusian", "bn": "Bengali", "bs": "Bosnian",
                 "bg": "Bulgarian", "ca": "Catalan", "ceb": "Cebuano", "ny": "Chichewa",
                 "zh-CN": "Chinese (Simplified)", "zh-TW": "Chinese (Traditional)", "co": "Corsican", "hr": "Croatian",
                 "cs": "Czech", "da": "Danish", "nl": "Dutch", "en": "English", "eo": "Esperanto", "et": "Estonian",
                 "tl": "Filipino", "fi": "Finnish", "fr": "French", "fy": "Frisian", "gl": "Galician", "ka": "Georgian",
                 "de": "German", "el": "Greek", "gu": "Gujarati", "ht": "Haitian Creole", "ha": "Hausa",
                 "haw": "Hawaiian", "he": "Hebrew", "iw": "Hebrew (deprecated)", "hi": "Hindi", "hmn": "Hmong",
                 "hu": "Hungarian", "is": "Icelandic", "ig": "Igbo", "id": "Indonesian", "ga": "Irish", "it": "Italian",
                 "ja": "Japanese", "jw": "Javanese", "kn": "Kannada", "kk": "Kazakh", "km": "Khmer", "ko": "Korean",
                 "ku": "Kurdish (Kurmanji)", "ky": "Kyrgyz", "lo": "Lao", "la": "Latin", "lv": "Latvian",
                 "lt": "Lithuanian", "lb": "Luxembourgish", "mk": "Macedonian", "mg": "Malagasy", "ms": "Malay",
                 "ml": "Malayalam", "mt": "Maltese", "mi": "Maori", "mr": "Marathi", "mn": "Mongolian",
                 "my": "Myanmar (Burmese)", "ne": "Nepali", "no": "Norwegian", "or": "Odia (Oriya)", "ps": "Pashto",
                 "fa": "Persian", "pl": "Polish", "pt": "Portuguese", "pa": "Punjabi", "ro": "Romanian",
                 "ru": "Russian", "sm": "Samoan", "gd": "Scots Gaelic", "sr": "Serbian", "st": "Sesotho", "sn": "Shona",
                 "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", "so": "Somali", "es": "Spanish",
                 "su": "Sundanese", "sw": "Swahili", "sv": "Swedish", "tg": "Tajik", "ta": "Tamil", "tt": "Tatar",
                 "te": "Telugu", "th": "Thai", "tr": "Turkish", "tk": "Turkmen", "uk": "Ukrainian", "ur": "Urdu",
                 "ug": "Uyghur", "uz": "Uzbek", "vi": "Vietnamese", "cy": "Welsh", "xh": "Xhosa", "yi": "Yiddish",
                 "yo": "Yoruba", "zu": "Zulu"}


@app.route('/languages')
def get_languages():
    return jsonify(language_dict)


@app.route('/')
def index():
    return render_template('index.html')


def translate_openai(text, from_lang, to_lang):
    my_prompt = f"""I want you to act as a translator from {language_dict[from_lang]} to {language_dict[to_lang]}.
I will speak to you in {language_dict[from_lang]} or English and you will translate in {language_dict[to_lang]}.
Your output should be in json format with optional 'translation' (string, only include the translation and nothing else, do not write explanations here), 'notes' (string) and 'success' (boolean) fields.
If an input cannot be translated, return it unmodified."""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": my_prompt},
            {"role": "user", "content": text}
        ]
    )

    response_json = completion.choices[0].message.content
    response = json.loads(response_json)['translation']
    # print(f"Tokens used: {str(completion.usage['total_tokens'])}")

    return response


@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    from_language = request.form['from']
    to_language = request.form['to']

    translated_text = str(translate_openai(text, from_language, to_language))

    return jsonify({'translated_text': translated_text})


if __name__ == '__main__':
    app.run(debug=True)
