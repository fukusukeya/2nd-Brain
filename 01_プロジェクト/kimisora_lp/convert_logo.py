from PIL import Image

def process_logo(input_path, output_path, threshold=230):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        gray = int(item[0] * 0.299 + item[1] * 0.587 + item[2] * 0.114)
        if gray > threshold:
            newData.append((255, 255, 255, 0))
        else:
            # 線の濃さに応じてアルファ値を設定し、色は真っ白にする
            # 真っ黒(0)ならalpha 255、グレー(100)ならalpha 155
            # 全体的に少し濃く見せるために係数をかける
            alpha = int((255 - gray) * 1.5)
            if alpha > 255: alpha = 255
            newData.append((255, 255, 255, alpha))

    img.putdata(newData)
    img.save(output_path, "PNG")

if __name__ == "__main__":
    process_logo("header_logo.jpg", "logo_white.png", threshold=230)
