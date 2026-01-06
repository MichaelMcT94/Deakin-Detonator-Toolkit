Tool Guide Generator

This tool automatically generates a Word document guide for penetration testing tools using a Word template and AI-generated content. When you have run this tool - you will still need to proof read and fix any formatting issues, as well as provide screenshots of the tool being run.\

If a new template is to be used, simply overwrite the current template, but ensure you replace the {{placeholders}} in the new template with the same words.

The {{placeholder}} in the template.json file is {{TOOL_NAME}}
Within the template.docx they are:
- {{Overview}}
- {{Purpose}}
- {{Results}}
- {{Troubleshooting}}
- {{Credit}}

## **Contents**

- toolguide.py Main Python script that generates the tool guide.
- template.docx Word template with placeholders for each section.
- template.json JSON file with prompts for AI content generation.
- Dockerfile Containerizes the tool for easy running without local dependencies.
- requirements.txt Python dependencies for running the script locally (if not using Docker).
- README.md Instructions for setup and usage.

## **Setup**

### Using Docker - Install Docker (if not installed) - Recommended ###

##Ensure Docker Desktop is running in background

1. Build the Docker image:

docker build -t tool-guide-gen .

2. Running the Docker:

docker run -it -v /path/to/output:/app/output tool-guide-gen

EXAMPLE (WINDOWS):
docker run -it -v "C:\Users\YourName\Documents\output:/app/output" tool-guide-gen

EXAMPLE (MACOS/LINUX)
docker run -it -v ~/output:/app/output tool-guide-gen

### Running with Python ###

1. Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\\Scripts\\activate      # Windows

2. Install dependencies:

pip install -r requirements.txt

3. Set up environment variables with GROQ:
export GROQ_API_KEY="YOUR_API_KEY"   # Linux/Mac
setx GROQ_API_KEY "YOUR_API_KEY"     # Windows

## NOTE - Simply create a free account for GROQ and it will generate an API Key ##

4. Run:
python toolguide.py


###Creating Tool-Guides in the Docker###

Simply run docker run -it -v /path/to/output:/app/output tool-guide-gen
It will then ask what tool-guide you want to generate - input the desired tool-guide
It will then auto generate, you will then need to go open it in the output folder
Proof read the document, correct any formatting issues
Include screenshots of the tool-being run as well as steps


