class ConfigLoader:

    def __init__(self):
        pass
    
class ModelLoader(BaseModel):

    model_provider: Literal["groq", "openai"] = "groq"

    config: Optional[ConfigLoader] = Field(default = None, exclude = True)