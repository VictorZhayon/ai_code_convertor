import os
import random
import openai
from flask import Flask, request, jsonify

# include your own API key. 
openai.api_key = ""

app = Flask(__name__)

def get_python_files(folder_path):
    # lists all files in the directory 
    # and filters them to return only those that end with .py
    return [f for f in os.listdir(folder_path) if f.endswith('.py')]

def read_file(file_path):
    # opens a specified file in read mode 
    # and returns its content as a string
    with open(file_path, 'r') as file:
        return file.read()

def generate_markdown_output(content):
    # sends a request to the OpenAI API, 
    # asking it to document the provided Python code from the file
    # The response is then extracted and returned
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Please document the following Python code in English:\n\n{content}"}
        ]
    )
    return response['choices'][0]['message']['content']

def save_markdown_file(folder_path, file_name, content):
    # creates the path for the Markdown file 
    # and writes the generated documentation to it
    markdown_file_path = os.path.join(folder_path, f"{file_name}.md")
    with open(markdown_file_path, 'w') as md_file:
        md_file.write(content)
    print(f"Markdown file saved as: {markdown_file_path}")

@app.route('/document', methods=['POST'])
def document_python_file():
    data = request.get_json()
    folder_path = data.get('folder_path')

    python_files = get_python_files(folder_path)
    if not python_files:
        return jsonify({"message": f"No Python files found in the folder: {folder_path}"}), 400 

    selected_file = random.choice(python_files)
    file_path = os.path.join(folder_path, selected_file)
    code_content = read_file(file_path)
    markdown_content = generate_markdown_output(code_content)
    markdown_file_path = save_markdown_file(folder_path, selected_file.replace('.py', ''), markdown_content) 

    return jsonify({"message": "Documentation generated successfully", "markdown_file": markdown_file_path})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')  # For local development only