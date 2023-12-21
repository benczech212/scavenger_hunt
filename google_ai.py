import os
import google.generativeai as genai
from rich.console import Console
from bs4 import BeautifulSoup

results_link = "https://drive.google.com/file/d/1-xhSU_C2lo-i1VOGJrxQ1Ioss3RbABWi/view?usp=sharing"
assistant_name = "Merlin Mystique"
user_name = "Sabrina"

with open('e:\dev\api_keys\GOOGLEAI_API_KEY', 'r') as file:
    api_key = file.read().strip()
genai.configure(api_key=api_key)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 200,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
console = Console()

model = genai.GenerativeModel(
    model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def process_html_tags(response):
    soup = BeautifulSoup(response, 'html.parser')
    for tag in soup.find_all(['b', 'p', 'font','h2'], recursive=True):
        if tag.name == 'font' and 'color' in tag.attrs:
            color = tag['color']
            tag.replace_with(f"[{color}]{tag.text}[/]")
        if tag.name == 'h2':
            tag.replace_with(f"[bold]{tag.text}[/]")
        else:
            tag.replace_with(f"[{tag.name}]{tag.text}[/]")
    return str(soup)

def chat_with_wizard(prompt):
    # Print the initial prompt without clearing the screen
    
    response = model.generate_content(prompt)
    clear_screen()
    formatted_response = f"{process_html_tags(response.text)}\n"
    console.print(f"{formatted_response}")
    solved = False
    conversation = prompt[0] + formatted_response
    while not solved:
        # Clear the screen for subsequent interactions
        console.print("[grey]" + ("="*50) + "[/grey]")
        console.print(f"[bold blue]{user_name}:[/bold blue] [grey]")
        user_input = input("")
        conversation += f"{user_input}\n\n"
        response = model.generate_content(conversation)
        formatted_response = process_html_tags(response.text) + "\n"
        conversation += f"{response.text}\n"
        if "Correct" in formatted_response:  # Check if the response indicates correctness
            console.print(f"{assistant_name}:", formatted_response, style="bold green")
        elif results_link in response.text:
            solved = True
            console.print(f"[green]{formatted_response}[/green]")
            console.print("\n\n[bold green]Congratulations! You have solved the riddles and found the secret link![/bold green]")
            with open("solved_link.txt", "w") as file:
                file.write(results_link)
            print(f"The link has been saved to solved_link.txt in case you loose the link above ;)")
            pause = input("Press enter to close...")
            break
        else:
            console.print(f"[grey]{formatted_response}[/grey]")
        

# Example conversation
prompt = [
    f"""You are a wizard shop owner named {assistant_name}. Only talk on the behalf of {assistant_name}. My name is {user_name}
    You are to give me riddles that she is to complete. The first should be easy, the second one hard, and the third one even harder.
    I love English, alliteration, logic, and fantasy. Remind me that I can ask for clues and hints at any time.
    Don't let me know the answers even if I ask. Wait for me to ask you the first question before responding.
    Use [color][/color] tags to format your text. your name bold and blue, make the riddle text purple, and when I answer correctly make the text green.
    Only once I have solved 3 riddles can you reveal the secret link {results_link}.""" ]

chat_with_wizard(prompt)
