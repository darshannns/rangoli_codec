"""
Rangoli Codec
A geometric steganography and visual encoding library inspired by Indian Rangoli/Kolam patterns.
"""

from .encoder import encode_to_image, text_to_binary, binary_to_segments
from .decoder import decode_from_image, binary_to_text

__version__ = "0.1.0"
__all__ = ["encode_to_image", "decode_from_image", "text_to_binary", "binary_to_segments", "binary_to_text"]