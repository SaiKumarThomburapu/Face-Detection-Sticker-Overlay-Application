from dataclasses import dataclass

@dataclass
class Artifact:
    def __init__(self, output_path, metadata=None):
        self.output_path = output_path
        self.metadata = metadata or {}


