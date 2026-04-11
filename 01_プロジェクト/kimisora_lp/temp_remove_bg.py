from PIL import Image
import sys

def remove_white(input_path, output_path, threshold=240):
    img = Image.open(input_path).convert("RGBA")
    new_data = [(255,255,255,0) if d[0]>threshold and d[1]>threshold and d[2]>threshold else d for d in img.getdata()]
    img.putdata(new_data)
    img.save(output_path, "PNG")

remove_white("/Users/kasuyatooru/.gemini/antigravity/brain/5113c2ea-079c-4f0c-bb1e-34ca35420b17/deco_learning_mom_1775822566661.png", "deco_mom.png")
remove_white("/Users/kasuyatooru/.gemini/antigravity/brain/5113c2ea-079c-4f0c-bb1e-34ca35420b17/deco_climbing_child_1775822580748.png", "deco_steps.png")
