"""
生成 WeekFlow Android APK 图标集：传统 launcher icon + Adaptive Icon
源图: ChatGPT Image 2026年8月12日 14_08_56.png
"""
import os
from PIL import Image, ImageDraw

SRC = r"C:\Users\Administrator\Desktop\提示词\ChatGPT Image 2026年8月12日 14_08_56.png"
RES_DIR = r"D:\workbuddy\运动学习app\android\app\src\main\res"

# 密度 -> px (launcher icon)
DENSITIES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

# Adaptive icon 前景尺寸 (108dp * density scale)
ADAPTIVE_DENSITIES = {
    "mipmap-mdpi": 108,
    "mipmap-hdpi": 162,
    "mipmap-xhdpi": 216,
    "mipmap-xxhdpi": 324,
    "mipmap-xxxhdpi": 432,
}

# WeekFlow 品牌浅米色（与图标原图背景、网页背景协调）
ADAPTIVE_BG_COLOR = "#F5F2EC"

img = Image.open(SRC).convert("RGBA")
print(f"源图尺寸: {img.size}")


def make_rounded_square(image, size, radius_ratio=0.22):
    """生成带圆角的正方形图标"""
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    # 居中缩放，覆盖整个正方形（crop to cover）
    iw, ih = image.size
    scale = max(size / iw, size / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    resized = image.resize((nw, nh), Image.LANCZOS)
    left = (nw - size) // 2
    top = (nh - size) // 2
    cropped = resized.crop((left, top, left + size, top + size))
    out.paste(cropped, (0, 0))
    # 圆角蒙版
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    r = int(size * radius_ratio)
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=255)
    out.putalpha(mask)
    return out


def make_adaptive_foreground(image, size):
    """
    生成 adaptive icon 前景图。
    Canvas = size x size (108dp at this density).
    安全区 = 中心 66dp (即 canvas 的 66/108 = 61%)。
    把图标内容放在安全区内。
    """
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    safe_size = int(size * 66 / 108)
    iw, ih = image.size
    scale = max(safe_size / iw, safe_size / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    resized = image.resize((nw, nh), Image.LANCZOS)
    paste_x = (size - nw) // 2
    paste_y = (size - nh) // 2
    canvas.paste(resized, (paste_x, paste_y), resized if resized.mode == "RGBA" else None)
    return canvas


# ---- 1. 传统 launcher icon (ic_launcher.png / ic_launcher_round.png) ----
for folder, px in DENSITIES.items():
    dpath = os.path.join(RES_DIR, folder)
    os.makedirs(dpath, exist_ok=True)
    icon = make_rounded_square(img, px)
    icon.save(os.path.join(dpath, "ic_launcher.png"))
    icon.save(os.path.join(dpath, "ic_launcher_round.png"))
    print(f"  {folder}/ic_launcher.png ({px}x{px})")
    print(f"  {folder}/ic_launcher_round.png ({px}x{px})")

# ---- 2. Adaptive Icon 前景 (ic_launcher_foreground.png) ----
for folder, px in ADAPTIVE_DENSITIES.items():
    dpath = os.path.join(RES_DIR, folder)
    os.makedirs(dpath, exist_ok=True)
    fg = make_adaptive_foreground(img, px)
    fg.save(os.path.join(dpath, "ic_launcher_foreground.png"))
    print(f"  {folder}/ic_launcher_foreground.png ({px}x{px})")

# ---- 3. Adaptive Icon 资源描述 ----
mipmap_any = os.path.join(RES_DIR, "mipmap-anydpi-v26")
os.makedirs(mipmap_any, exist_ok=True)

xml_adaptive = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
'''
with open(os.path.join(mipmap_any, "ic_launcher.xml"), "w") as f:
    f.write(xml_adaptive)
with open(os.path.join(mipmap_any, "ic_launcher_round.xml"), "w") as f:
    f.write(xml_adaptive)
print(f"  mipmap-anydpi-v26/ic_launcher.xml (adaptive icon)")
print(f"  mipmap-anydpi-v26/ic_launcher_round.xml")

# ---- 4. 背景色定义 ----
values_dir = os.path.join(RES_DIR, "values")
os.makedirs(values_dir, exist_ok=True)
colors_path = os.path.join(values_dir, "colors.xml")
if os.path.exists(colors_path):
    with open(colors_path, "r", encoding="utf-8") as f:
        existing = f.read()
else:
    existing = "<resources></resources>"

if "ic_launcher_background" not in existing:
    existing = existing.replace(
        "</resources>",
        f'    <color name="ic_launcher_background">{ADAPTIVE_BG_COLOR}</color>\n</resources>',
    )
    with open(colors_path, "w", encoding="utf-8") as f:
        f.write(existing)
    print(f"  values/colors.xml (ic_launcher_background = {ADAPTIVE_BG_COLOR})")
else:
    print(f"  values/colors.xml (already has background color)")

print("\n=== WeekFlow 图标生成完成 ===")
