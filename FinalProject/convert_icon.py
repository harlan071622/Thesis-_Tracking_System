from PIL import Image
import os

# Paths (adjust if needed)
base    = os.path.dirname(os.path.abspath(__file__))
png_src = os.path.join(base, "assets", "my_logo.png")
ico_out = os.path.join(base, "assets", "my_logo.ico")
png16   = os.path.join(base, "assets", "my_logo16.png")

# Load your source PNG (should be square)
img = Image.open(png_src)

# === Option A: produce a single-size 16×16 ICO ===
# Use LANCZOS resampling instead of ANTIALIAS
img16 = img.resize((16, 16), resample=Image.LANCZOS)
img16.save(ico_out, sizes=[(16, 16)])
print(f"Wrote single-size 16×16 ICO: {ico_out}")

# === Option B: produce a standalone 16×16 PNG (for iconphoto fallback) ===
img16.save(png16, format="PNG")
print(f"Wrote 16×16 PNG: {png16}")