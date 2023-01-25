from pydantic import BaseModel
from typing import Optional, List

class Engine(BaseModel):
    name: str
    author: str
    description: str

class Engines(BaseModel):
    engines: List[Engine]

class Completion(BaseModel):
    prompt: str
    engine: Optional[str] = None
    max_new_tokens: Optional[int] = 10
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    typical_p: Optional[float] = None
    repetition_penalty: Optional[float] = None
    do_sample: Optional[bool] = None
    penalty_alpha: Optional[float] = None
    num_return_sequences: Optional[int] = 1
    stop_sequence: Optional[str] = None
    bad_words: Optional[list] = None
