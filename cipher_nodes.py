import torch

# ==========================================
# 🔑 固定密钥
# ==========================================
SECRET_KEY = 999


class ImageCipherEncode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # 这里定义显示在节点上的文字内容
        info_text = (
            "📌【前端解码指南 / Frontend Guide】\n"
            "本节点专为API工作流设计，前端需按以下算法还原：\n"
            "------------------------------------------------\n"
            "1. 固定密钥 (Key): 999\n"
            "2. 算法原理: RGB通道独立行位移 (Row Rolling)\n"
            "3. 核心公式 (y=行号, w=图像宽度):\n"
            "   R_shift = (y * 999 * 1) % w\n"
            "   G_shift = (y * 999 * 2) % w\n"
            "   B_shift = (y * 999 * 3) % w\n"
            "4. 操作: 将对应通道的每行像素向左(反向)回滚 shift 距离\n"
            "------------------------------------------------"
        )

        return {
            "required": {
                "images": ("IMAGE",),
            },
            # 添加这个可选输入，专门用于显示文字
            "optional": {
                "decryption_guide": ("STRING", {"default": info_text, "multiline": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("cipher_image",)
    FUNCTION = "encode"
    CATEGORY = "CipherTools"

    # 注意：函数签名里要加上 decryption_guide，尽管我们在代码里不使用它
    def encode(self, images, decryption_guide=""):
        batch, h, w, c = images.shape
        out_list = []
        base_shift = SECRET_KEY

        for i in range(batch):
            img = images[i]
            r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]

            r_enc = torch.zeros_like(r)
            g_enc = torch.zeros_like(g)
            b_enc = torch.zeros_like(b)

            for y in range(h):
                shift_r = (y * base_shift * 1) % w
                shift_g = (y * base_shift * 2) % w
                shift_b = (y * base_shift * 3) % w

                r_enc[y, :] = torch.roll(r[y, :], shifts=shift_r, dims=0)
                g_enc[y, :] = torch.roll(g[y, :], shifts=shift_g, dims=0)
                b_enc[y, :] = torch.roll(b[y, :], shifts=shift_b, dims=0)

            out_list.append(torch.stack((r_enc, g_enc, b_enc), dim=-1))

        return (torch.stack(out_list, dim=0),)


# 解码节点保持不变，这里省略以节省篇幅，请保留你原来的 ImageCipherDecode 类
class ImageCipherDecode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"images": ("IMAGE",), }}

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("restored_image",)
    FUNCTION = "decode"
    CATEGORY = "CipherTools"

    def decode(self, images):
        batch, h, w, c = images.shape
        out_list = []
        base_shift = SECRET_KEY

        for i in range(batch):
            img = images[i]
            r_enc, g_enc, b_enc = img[:, :, 0], img[:, :, 1], img[:, :, 2]

            r_dec = torch.zeros_like(r_enc)
            g_dec = torch.zeros_like(g_enc)
            b_dec = torch.zeros_like(b_enc)

            for y in range(h):
                shift_r = (y * base_shift * 1) % w
                shift_g = (y * base_shift * 2) % w
                shift_b = (y * base_shift * 3) % w

                r_dec[y, :] = torch.roll(r_enc[y, :], shifts=-shift_r, dims=0)
                g_dec[y, :] = torch.roll(g_enc[y, :], shifts=-shift_g, dims=0)
                b_dec[y, :] = torch.roll(b_enc[y, :], shifts=-shift_b, dims=0)

            out_list.append(torch.stack((r_dec, g_dec, b_dec), dim=-1))
        return (torch.stack(out_list, dim=0),)