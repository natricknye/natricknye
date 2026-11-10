from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "rag-orbit-v5-final.gif"
SVG = ROOT / "assets" / "rag-orbit-base-v3.svg"
OUTPUT = ROOT / "assets" / "rag-orbit-v6-final.gif"


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
globe_box = (320, 165, 570, 400)
nate_box = (338, 398, 548, 535)
globe_target = (447, 205)
nate_target = (242, 268)
frames = []

for frame_index in range(source.n_frames):
    source.seek(frame_index)
    frame = base.copy()
    source_frame = source.convert("RGB")
    globe = source_frame.crop(globe_box).resize(
        (220, 207), Image.Resampling.LANCZOS
    )
    nate = source_frame.crop(nate_box).resize(
        (165, 108), Image.Resampling.LANCZOS
    )
    for layer, target in ((nate, nate_target), (globe, globe_target)):
        mask = ImageOps.grayscale(layer).point(
            lambda value: max(0, min(255, int((value - 42) * 5)))
        )
        frame.paste(layer, target, mask)
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
