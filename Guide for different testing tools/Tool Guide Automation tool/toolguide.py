import json
import os
import time

from docxtpl import DocxTemplate
from groq import Groq

# -------------------------
# Configuration constants.
# -------------------------

TEMPLATE_FILE = "template.docx"
OUTPUT_DIR = "/app/output"

# Retrieve the Groq API key from environment variables.
groqApiKey = os.getenv("GROQ_API_KEY")

if not groqApiKey:
  raise RuntimeError(
    "GROQ_API_KEY environment variable is not set."
  )

# Groq client used to generate AI content.
client = Groq(api_key=groqApiKey)

def generateAi(text):
  """
  Generate AI-generated content using the Groq chat completion API.

  @param text: The prompt text sent to the AI model.
  @return: The generated text response from the AI model.
  """
  response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": text}],
    max_tokens=200,
    temperature=0.7
  )

  return response.choices[0].message.content


# -------------------------
# Load template prompts.
# -------------------------

with open("template.json", "r") as templateFile:
  templatePrompts = json.load(templateFile)

# -------------------------
# Main execution loop.
# -------------------------

while True:
  toolName = input(
    "\nEnter the tool name (or type 'exit' to quit): "
  ).strip()

  if toolName.lower() == "exit":
    print("Goodbye!")
    break

  # -------------------------
  # Generate AI content.
  # -------------------------

  context = {
    "TOOL_NAME": toolName
  }

  print(f"\nGenerating AI text for '{toolName}'...\n")

  for section, prompt in templatePrompts.items():
    finalPrompt = prompt.replace("{{TOOL_NAME}}", toolName)
    print(f" - Generating {section}...")
    context[section] = generateAi(finalPrompt)

  # -------------------------
  # Render Word template.
  # -------------------------

  document = DocxTemplate(TEMPLATE_FILE)
  document.render(context)

  # -------------------------
  # Save output file.
  # -------------------------

  os.makedirs(OUTPUT_DIR, exist_ok=True)

  outputFile = os.path.join(
    OUTPUT_DIR,
    f"{toolName.replace(' ', '_')}_Tool_Guide.docx"
  )

  document.save(outputFile)

  print(f"\nAll done! Tool guide saved to: {outputFile}")
  print("\n----------------------------------------------")
  print("Ready for another tool!\n")
