import os
import json
import urllib.request
import urllib.error

# Config for local Gemma API (OpenAI compatible)
API_URL = "http://192.168.0.115:11434/v1/chat/completions" # User's Ollama server
MODEL_NAME = "gemma4:31b" 
API_KEY = "sk-local"

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def extract_entities(query):
    # Call LLM to extract breed and food from the raw query
    prompt = f"""
    Extract the dog breed and the food item from this user query: "{query}"
    Return ONLY a raw JSON object with no markdown formatting or extra text.
    Format:
    {{
      "breedName": "Golden Retriever",
      "breedId": "golden-retriever",
      "foodName": "Apples",
      "foodId": "apples",
      "category": "Food"
    }}
    If you cannot find a dog breed, default to "Dog" and breedId "dog".
    """
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    req = urllib.request.Request(API_URL, data=json.dumps(data).encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        content = result['choices'][0]['message']['content']
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        print(f"Extraction failed: {e}")
        return None

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
    
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        return result['choices'][0]['message']['content']
    except urllib.error.URLError as e:
        print(f"Error calling local API: {e}")
        return None

def process_pending():
    pending_path = '../data/pending.json'
    schema_path = '../data/schema.json'
    
    pending = load_json(pending_path)
    if not pending:
        print("No pending queries to process.")
        return
        
    schema = load_json(schema_path)
    remaining = []
    
    for item in pending:
        print(f"Processing queued search: {item['breedName']}")
        
        entities = extract_entities(item['breedName'])
        if not entities:
            print("Failed to extract entities. Skipping.")
            remaining.append(item)
            continue
            
        breed = {
            "id": entities.get('breedId', 'dog').lower().replace(' ', '-'),
            "name": entities.get('breedName', 'Dog'),
            "emoji": "🐶"
        }
        food = {
            "id": entities.get('foodId', 'food').lower().replace(' ', '-'),
            "name": entities.get('foodName', 'Food'),
            "category": entities.get('category', 'Unknown')
        }
        
        print(f"Generating content for: Can {breed['name']} eat {food['name']}?")
        content = generate_article(breed, food)
        
        if content:
            output_dir = '../src/pages'
            breed_dir = os.path.join(output_dir, breed['id'])
            os.makedirs(breed_dir, exist_ok=True)
            file_path = os.path.join(breed_dir, f"can-eat-{food['id']}.md")
            
            with open(file_path, 'w') as f:
                f.write(f"---\n")
                f.write(f"layout: '../../layouts/Layout.astro'\n")
                f.write(f"title: 'Can a {breed['name']} eat {food['name']}?'\n")
                f.write(f"description: 'Find out if {food['name']} is safe for your {breed['name']} to eat.'\n")
                f.write(f"---\n\n")
                f.write(content)
            print(f"Saved {file_path}")
            
            # Update Schema
            if not any(b['id'] == breed['id'] for b in schema['breeds']):
                schema['breeds'].append(breed)
            if not any(f['id'] == food['id'] for f in schema['foods']):
                schema['foods'].append(food)
        else:
            print("Failed to generate article.")
            remaining.append(item)

    save_json(schema_path, schema)
    save_json(pending_path, remaining)
    print("Pending queue processed. Run 'npm run build' to apply changes.")

def main():
    # Process the search queue first
    process_pending()
    
    # Then generate missing items from standard schema
    schema = load_json('../data/schema.json')
    output_dir = '../src/pages'
    
    for breed in schema['breeds']:
        breed_dir = os.path.join(output_dir, breed['id'])
        os.makedirs(breed_dir, exist_ok=True)
        
        for food in schema['foods']:
            file_path = os.path.join(breed_dir, f"can-eat-{food['id']}.md")
            if os.path.exists(file_path):
                continue # Skip if already exists
                
            print(f"Generating bulk content for: Can {breed['name']} eat {food['name']}?")
            content = generate_article(breed, food)
            
            if content:
                with open(file_path, 'w') as f:
                    f.write(f"---\n")
                    f.write(f"layout: '../../layouts/Layout.astro'\n")
                    f.write(f"title: 'Can a {breed['name']} eat {food['name']}?'\n")
                    f.write(f"description: 'Find out if {food['name']} is safe for your {breed['name']} to eat.'\n")
                    f.write(f"---\n\n")
                    f.write(content)
                print(f"Saved {file_path}")

if __name__ == "__main__":
    main()
