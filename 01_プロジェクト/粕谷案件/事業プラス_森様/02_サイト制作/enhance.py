from PIL import Image, ImageEnhance
import sys

try:
    img_path = 'assets/images/hero_sashimi_landscape.png'
    img = Image.open(img_path).convert('RGB')
    
    # 1. シャープネスを限界近くまで引き上げる（表面の照り、ツヤ、エッジの透明感を最大化）
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.5) 
    
    # 2. 明るさをさらに強めて、光が奥まで透き通るような白飛びギリギリを狙う
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.18) 
    
    # 3. コントラストを一段上げて、ガラスのようなメリハリ（暗い部分と光の反射）を強化
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.15) 
    
    # 4. 彩度を少しだけ補って血色をよくする
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.15)
    
    img.save(img_path)
    print("Super Glassy enhancement applied successfully!")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
