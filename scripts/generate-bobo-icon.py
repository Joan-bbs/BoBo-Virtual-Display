"""Generate a minimal dual-display Bobo icon before Tauri packaging."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
S = 1024
im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.rounded_rectangle((42, 42, 982, 982), radius=215, fill="#0C1C50")
for i in range(55):
    d.rounded_rectangle((60+i, 60+i, 964-i, 964-i), radius=max(30, 200-i), outline=(24, 103, 232, max(15, 115-i*2)), width=2)
d.rounded_rectangle((374, 242, 856, 645), radius=49, fill="#153E9E", outline="#4DCBFF", width=19)
d.rounded_rectangle((404, 274, 825, 613), radius=29, fill="#1C70DD")
d.rounded_rectangle((167, 360, 736, 766), radius=58, fill="#082B83", outline="#8DEBFF", width=25)
d.rounded_rectangle((202, 395, 701, 716), radius=32, fill="#1689EE")
d.polygon([(205, 702), (560, 395), (700, 395), (348, 716)], fill="#38C4F7")
d.rounded_rectangle((420, 764, 492, 832), radius=13, fill="#7CEBFF")
d.rounded_rectangle((325, 824, 584, 866), radius=20, fill="#7CEBFF")
d.rounded_rectangle((432, 734, 474, 747), radius=6, fill="#061D5C")
icon_dir = ROOT / "src-tauri" / "icons"
icon_dir.mkdir(parents=True, exist_ok=True)
for size, filename in [(32, "32x32.png"), (64, "64x64.png"), (128, "128x128.png"), (256, "128x128@2x.png")]:
    im.resize((size,size), Image.Resampling.LANCZOS).save(icon_dir / filename)
im.save(ROOT / "resources" / "icon.png")
im.save(icon_dir / "icon.png")
im.save(icon_dir / "icon.ico", sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
# Windows tile icon variants
for size in [30, 44, 71, 89, 107, 142, 150, 284, 310]:
    filename = f"Square{size}x{size}Logo.png"
    if (icon_dir / filename).exists():
        im.resize((size, size), Image.Resampling.LANCZOS).save(icon_dir / filename)
if (icon_dir / "StoreLogo.png").exists():
    im.resize((50, 50), Image.Resampling.LANCZOS).save(icon_dir / "StoreLogo.png")

# NSIS wizard images are separate from the executable icon.
win = ROOT / "src-tauri" / "windows"
win.mkdir(parents=True, exist_ok=True)
for filename, width, height, icon_size in [
    ("header.bmp", 150, 57, 48),
    ("sidebar.bmp", 164, 314, 136),
]:
    bg = Image.new("RGB", (width, height), "#0C1C50")
    logo = im.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    bg.paste(logo, ((width-icon_size)//2, (height-icon_size)//2), logo)
    bg.save(win / filename, format="BMP")

print("Generated Bobo icon assets")
