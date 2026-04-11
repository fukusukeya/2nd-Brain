from PIL import Image

def process_logo(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # 白に近いピクセル（JPGのノイズ含め230以上）を透過
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            newData.append((255, 255, 255, 0))
        else:
            # それ以外は真っ白にする
            newData.append((255, 255, 255, 255))

    img.putdata(newData)
    img.save(output_path, "PNG")

if __name__ == "__main__":
    process_logo("header_logo.jpg", "logo_white_fixed.png")
