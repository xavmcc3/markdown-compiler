from javascript import require, globalThis

pdf = require('pdfjs')
url = './src/main.pdf'

print(pdf)
pdf.getDocument(url)
