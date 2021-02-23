class PromptIndexError(Exception):
    """Raised when prompt index is incorrect"""
    
    def __init__(self, index, max_index):
        self.index = index
        self.valid_i = list(range(max_index))
        self.message = f"The index is not within the accepted range ({', '.join(self.valid_i)})"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.index} -> {self.message}'