# 导入你写的节点类
from .cipher_nodes import ImageCipherEncode, ImageCipherDecode

# 建立 ComfyUI 内部识别名与 Python 类的映射
NODE_CLASS_MAPPINGS = {
    "ImageCipherEncode": ImageCipherEncode,
    "ImageCipherDecode": ImageCipherDecode
}

# 建立节点在 UI 界面显示的中文/英文名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageCipherEncode": "🔒 RGB 行交织加密",
    "ImageCipherDecode": "🔓 RGB 行交织解密"
}

# 必须导出这两个变量
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']