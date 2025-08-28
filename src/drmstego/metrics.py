import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def psnr_rgb(a, b) -> float:
    return psnr(np.array(a), np.array(b), data_range=255)

def ssim_rgb(a, b) -> float:
    return ssim(np.array(a), np.array(b), channel_axis=2, data_range=255)
