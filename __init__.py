from .cipher_nodes import ImageCipherEncode, ImageCipherDecode

NODE_CLASS_MAPPINGS = {
    "ImageCipherEncode": ImageCipherEncode,
    "ImageCipherDecode": ImageCipherDecode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCipherEncode": "🔒 Cipher Encode (Color Noise)",
    "ImageCipherDecode": "🔓 Cipher Decode (Preview)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']