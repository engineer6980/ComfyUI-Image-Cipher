import cv2
import numpy as np

# ==========================================
# 🔑 必须与 ComfyUI 里的密钥完全一致
# ==========================================
SECRET_KEY = 999


def restore_image_from_cipher(cipher_image_path):
    # 1. 读取加密图片
    # 注意：OpenCV 读取的顺序是 BGR
    cipher_bgr = cv2.imread(cipher_image_path)
    if cipher_bgr is None:
        print(f"❌ 找不到图片: {cipher_image_path}")
        return

    h, w, c = cipher_bgr.shape
    print(f"Attempting restore. Size: {w}x{h}, Key: {SECRET_KEY}")

    # 2. 拆分 BGR 通道
    b_enc, g_enc, r_enc = cv2.split(cipher_bgr)

    # 准备还原容器
    # 必须使用 .copy() 确保内存独立，否则修改可能会互相影响
    r_dec = r_enc.copy()
    g_dec = g_enc.copy()
    b_dec = b_enc.copy()

    base_shift = SECRET_KEY

    # 3. 核心还原循环：反向位移
    print("Restoring RGB channels independently...")
    for y in range(h):
        # 计算原本的位移量 (和 ComfyUI 逻辑一致)
        # R用倍率1, G用倍率2, B用倍率3
        shift_r = (y * base_shift * 1) % w
        shift_g = (y * base_shift * 2) % w
        shift_b = (y * base_shift * 3) % w

        # 执行反向滚动 (np.roll 如果 shift 为负数就是反向)
        r_dec[y, :] = np.roll(r_enc[y, :], -shift_r)
        g_dec[y, :] = np.roll(g_enc[y, :], -shift_g)
        b_dec[y, :] = np.roll(b_enc[y, :], -shift_b)

    # 4. 合并回 BGR 图片以便显示
    restored_bgr = cv2.merge([b_dec, g_dec, r_dec])

    # 5. 显示结果对比
    # 缩放以便屏幕能放下
    scale = 0.5
    disp_h, disp_w = int(h * scale), int(w * scale)

    cv2.imshow("1. Encrypted Input (Color Noise)", cv2.resize(cipher_bgr, (disp_w, disp_h)))
    cv2.imshow("2. Restored Result (Normal)", cv2.resize(restored_bgr, (disp_w, disp_h)))

    print("✅ 还原完成！请查看弹出的窗口。")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# --- 运行测试 ---
# 把你从 ComfyUI 保存下来的那张彩色噪点图路径填在这里
cipher_file = "ComfyUI_0001.png"
restore_image_from_cipher(cipher_file)