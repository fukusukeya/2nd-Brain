import fitz
import base64
import os

doc = fitz.open('kimisora_hagaki1.pdf')
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    pix.save(f"page_{i}.png")
