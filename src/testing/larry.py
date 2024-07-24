import ollama as larry
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension

class LarryBackend:
    def __init__(self):
        self.full_response_html = ""
        self.chunk_buffer = ""
        self.current_response_html = ""
        self.model_name = "default_model"

    def set_model(self, model_name):
        self.model_name = model_name

    def get_models(self):
        models = larry.list()  # Acquire the list of available models
        model_names = [model['name'] for model in models['models']]  # Extract model names from the dictionary
        return model_names

    def send_message(self, user_input):
        response = larry.chat(
            model=self.model_name,
            messages=[
                {
                    'role': 'user',
                    'content': user_input,
                }],
            stream=True,
        )
        return response

    def format_chunk(self, chunk):
        self.chunk_buffer += chunk
        html_chunk = markdown.markdown(self.chunk_buffer, extensions=[TableExtension(), FencedCodeExtension()])
        larry_html_chunk = f"""
        <div style='text-align: left;'>
            <div style='display: inline-block; background-color: #2C2F33; border-radius: 10px; padding: 5px 10px; margin: 5px 10px 5px 0px; max-width: 70%; word-wrap: break-word; color: #d3d3d3; font-size: 10px;'>
                {html_chunk}
            </div>
        </div>
        """
        self.current_response_html = larry_html_chunk
        return self.current_response_html
