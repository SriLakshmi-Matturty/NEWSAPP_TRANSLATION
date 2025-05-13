import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get your API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env file")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Indian languages
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

# Read input.json
with open("input.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    headline = data.get("headline", "")
    summary = data.get("summary", "")
    lang_code = data.get("language", "").strip()
    date = data.get("date", "")
    time = data.get("time", "")

if lang_code not in target_languages:
    raise ValueError(f"Invalid language code: {lang_code}")
target_language_name = target_languages[lang_code]

# Translation function
def translate_text(text, target_language_name):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates news headlines and summaries."},
            {"role": "user", "content": f"Translate the following to {target_language_name}:\n{text}"}
        ]
    )
    return response.choices[0].message.content

# Translate both fields
translated_headline = translate_text(headline, target_language_name)
translated_summary = translate_text(summary, target_language_name)

# Prepare output
output_data = {
    "headline": headline,
    "translated_headline": translated_headline,
    "translated_text": translated_summary,
    "language": target_language_name,
    "date": date,
    "time": time
}

# Save output
with open("output.json", "w", encoding="utf-8") as file:
    json.dump(output_data, file, ensure_ascii=False, indent=4)

print("✅ Translation saved to output.json")
