import os
import json
import urllib.request
import urllib.error

# Config for local Gemma API (OpenAI compatible)
API_URL = "http://192.168.0.115:11434/v1/chat/completions" # User's Ollama server
MODEL_NAME = "gemma4:31b" 
API_KEY = "sk-local"

def load_schema():
    with open('../data/schema.json', 'r') as f:
        return json.load(f)

def generate_article(breed, food):
    prompt = f"""
    Write a short, engaging, and highly structured SEO article answering: "Can a {breed['name']} eat {food['name']}?"
    Format it in Markdown. Include:
    1. A clear YES or NO verdict at the top.
    2. A brief explanation of why.
    3. Potential benefits or risks.
    4. How to safely prepare it (if yes) or what to do if they ate it (if no).
    Keep it concise but helpful. Do not output anything outside of the markdown content.
    """
    
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are an expert pet nutritionist and SEO writer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    req = urllib.request.Request(API_URL, data=json.dumps(data).encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {API_KEY}')
    
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        return result['choices'][0]['message']['content']
    except urllib.error.URLError as e:
        print(f"Error calling local API: {e}")
        return None

def main():
    schema = load_schema()
    output_dir = '../src/pages'
    
    for breed in schema['breeds']:
        breed_dir = os.path.join(output_dir, breed['id'])
        os.makedirs(breed_dir, exist_ok=True)
        
        for food in schema['foods']:
            print(f"Generating content for: Can {breed['name']} eat {food['name']}?")
            content = generate_article(breed, food)
            
            if content:
                file_path = os.path.join(breed_dir, f"can-eat-{food['id']}.md")
                with open(file_path, 'w') as f:
                    f.write(f"---\n")
                    f.write(f"layout: '../../layouts/Layout.astro'\n")
                    f.write(f"title: 'Can a {breed['name']} eat {food['name']}?'\n")
                    f.write(f"description: 'Find out if {food['name']} is safe for your {breed['name']} to eat.'\n")
                    f.write(f"---\n\n")
                    f.write(content)
                print(f"Saved {file_path}")
            else:
                print("Failed to generate content. Please check if your local Gemma API is running.")
                break # Stop on first failure to avoid spamming

if __name__ == "__main__":
    main()
