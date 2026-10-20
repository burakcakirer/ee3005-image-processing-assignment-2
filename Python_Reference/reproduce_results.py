"""Reference image processing run, metrics, and report-ready figures.

MATLAB source in ../MATLAB is the requested course deliverable; this numerical
reference is included to make submitted outputs reproducible without MATLAB.
Use provided sample images only. Experimental images are NOT clinical images.
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage import exposure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
PREP=ROOT/'Source_Images'/'Prepared_Inputs'
RAW=ROOT/'Source_Images'/'Original_Samples'
FIG=ROOT/'Report'/'Figures'
RES=ROOT/'Outputs'/'Results'
for d in (PREP,FIG,RES): d.mkdir(parents=True,exist_ok=True)
SEED=3005
rng=np.random.default_rng(SEED)
plt.rcParams.update({'font.size':9,'axes.titlesize':10,'figure.titlesize':15,'savefig.dpi':170,'font.family':'DejaVu Sans'})


def save_input(name,x):
    x=np.clip(x,0,1)
    Image.fromarray(np.rint(x*255).astype(np.uint8)).save(PREP/name)
    return np.array(Image.open(PREP/name),dtype=np.float64)/255.0

def read_original(name):
    # Explicit RGB->gray conversion (matching MATLAB rgb2gray to rounding tolerance).
    a=cv2.imread(str(RAW/name),cv2.IMREAD_COLOR)
    if a is None:raise OSError(f'Cannot load {name}')
    return cv2.cvtColor(a,cv2.COLOR_BGR2GRAY).astype(np.float64)/255.0

chest=save_input('chest_xray_gray.png',read_original('image3.jpg'))
brain=save_input('brain_mri_gray.png',read_original('image2.jpg'))

def psnr(ref,x):
    mse=np.mean(np.square(x-ref,dtype=np.float64))
    return float('inf') if mse==0 else -10*math.log10(mse)

def get_kernel(n,sigma):
    g=cv2.getGaussianKernel(n,sigma).flatten()
    return np.outer(g,g)

def filt(x,k,mode='reflect'):
    return ndi.correlate(x,k,mode=mode)

def mean(x,n):return ndi.uniform_filter(x,size=n,mode='reflect')
def gauss(x,n,s):return filt(x,get_kernel(n,s))
def median(x,n):return ndi.median_filter(x,size=n,mode='reflect')
def hist_eq(x):return exposure.equalize_hist(x,nbins=256)
def tile_shape(x,t):return (max(4,int(round(x.shape[0]/t))),max(4,int(round(x.shape[1]/t))))
def clahe(x,clip=.015,tiles=8):
    return exposure.equalize_adapthist(np.clip(x,0,1),kernel_size=tile_shape(x,tiles),clip_limit=clip,nbins=256)
def ahe(x,tiles=8):return clahe(x,clip=1.,tiles=tiles)

def geo(x,n):
    # For zero valued images, epsilon enforces a well-defined log.
    return np.exp(ndi.uniform_filter(np.log(np.maximum(x,1/255)),size=n,mode='reflect'))
def harmonic(x,n):return 1/ndi.uniform_filter(1/np.maximum(x,1/255),size=n,mode='reflect')
def contra(x,n,q):
    z=np.maximum(x,1/255) if q<0 else x
    numerator=ndi.uniform_filter(z**(q+1),size=n,mode='reflect')
    denominator=ndi.uniform_filter(z**q,size=n,mode='reflect')
    return np.divide(numerator,denominator,out=np.zeros_like(x),where=denominator>1e-12).clip(0,1)

def noisy_gauss(x,sigma=.06):return save_input('gaussian_noise.png',np.clip(x+rng.normal(0,sigma,size=x.shape),0,1))
def noisy_impulse(x,density=.08,which='both',name='sp_noise.png'):
    r=rng.random(x.shape)
    z=x.copy()
    if which=='both':z[r<density/2]=0;z[(r>=density/2)&(r<density)]=1
    if which=='salt':z[r<density]=1
    if which=='pepper':z[r<density]=0
    return save_input(name,z)

def savefig(filename):
    plt.savefig(FIG/filename,bbox_inches='tight',facecolor='white',dpi=170)
    plt.close()

def imgplot(ax,x,title,cmap='gray',range01=True):
    ax.imshow(x,cmap=cmap,vmin=0 if range01 else None,vmax=1 if range01 else None)
    ax.set_title(title,pad=6)
    ax.axis('off')

def panel(filename,items,cols=4,title=None,imsize=(3.4,3.1)):
    rows=int(math.ceil(len(items)/cols))
    fig,axs=plt.subplots(rows,cols,figsize=(imsize[0]*cols,imsize[1]*rows+(.5 if title else 0)),squeeze=False,constrained_layout=True)
    if title:fig.suptitle(title,fontweight='bold')
    for ax,(text,x) in zip(axs.flat,items):imgplot(ax,x,text)
    for ax in axs.flat[len(items):]:ax.axis('off')
    savefig(filename)

# Task 1
h=hist_eq(chest)
a=ahe(chest)
c1=clahe(chest,.01,8)
c2=clahe(chest,.03,16)
fig,ax=plt.subplots(2,5,figsize=(17,7.4),constrained_layout=True)
for j,(name,x) in enumerate([('Original',chest),('Global HE',h),('AHE (8x8)',a),('CLAHE (8x8, clip .01)',c1),('CLAHE (16x16, clip .03)',c2)]):
    imgplot(ax[0,j],x,name)
    ax[1,j].hist(x.ravel(),bins=64,range=(0,1),color='#36688e')
    ax[1,j].set_xlim(0,1);ax[1,j].set_xlabel('Intensity (0 to 1)')
    ax[1,j].set_ylabel('Pixel count' if j==0 else '')
fig.suptitle('Task 1 | Biomedical chest radiograph and intensity histograms',fontweight='bold')
savefig('F01_contrast_histograms.png')
roi=(slice(190,470),slice(210,510))
t1metrics={n:{'global_std':float(x.std()),'central_roi_std':float(x[roi].std())} for n,x in [('Original',chest),('HE',h),('AHE',a),('CLAHE_8x8_0.01',c1),('CLAHE_16x16_0.03',c2)]}

# Task 2
A=np.array([[10,20,30,40,50],[15,25,35,45,55],[20,30,40,50,60],[25,35,45,55,65],[30,40,50,60,70]])
K=np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
P=A[1:4,1:4]
correlation=int(np.sum(P*K)); convolution=int(np.sum(P*np.flip(K)))
assert (correlation,convolution)==(-80,80)
with (RES/'task02_manual_calculations.txt').open('w') as f:
    f.write('Center patch P =\n'+str(P)+'\nKernel K =\n'+str(K)+'\nFlipped K =\n'+str(np.flip(K))+'\n')
    f.write('Correlation element products =\n'+str(P*K)+'\nSum = '+str(correlation)+'\n')
    f.write('Convolution element products =\n'+str(P*np.flip(K))+'\nSum = '+str(convolution)+'\n')
edge_chest=chest[140:650,165:620]
padded={
    'Zero':ndi.uniform_filter(edge_chest,size=3,mode='constant',cval=0),
    'Replicate':ndi.uniform_filter(edge_chest,size=3,mode='nearest'),
    'Reflect':ndi.uniform_filter(edge_chest,size=3,mode='mirror'),
    'Circular':ndi.uniform_filter(edge_chest,size=3,mode='wrap')
}
fig,ax=plt.subplots(2,4,figsize=(13.8,7.1),constrained_layout=True)
for j,(name,x) in enumerate(padded.items()):
    imgplot(ax[0,j],x,name+' padding')
    imgplot(ax[1,j],x[:70,:90],name+' | upper-left crop')
fig.suptitle('Task 2 | Same 3x3 mean kernel, different boundary conditions',fontweight='bold')
savefig('F02_padding_comparison.png')
mask=np.zeros_like(edge_chest,dtype=bool);mask[0,:]=mask[-1,:]=True;mask[:,0]=mask[:,-1]=True
pad_mae={name:float(np.abs(x-padded['Reflect'])[mask].mean()) for name,x in padded.items()}

# Task 3
G=np.outer([1,2,1],[1,2,1])/16.0
v=np.array([1,2,1])/4
assert np.array_equal(G,np.outer(v,v))
direct=filt(brain,G)
sep=ndi.correlate1d(ndi.correlate1d(brain,v,axis=1,mode='reflect'),v,axis=0,mode='reflect')
maxdiff=float(np.max(np.abs(direct-sep)))
panel('F03_separable_gaussian.png',[('Original MRI',brain),('Direct 3x3 Gaussian',direct),('1D horizontal then vertical',sep),('Absolute difference x1e12',np.clip(np.abs(sep-direct)*1e12,0,1))],cols=4,title='Task 3 | 2D versus separable 1D Gaussian smoothing')

# Task 4
ng=noisy_gauss(brain)
ns=noisy_impulse(brain,.08,'both','sp_noise.png')
methods={'Noisy':lambda x:x,'Mean 3x3':lambda x:mean(x,3),'Mean 5x5':lambda x:mean(x,5),'Gaussian 3x3 s=.8':lambda x:gauss(x,3,.8),'Gaussian 7x7 s=1.4':lambda x:gauss(x,7,1.4)}
t4=[]
for noise,inp in [('Gaussian sigma=.06',ng),('Salt-pepper density=.08',ns)]:
    items=[('Clean reference',brain)]
    for name,fn in methods.items():
        x=fn(inp)
        t4.append({'noise':noise,'filter':name,'psnr_db':round(psnr(brain,x),4)})
        items.append((name+'\nPSNR '+f'{psnr(brain,x):.2f} dB',x))
    panel('F04_'+('gaussian' if noise.startswith('Gaussian') else 'impulse')+'_filtering.png',items,cols=3,title='Task 4 | '+noise,imsize=(3.8,3.25))

# Task 5
salt=noisy_impulse(brain,.08,'salt','salt_only.png')
pepper=noisy_impulse(brain,.08,'pepper','pepper_only.png')
t5=[]
def record(noise,name,x):
    t5.append({'noise':noise,'filter':name,'psnr_db':round(psnr(brain,x),4)})
    return x
mix_items=[('Clean',brain),('Salt & pepper',record('mixed_salt_pepper','Noisy',ns))]
for name,out in [('Mean 3x3',mean(ns,3)),('Median 3x3',median(ns,3)),('Median 5x5',median(ns,5))]:
    mix_items.append((name+f'\n{psnr(brain,out):.2f} dB',record('mixed_salt_pepper',name,out)))
panel('F05_median_impulse.png',mix_items,cols=3,title='Task 5 | Median versus arithmetic mean for impulse contamination')
variant_items=[('Clean reference',brain),('Gaussian noisy',ng)]
for name,x in [('Geometric 3x3',geo(ng,3)),('Harmonic 3x3',harmonic(ng,3)),('Mean 3x3',mean(ng,3))]:
    variant_items.append((name+f'\n{psnr(brain,x):.2f} dB',record('gaussian',''+name,x)))
panel('F06_mean_variants.png',variant_items,cols=3,title='Task 5 | Alternative nonlinear mean filters on Gaussian noise')
contra_items=[('Clean reference',brain),('Salt only (8%)',record('salt_only','Noisy',salt)),('Pepper only (8%)',record('pepper_only','Noisy',pepper))]
for noisy,n in [(salt,'salt_only'),(pepper,'pepper_only')]:
    for q in [1.5,-1.5]:
        z=record(n,f'Contra 3x3 Q={q:+.1f}',contra(noisy,3,q))
        contra_items.append((f'{n} Q={q:+.1f}\n{psnr(brain,z):.2f} dB',z))
panel('F07_contraharmonic.png',contra_items,cols=4,title='Task 5 | Contra-harmonic filters: Q sign versus impulse polarity')

# Task 6
blur=gauss(brain,5,1.2)
sharp={gamma:np.clip(brain+gamma*(brain-blur),0,1) for gamma in [.5,1,2.5]}
sharp_items=[('Original MRI',brain),('Gaussian-blurred (5x5)',blur)]
for gamma,x in sharp.items():sharp_items.append((f'Unsharp gamma={gamma}',x))
panel('F08_unsharp.png',sharp_items,cols=3,title='Task 6 | Gaussian high-pass unsharp masking')
sharp_stats={str(g):{'clipped_percentage':float(100*np.mean((brain+g*(brain-blur)<0)|(brain+g*(brain-blur)>1))),'mean_absolute_change':float(np.abs(x-brain).mean())} for g,x in sharp.items()}

# Task 7
sobel=lambda x:np.hypot(ndi.sobel(x,axis=0,mode='reflect'),ndi.sobel(x,axis=1,mode='reflect'))/8
lap=lambda x:ndi.laplace(x,mode='reflect')
lo=lap(gauss(brain,7,1.2))
dog12=ndi.gaussian_filter(brain,1.,mode='reflect')-ndi.gaussian_filter(brain,2.,mode='reflect')
dog24=ndi.gaussian_filter(brain,2.,mode='reflect')-ndi.gaussian_filter(brain,4.,mode='reflect')
def rescale(x):
    a=np.abs(x);scale=np.percentile(a,99.5)
    return np.clip(a/max(scale,1e-9),0,1)
panel('F09_edges.png', [('MRI',brain),('Sobel | gradient|',rescale(sobel(brain))),('Laplacian |response|',rescale(lap(brain))),('LoG: G(1.2) then Lap',rescale(lo)),('DoG sigma 1 & 2',rescale(dog12)),('DoG sigma 2 & 4',rescale(dog24)),('Sobel on noisy MRI',rescale(sobel(ng))),('Laplacian on noisy MRI',rescale(lap(ng)))],cols=4,title='Task 7 | Derivative operators and Gaussian scale comparisons')
t7_stats={'sobel_clean_mean':float(sobel(brain).mean()),'sobel_gaussian_noisy_mean':float(sobel(ng).mean()),'laplacian_clean_mean_abs':float(abs(lap(brain)).mean()),'laplacian_noisy_mean_abs':float(abs(lap(ng)).mean())}

# Task 8: noisy low-contrast chest input from supplied image, synthetic mixed noise
mix=np.clip(chest+rng.normal(0,.03,size=chest.shape),0,1)
r=rng.random(chest.shape)
mix[r<.0125]=0;mix[(r>=.0125)&(r<.025)]=1
mix=save_input('pipeline_mixed_input.png',mix)
step1=median(mix,3)
step2=clahe(step1,.01,8)
step3=gauss(step2,5,1.1)
final=np.clip(step2+.7*(step2-step3),0,1)
panel('F10_pipeline.png',[('Clean source (reference)',chest),('Mixed noise input',mix),('Step 1: median 3x3',step1),('Step 2: CLAHE',step2),('Step 3: unsharp gamma .7',final)],cols=3,title='Task 8 | Denoising -> local contrast -> restrained sharpening')
pipeline_metrics={label:{'psnr_to_clean_db':(round(psnr(chest,x),4) if label!='Clean' else None),'image_std':round(float(x.std()),5),'entropy_bits':round(float(exposure.shannon_entropy(np.rint(x*255).astype(np.uint8))) if hasattr(exposure,'shannon_entropy') else float(-np.sum(np.histogram(x,bins=256,range=(0,1),density=False)[0]/x.size*np.log2(np.maximum(np.histogram(x,bins=256,range=(0,1))[0]/x.size,1e-12)))),4)} for label,x in [('Clean',chest),('Noisy',mix),('Median',step1),('CLAHE',step2),('Final',final)]}

# Write machine-readable experiment outputs
for name,rows in [('task04_psnr.csv',t4),('task05_psnr.csv',t5)]:
    with (RES/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
meta={
 'random_seed':SEED,'inputs':{'chest':'provided image3.jpg converted to grayscale png','brain':'provided image2.jpg converted to grayscale png'},
 't1_contrast_metrics':t1metrics,'t2_center_patch':P.tolist(),'t2_kernel':K.tolist(),'t2_corr_center':correlation,'t2_conv_center':convolution,'t2_boundary_mae_vs_reflection':pad_mae,
 't3_kernel':G.tolist(),'t3_kernel_outer_product':np.outer(v,v).tolist(),'t3_max_abs_difference':maxdiff,'t3_multiplications_per_pixel':{'direct':9,'separable':6},
 't4_psnr':t4,'t5_psnr':t5,'t6_sharpening':sharp_stats,'t7_edge_stats':t7_stats,'t8_pipeline':pipeline_metrics,
 'software':'Python + scipy + scikit-image + OpenCV (reference run, not MATLAB)','units':{'intensity':'[0,1]','psnr':'dB'}
}
(RES/'experiment_metrics.json').write_text(json.dumps(meta,indent=2,allow_nan=False))
print('Task2 correlation/convolution',correlation,convolution)
print('Task3 max absolute diff',maxdiff)
print('Task4',t4)
print('Task5',t5)
print('Task8',pipeline_metrics)
print('Wrote figures',len(list(FIG.glob('*.png'))))
