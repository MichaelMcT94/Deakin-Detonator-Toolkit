import json
import os
import sys
from docxtpl import DocxTemplate
from groq import Groq

# -------------------------
# ASCII Banner
# -------------------------
ASCII_BANNER = r"""
 _____           _   _____       _     _        _____                           _             
|_   _|         | | |  __ \     (_)   | |      |  __ \                         | |            
  | | ___   ___ | | | |  \/_   _ _  __| | ___  | |  \/ ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
  | |/ _ \ / _ \| | | | __| | | | |/ _` |/ _ \ | | __ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
  | | (_) | (_) | | | |_\ \ |_| | | (_| |  __/ | |_\ \  __/ | | |  __/ | | (_| | || (_) | |   
  \_/\___/ \___/|_|  \____/\__,_|_|\__,_|\___|  \____/\___|_| |_|\___|_|  \__,_|\__\___/|_|   

Tool automation created by
- Michael McTackett - 223159999
"""
print(ASCII_BANNER)

# -------------------------
# Configuration constants
# -------------------------
TEMPLATE_FILE = "template.docx"
OUTPUT_DIR = "/app/output"

# -------------------------
# Helper: Get Groq client (env → prompt → fail cleanly)
# -------------------------
def get_groq_client():
    groqApiKey = os.environ.get("GROQ_API_KEY")

    if not groqApiKey:
        # Non-interactive environment (GitHub Actions, CI, docker w/o -it)
        if not sys.stdin.isatty():
            raise RuntimeError(
                "GROQ_API_KEY not set and no interactive terminal available.\n"
                "Set the environment variable or run Docker with -it."
            )

        print("GROQ_API_KEY not found in environment.")
        groqApiKey = input("Enter your Groq API key: ").strip()

    if not groqApiKey:
        raise ValueError("Groq API key is required to run this tool.")

    return Groq(api_key=groqApiKey)

# Initialise client
client = get_groq_client()

# -------------------------
# Generate AI function with retry
# -------------------------
def generateAi(text):
    global client
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": text}],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        print("\nGroq API error:")
        print(str(e))

        if not sys.stdin.isatty():
            raise RuntimeError(
                "Groq API call failed in non-interactive mode. "
                "Check your GROQ_API_KEY."
            )

        retry = input(
            "\nAPI key may be invalid or expired. Enter a new key? (y/n): "
        ).strip().lower()

        if retry != "y":
            raise

        new_key = input("Enter your new Groq API key: ").strip()
        if not new_key:
            raise ValueError("No API key entered.")

        os.environ["GROQ_API_KEY"] = new_key
        client = Groq(api_key=new_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": text}],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content

# -------------------------
# Load template prompts
# -------------------------
with open("template.json", "r") as templateFile:
    templatePrompts = json.load(templateFile)

# -------------------------
# Main execution loop
# -------------------------
print("Type 'exit' or 'quit' to stop the tool. Ctrl+C also works.\n")

while True:
    try:
        toolName = input("\nEnter the tool name (or type 'exit'/'quit'): ").strip()
        toolName = "".join(c for c in toolName if c.isprintable())

        if not toolName or toolName.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        disclaimerText = (
            f"Only use {toolName} on systems you own or have explicit written permission to test. "
            "Scanning without consent may be illegal depending on your region."
        )

        context = {
            "TOOL_NAME": toolName,
            "DISCLAIMER": disclaimerText
        }

        print(f"\nGenerating AI text for '{toolName}'...\n")
        for section, prompt in templatePrompts.items():
            print(f" - Generating {section}...")
            context[section] = generateAi(
                prompt.replace("{{TOOL_NAME}}", toolName)
            )

        document = DocxTemplate(TEMPLATE_FILE)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        base = f"{toolName.replace(' ', '_')}_Tool_Guide"
        version = 1
        outputFile = os.path.join(OUTPUT_DIR, f"{base}_v{version}.docx")

        while os.path.exists(outputFile):
            version += 1
            outputFile = os.path.join(OUTPUT_DIR, f"{base}_v{version}.docx")

        context["Version"] = f"v{version}"
        document.render(context)
        document.save(outputFile)

        print(f"\nSaved to: {outputFile}")
        print("\n----------------------------------------------")

    except KeyboardInterrupt:
        print("\nExiting...")
        break
