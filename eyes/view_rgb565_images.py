from PIL import Image
import numpy as np

def rgb565_to_rgb888(pixel):
    r = (pixel >> 11) & 0x1F
    g = (pixel >> 5)  & 0x3F
    b = pixel & 0x1F
    return (
        (r * 255) // 31,
        (g * 255) // 63,
        (b * 255) // 31,
    )

def load_rgb565(path):
    with open(path, "rb") as f:
        raw = f.read()

    # read header 2 bytes width, 2 bytes height
    width  = int.from_bytes(raw[0:2], "little")
    height = int.from_bytes(raw[2:4], "little")

    # remaining bytes are pixel data
    pixel_data = raw[4:]
    pixels = np.frombuffer(pixel_data, dtype=np.uint16)

    img = np.zeros((height, width, 3), dtype=np.uint8)

    idx = 0
    for y in range(height):
        for x in range(width):
            img[y, x] = rgb565_to_rgb888(pixels[idx])
            idx += 1

    return Image.fromarray(img, "RGB")



input_path = "eye_test_rgb565/left/normal_blink_full_left.rgb565"
output_path = "output.png"

img = load_rgb565(input_path)
img.save(output_path)

