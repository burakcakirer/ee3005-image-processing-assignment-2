"""Fast consistency checks on packaged metrics and prepared inputs."""
import csv,json,math
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
metrics=json.loads((ROOT/'Outputs/Results/experiment_metrics.json').read_text())
assert metrics['t2_corr_center']==-80
assert metrics['t2_conv_center']==80
assert metrics['t3_max_abs_difference']<1e-12
assert len(metrics['t4_psnr'])==10
assert len(metrics['t5_psnr'])>=12
assert len(list((ROOT/'Report/Figures').glob('F*.png')))==11
for n in ['brain_mri_gray.png','chest_xray_gray.png','gaussian_noise.png','sp_noise.png','salt_only.png','pepper_only.png','pipeline_mixed_input.png']:
    x=Image.open(ROOT/'Source_Images/Prepared_Inputs'/n)
    assert x.mode=='L',n
res=metrics['t5_psnr']
def score(noise,f):return next(r['psnr_db'] for r in res if r['noise']==noise and r['filter']==f)
assert score('mixed_salt_pepper','Median 3x3')>score('mixed_salt_pepper','Mean 3x3')
assert score('pepper_only','Contra 3x3 Q=+1.5')>score('pepper_only','Contra 3x3 Q=-1.5')
assert score('salt_only','Contra 3x3 Q=-1.5')>score('salt_only','Contra 3x3 Q=+1.5')
print('All packaged output checks passed.')
