import openai
import json

client = openai.OpenAI(api_key="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")

with open("faq_data.json", "r") as f:
    faq_data = json.load(f)

DEFAULT_RESPONSE = "Sorry, I cannot answer that at the moment. Please contact the student organizer for more information."

print("Hi, I am the AI Chatbot for UNC's CUSA.")

def get_semantic_similarity(user_input, question):
    """
    Use ChatGPT to determine if the user's input is semantically similar to a question in the FAQ.
    """
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that determines if two questions are semantically similar. Respond with 'yes' or 'no'."},
        {"role": "user", "content": f"Is '{user_input}' similar to '{question}'? Answer only with 'yes' or 'no'."}
    ],
    max_tokens=5,
    temperature=0)
    return response.choices[0].message.content.strip().lower() == "yes"

def get_faq_response(user_input):
    """
    Check if the user's input is semantically similar to any question in the FAQ.
    If so, return the corresponding answer.
    """
    for question, answer in faq_data.items():
        if get_semantic_similarity(user_input, question):
            return answer
    return None  # No match found

def chat_with_gpt(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot for UNC's CUSA."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content 

    return DEFAULT_RESPONSE

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        print("Bot:", chat_with_gpt(user_input))
