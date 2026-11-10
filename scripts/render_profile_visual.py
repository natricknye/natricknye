from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "rag-orbit-v5-final.gif"
SVG = ROOT / "assets" / "rag-orbit-base-v3.svg"
PREVIEW = ROOT / "rag-orbit-base-preview.png"
OUTPUT = ROOT / "assets" / "rag-orbit-v6-final.gif"


if PREVIEW.exists():
    base = Image.open(PREVIEW).convert("RGB")
else:
    import cairosvg

    rendered = ROOT / "rag-orbit-base-rendered.png"
    cairosvg.svg2png(
        url=str(SVG),
        write_to=str(rendered),
        output_width=1200,
        output_height=900,
    )
    base = Image.open(rendered).convert("RGB")

base = base.resize((880, 660), Image.Resampling.LANCZOS)
source = Image.open(SOURCE)
center_box = (330, 150, 530, 520)
frames = []

for frame_index in range(source.n_frames):
    source.seek(frame_index)
    frame = base.copy()
    center = source.convert("RGB").crop(center_box)
    gray = ImageOps.grayscale(center)
    mask = gray.point(
        lambda value: max(0, min(255, int((value - 52) * 4)))
    )
    frame.paste(center, center_box[:2], mask)
    frame = ImageEnhance.Contrast(frame).enhance(1.04)
    frames.append(frame.quantize(colors=56, method=Image.Quantize.MEDIANCUT))

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=source.info.get("duration", 210),
    loop=source.info.get("loop", 0),
    optimize=True,
    disposal=2,
)
