"""
RetailSense AI - Multimodal E-commerce Intelligence Engine
"""

__version__ = "0.1.0"
__author__ = "RetailSense AI Team"
__description__ = "Multimodal E-commerce Intelligence Engine using BigQuery AI"

from .core import RetailSenseAI
from .demo import RetailSenseAIDemo
from .main import main

__all__ = ["RetailSenseAI", "RetailSenseAIDemo", "main"]