import ollama

class ModelManager:
    def __init__(self):
        self.current_model = None

        try:
            self.current_model = self.list_models()[0]
        except IndexError:
            self.current_model = "No Models Installed"

    def change_model(self, model_name):
        self.current_model = model_name

    def list_models(self):
        try:
            models = ollama.list()
            model_names = [model['name'] for model in models['models']]
            return [model for model in model_names if model != self.current_model]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def install_model(self, model_name):
        return ollama.pull(model_name, stream=True)
    
    def remove_model(self, model_name):
        return ollama.delete(model_name)

