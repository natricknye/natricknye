from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "rag-orbit-v5-final.gif"
OUTPUT = ROOT / "assets" / "rag-orbit-v6-final.gif"
FONT_BOLD = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    29,
)
FONT_TITLE = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    36,
)


def header_background(width: int, height: int) -> Image.Image:
    layer = Image.new("RGB", (width, height))
    pixels = layer.load()
    left = (2, 9, 17)
    right = (8, 27, 46)
    for y in range(height):
        for x in range(width):
            mix = x / max(1, width - 1)
            pixels[x, y] = tuple(
                round(start + (end - start) * mix)
                for start, end in zip(left, right)
            )
    return layer


source = Image.open(SOURCE)
frames = []
for frame_index in range(source.n_frames):
    source.seek(frame_index)
    frame = source.convert("RGB")
    frame.paste(header_background(880, 80), (0, 0))
    draw = ImageDraw.Draw(frame)
    draw.text((35, 14), "AGENTIC ENGINEERING", font=FONT_BOLD, fill=(143, 182, 210))
    draw.text((35, 43), "Inspectable R-A-G", font=FONT_TITLE, fill=(245, 249, 253))
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

readme = ROOT / "README.md"
text = readme.read_text()
text = text.replace("assets/rag-orbit-v5-final.gif", "assets/rag-orbit-v6-final.gif")
text = text.replace(
    "Currently exploring **Campus Agents**, **Retrival Augmented Generation**, "
    "**Interaction Design** and **Recursive Self-Improving** for AI systems.",
    "Currently exploring **campus agents**, **retrieval-augmented generation**, "
    "**interaction design**, and **recursive self-improvement** for AI systems.",
)
readme.write_text(text)
