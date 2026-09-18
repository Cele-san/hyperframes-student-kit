from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw, ImageFont
p=Path(__file__).parent
cues=json.loads((p/'cues.json').read_text())
font=ImageFont.truetype(str(p/'shared/Inter-Regular.ttf'),40)
capdir=p/'caption-assets';capdir.mkdir(exist_ok=True)
concat=[]
for i,(a,b,text) in enumerate(cues):
 im=Image.new('RGB',(1920,150),'#101827');draw=ImageDraw.Draw(im)
 box=draw.textbbox((0,0),text,font=font)
 draw.text(((1920-box[2]+box[0])/2,48),text,font=font,fill='#edf3fc')
 im.save(capdir/f'{i}.png')
 concat += [f"file '{i}.png'",f'duration {b-a:.6f}']
concat += [f"file '{len(cues)-1}.png'"]
(capdir/'captions.concat').write_text('\n'.join(concat)+'\n')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'master.mp4'),'-f','concat','-safe','0','-i',str(capdir/'captions.concat'),'-filter_complex','[0:v]setsar=1[v];[1:v]fps=30,setsar=1[c];[v][c]vstack[out]','-map','[out]','-t','30','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(p/'timing-preview.mp4')],check=True)
