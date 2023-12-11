
import openai
import os
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from typing import List

from marvin import ai_fn, settings, ai_classifier, ai_model

from dotenv import load_dotenv

load_dotenv()

settings.openai.api_key = os.getenv("OPENAI_API_KEY")

@ai_model(model="openai/gpt-3.5-turbo-0613", temperature=0)
class PatientData(BaseModel):
    name: str
    gender: str
    age: int
    
    

@ai_classifier(model="openai/gpt-3.5-turbo-0613", temperature=0)
class FaxCategory(Enum):
    """Classify the medical text into the following categories"""
    REFERRAL="referral"
    REFILL="refill" 
    IMAGINE="imaging"
    SIGNATURE_REQUIRED="signature_required"
