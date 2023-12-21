from gtts import gTTS
import os
from openai import OpenAI

with open('/etc/OPENAI_API_KEY', 'r') as file:
    api_key = file.read().strip()

result_link = "https://drive.google.com/file/d/1-xhSU_C2lo-i1VOGJrxQ1Ioss3RbABWi/view?usp=sharing"

client = OpenAI(api_key=api_key)

# Create the assistant
my_assistant = client.beta.assistants.create(
    instructions=f"You are a wizard shop owner. I will be connecting you with Sabrina, my beautiful girlfriend. You are to give her riddles that she is to complete. The first should be easy, the second one hard, and the third one even harder. She loves English, alliteration, logic and fantasy.   Let her know she can ask for clues and hints. Don't let her know the answers even if she asks. When she gets all three correct, reveal the secret link {result_link}. Wait for her to ask you the first question before responding.",
    name="Merlin Mystique",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4",
)

# Create a thread
thread = client.beta.threads.create()

# Start the conversation
def prompt_user(user_message):
    return client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )

def assistant_response(assistant_message):
    # Convert text to speech
    tts = gTTS(text=assistant_message, lang='en')
    tts.save('assistant_response.mp3')

    # Play the audio file
    os.system("mpg321 assistant_response.mp3")

    # Return the assistant message
    return assistant_message

# User prompt
user_message = "I need to solve the equation `3x + 11 = 14`. Can you help me?"
prompt_user(user_message)

# Get assistant's response
assistant_message = assistant_response("This is a test")  # Fix the role parameter here

# Print the conversation
print(f"Assistant: {assistant_message}")
