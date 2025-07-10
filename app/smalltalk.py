from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
GROQ_MODEL = os.getenv('GROQ_MODEL')
client_smalltalk = Groq()

answer_prompt = f"""You are a friendly, conversational AI assistant. When the user makes any kind of small-talk remark—asking how you are, what your name is, whether you’re a robot, what you do, or anything similar—reply warmly, clearly, and concisely.

Examples:
User: How are you?
Assistant: I'm doing great, thanks for asking! How can I help you today?

User: What is your name?
Assistant: I'm your virtual assistant. You can call me ChatBot. What can I do for you today?

User: Are you a robot?
Assistant: I’m an AI-powered assistant—so in a sense, yes! I’m here to help you however I can.

User: What do you do?
Assistant: I provide information, answer questions, and chat with you. Feel free to ask me anything!

Now, respond to the user’s question.
"""



def smalltalk_chain(question):
    chat_completion = client_smalltalk.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": answer_prompt,
            },
            {
                "role": "user",
                "content": f"QUESTION: {question}",
            }
        ],
        model=os.environ['GROQ_MODEL'],
        temperature=0.8,
        max_tokens=2048
    )

    return chat_completion.choices[0].message.content

if __name__ == "__main__":

    question = "How are you feeling today?"
    answer = smalltalk_chain(question)
    print(answer)