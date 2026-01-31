import torch

# ==========================================
# 🔑 全局密钥：必须保持一致
# ==========================================
SECRET_KEY = 999


class ImageCipherEncode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("cipher_image",)
    FUNCTION = "encode"
    CATEGORY = "CipherTools"

    def encode(self, images):
        batch, h, w, c = images.shape
        out_list = []
        base_shift = SECRET_KEY

        for i in range(batch):
            img = images[i]

            # 分离通道
            r = img[:, :, 0]
            g = img[:, :, 1]
            b = img[:, :, 2]

            # 准备容器
            r_enc = torch.zeros_like(r)
            g_enc = torch.zeros_like(g)
            b_enc = torch.zeros_like(b)

            # 加密循环：正向位移 (shifts=正数)
            for y in range(h):
                shift_r = (y * base_shift * 1) % w
                shift_g = (y * base_shift * 2) % w
                shift_b = (y * base_shift * 3) % w

                r_enc[y, :] = torch.roll(r[y, :], shifts=shift_r, dims=0)
                g_enc[y, :] = torch.roll(g[y, :], shifts=shift_g, dims=0)
                b_enc[y, :] = torch.roll(b[y, :], shifts=shift_b, dims=0)

            out_list.append(torch.stack((r_enc, g_enc, b_enc), dim=-1))

        return (torch.stack(out_list, dim=0),)


class ImageCipherDecode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            }
        }

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

            r_enc = img[:, :, 0]
            g_enc = img[:, :, 1]
            b_enc = img[:, :, 2]

            r_dec = torch.zeros_like(r_enc)
            g_dec = torch.zeros_like(g_enc)
            b_dec = torch.zeros_like(b_enc)

            # 解密循环：反向位移 (shifts=负数)
            for y in range(h):
                shift_r = (y * base_shift * 1) % w
                shift_g = (y * base_shift * 2) % w
                shift_b = (y * base_shift * 3) % w

                # 注意这里的负号 -shift
                r_dec[y, :] = torch.roll(r_enc[y, :], shifts=-shift_r, dims=0)
                g_dec[y, :] = torch.roll(g_enc[y, :], shifts=-shift_g, dims=0)
                b_dec[y, :] = torch.roll(b_enc[y, :], shifts=-shift_b, dims=0)

            out_list.append(torch.stack((r_dec, g_dec, b_dec), dim=-1))

        return (torch.stack(out_list, dim=0),)