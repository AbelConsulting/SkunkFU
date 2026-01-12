from PIL import Image
import os

# thresholds for 'spike red'
R_MIN=200
G_MAX=100
B_MAX=100

screenshot='tmp-frames/rebuild_static_screenshot.png'
if not os.path.exists(screenshot):
    print('NO_SCREENSHOT')
    raise SystemExit(1)

img=Image.open(screenshot).convert('RGB')
px=img.load()
w,h=img.size
count=0
coords=[]
for y in range(0,h):
    for x in range(0,w):
        r,g,b=px[x,y]
        if r>=R_MIN and g<=G_MAX and b<=B_MAX:
            count+=1
            if len(coords)<10: coords.append((x,y,(r,g,b)))
print('screenshot_red_pixels',count)
if coords:
    print('sample_coords',coords)

# scan asset PNGs
red_files=[]
for root,dirs,files in os.walk('assets'):
    for fn in files:
        if fn.lower().endswith('.png'):
            path=os.path.join(root,fn)
            try:
                im=Image.open(path).convert('RGB')
            except Exception as e:
                continue
            px=im.load(); w2,h2=im.size
            c=0
            for y in range(h2):
                for x in range(w2):
                    r,g,b=px[x,y]
                    if r>=R_MIN and g<=G_MAX and b<=B_MAX:
                        c+=1
                        break
                if c>0: break
            if c>0:
                red_files.append((path,c))
print('asset_files_with_red_count>',len(red_files))
for p,c in red_files[:50]: print(p)
