import ollama

ollama.serve()

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "Hello, how are you today?"
        },
        {
            "role": "assistant",
            "content": "Hello! I'm doing well, thank you for asking. How about you?"
        },
        {
            "role": "user",
            "content": "I'm doing great, thank you! Why is the sky blue?"
        },
        {
            "role": "assistant",
            "content": "The sky is blue because it reflects the sunlight that reaches us. It's a beautiful natural phenomenon."
        },
        {
            "role": "user",
            "content": "That's interesting. List the previous prompts I have submitted to you."
        },
    ],
    stream=True,
)

for chunk in response:
    print(chunk['message']['content'])