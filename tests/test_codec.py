import os
import pytest
from rangoli_codec import encode_to_image, decode_from_image, text_to_binary, binary_to_text

def test_roundtrip(tmp_path):
    message = "HI"
    img_path = str(tmp_path / "test_rangoli.png")
    
    # 1. Encode
    encode_to_image(message, img_path)
    assert os.path.exists(img_path)
    
    # 2. Decode
    decoded = decode_from_image(img_path)
    assert decoded == message