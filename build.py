# Builds index.html (installable PWA) from src/app.html
src=open("src/app.html",encoding="utf-8").read()
head,body=src.split("<!--BODY-->",1)
out=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#1f4e79">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
{head.strip()}
</head><body>
{body.strip()}
</body></html>
'''
open("index.html","w",encoding="utf-8").write(out)
print("index.html built")
