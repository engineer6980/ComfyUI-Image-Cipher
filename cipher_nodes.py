import torch

# ==========================================
# 🔑 固定密钥：前端和PyCharm必须使用同一个数字
# ==========================================
SECRET_KEY = 999


class ImageCipherEncode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # 输入标准 VAE 解码后的图像
                "images": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("cipher_color_noise",)
    FUNCTION = "encode"
    CATEGORY = "CipherTools"

    def encode(self, images):
        # images shape: [Batch, Height, Width, Channel=3]
        batch, h, w, c = images.shape
        out_list = []

        # 使用固定密钥作为基础偏移量
        base_shift = SECRET_KEY

        for i in range(batch):
            img = images[i]  # [H, W, 3]

            # 1. 拆分三个通道，它们现在的形状都是 [H, W]
            r_plane = img[:, :, 0]
            g_plane = img[:, :, 1]
            b_plane = img[:, :, 2]

            # 准备加密容器
            r_encrypted = torch.zeros_like(r_plane)
            g_encrypted = torch.zeros_like(g_plane)
            b_encrypted = torch.zeros_like(b_plane)

            # 2. 核心加密循环：对每一行进行不同程度的位移
            for y in range(h):
                # 关键点：R, G, B 使用不同的倍率 (1, 2, 3)，确保它们错开
                # 计算 R 通道当前行的位移量
                shift_r = (y * base_shift * 1) % w
                r_encrypted[y, :] = torch.roll(r_plane[y, :], shifts=shift_r, dims=0)

                # 计算 G 通道当前行的位移量 (倍率不同)
                shift_g = (y * base_shift * 2) % w
                g_encrypted[y, :] = torch.roll(g_plane[y, :], shifts=shift_g, dims=0)

                # 计算 B 通道当前行的位移量 (倍率不同)
                shift_b = (y * base_shift * 3) % w
                b_encrypted[y, :] = torch.roll(b_plane[y, :], shifts=shift_b, dims=0)

            # 3. 重新组合成彩色图像 [H, W, 3]
            # 此时 R,G,B 已经完全错位，图像看起来是彩色噪点
            encrypted_img = torch.stack((r_encrypted, g_encrypted, b_encrypted), dim=-1)
            out_list.append(encrypted_img)

        return (torch.stack(out_list, dim=0),)


# 解密节点（仅供 ComfyUI 内部测试用，实际业务在前端完成）
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
            # 1. 拆分加密后的通道
            r_enc = img[:, :, 0]
            g_enc = img[:, :, 1]
            b_enc = img[:, :, 2]

            r_dec = torch.zeros_like(r_enc)
            g_dec = torch.zeros_like(g_enc)
            b_dec = torch.zeros_like(b_enc)

            # 2. 反向操作：向相反方向回滚
            for y in range(h):
                # 计算加密时用的位移量
                shift_r = (y * base_shift * 1) % w
                shift_g = (y * base_shift * 2) % w
                shift_b = (y * base_shift * 3) % w

                # 使用负数 shifts 进行反向滚动
                r_dec[y, :] = torch.roll(r_enc[y, :], shifts=-shift_r, dims=0)
                g_dec[y, :] = torch.roll(g_enc[y, :], shifts=-shift_g, dims=0)
                b_dec[y, :] = torch.roll(b_enc[y, :], shifts=-shift_b, dims=0)

            restored_img = torch.stack((r_dec, g_dec, b_dec), dim=-1)
            out_list.append(restored_img)

        return (torch.stack(out_list, dim=0),)