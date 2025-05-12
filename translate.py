import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

# Supported Indian languages
target_languages = {
    'as': 'Assamese',
    'bn': 'Bengali',
    'bho': 'Bhojpuri',
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'kn': 'Kannada',
    'kok': 'Konkani',
    'mai': 'Maithili',
    'ml': 'Malayalam',
    'mni-Mtei': 'Manipuri',
    'mr': 'Marathi',
    'or': 'Odia',
    'pa': 'Punjabi',
    'sa': 'Sanskrit',
    'sd': 'Sindhi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ur': 'Urdu',
}

# Read input JSON file
with open("input.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    headline = data.get("headline", "")
    summary = data.get("summary", "")
    lang_code = data.get("language", "").strip()
    date = data.get("date", "")
    time = data.get("time", "")

# Validate language code
if lang_code not in target_languages:
    raise ValueError(f"Invalid language code: {lang_code}")

# Get full language name
target_language_name = target_languages[lang_code]

# Prepare translation prompt
def translate_text(text, target_language):
    prompt = f"Translate the following text into {target_language}:\n\n\"{text}\""
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Translate the following text to " + target_language_name + ": " + text,
        max_tokens=100
    )

    return response['choices'][0]['message']['content'].strip()

# Translate headline and summary
translated_headline = translate_text(headline, target_language_name)
translated_summary = translate_text(summary, target_language_name)

# Prepare output data
output_data = {
    "headline": headline,
    "translated_headline": translated_headline,
    "translated_text": translated_summary,
    "language": target_language_name,
    "date": date,
    "time": time
}

# Save output JSON file
with open("output.json", "w", encoding="utf-8") as file:
    json.dump(output_data, file, ensure_ascii=False, indent=4)

print("Translation saved to output.json")
