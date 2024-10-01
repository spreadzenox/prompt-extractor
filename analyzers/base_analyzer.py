from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    def __init__(self, file_path, content):
        self.file_path = file_path
        self.content = content
    
    @abstractmethod
    def analyze(self):
        pass
