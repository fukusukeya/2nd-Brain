from PIL import Image

def process_logo(input_path, output_path, threshold=200):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        gray = int(item[0] * 0.299 + item[1] * 0.587 + item[2] * 0.114)
        if gray > threshold:
            # 明るいピクセル（背景やノイズ）は完全に透明にする
            newData.append((255, 255, 255, 0))
        else:
            # それ以外（文字、アイコン）は完全に白く不透明にする
            newData.append((255, 255, 255, 255))

    img.putdata(newData)
    img.save(output_path, "PNG")

if __name__ == "__main__":
    process_logo("header_logo.jpg", "logo_white.png", threshold=190)
