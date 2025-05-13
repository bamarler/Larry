# Larry

## Description
Larry is an AI assistant that runs opensource Large Language Models locally on consumer grade hardware through Ollama. It is designed to be an assistant for any task you might have such as coding, research, writing, etc. The window stays on top of all of your applications so you can easily reference and chat with your model.

![image](https://github.com/user-attachments/assets/eff21959-4226-481c-89ee-1ac658a060f7)

## How to Use
Clone the repository, then run the following script: ```src/backend/main.py```

## Features
* You can install any available model from [Ollama](https://ollama.com/search) depending on your available memory and computer specs. You can also remove any old models that you don't use anymore to make space.
  
![image](https://github.com/user-attachments/assets/5d2e7093-df3a-4e05-b48f-954bfe7629ea)

* All chats are stored in sqlite3 database and the model is fed all previous context from the current chat each time.
  
* If the model you are using supports markdown features, they will be rendered appropriately in an HTML window
  
* You can choose to pin the window on the left or right side depending on your preference
  
* You can create multiple personas with custom names, roles, personalities, and behaviors to be masked over any model
  
![image](https://github.com/user-attachments/assets/ba43841c-108c-42ef-b5c2-b932550ac002)

* For those who want to modify specific model details, you have the option to change the models the temperature, penalties, and other attributes.

![image](https://github.com/user-attachments/assets/07c7a0ae-11a6-475f-8ef4-ebf7150908ca)

## Tech Stack
The majority of the Program is coded in **Python**, and frontend is designed using the **TKinter** library. Models and model requests are handled via **Ollama's** python api library. Chats are stored in a **sqlite3** database.
