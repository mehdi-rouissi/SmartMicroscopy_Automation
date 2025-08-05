# ================================================
# Script : fit 3D et export FWHM
# Auteur : ROUISSI Mehdi
# Date : 17/07
# Description : Ce script extrait les tailles de pixel depuis un fichier .czi,
#               réalise un fit gaussien 3D, affiche les résultats,
#               trace les plans 2D et enregistre les FWHM dans un fichier texte.
# ================================================

###Import des bibliothèques
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from aicspylibczi import CziFile
import czifile
import sys
import os

###Fonction pour extraire la taille des pixels depuis le zstack.czi
def extraire_pixel_size(file_path):
    czi = czifile.CziFile(file_path)
    metadata = czi.metadata(raw=False)
    try:
        scale_x = float(metadata['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][0]['Value']) * 1e6
        scale_y = float(metadata['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][1]['Value']) * 1e6
        scale_z = float(metadata['ImageDocument']['Metadata']['Scaling']['Items']['Distance'][2]['Value']) * 1e6
    except:
        scale_x = scale_y = scale_z = None
    return scale_x, scale_y, scale_z

###Fonction pour fit 3D
def gaussian_3d(coords, amp, x0, y0, z0, sigma_x, sigma_y, sigma_z, offset):
    x, y, z = coords
    g = amp * np.exp(-(((x - x0)**2)/(2*sigma_x**2) + ((y - y0)**2)/(2*sigma_y**2) + ((z - z0)**2)/(2*sigma_z**2))) + offset
    return g.ravel()

###Lecture des chemins
zstack_path = sys.argv[1]
output_folder = sys.argv[2]

###Extraction échelle
czi = CziFile(zstack_path)
scale_x, scale_y, scale_z = extraire_pixel_size(zstack_path)
image, _ = czi.read_image()
image_3d = np.squeeze(image)
Z, Y, X = image_3d.shape
z, y, x = np.meshgrid(np.arange(Z), np.arange(Y), np.arange(X), indexing='ij')

###Definition des valeurs initiales 
z0, y0, x0 = np.unravel_index(np.argmax(image_3d), image_3d.shape)
sigma_x = 10 / (2.355 * scale_x)
sigma_y = 10 / (2.355 * scale_y)
sigma_z = 10 / (2.355 * scale_z)

initial_guess = (
    image_3d.max(),
    x0, y0, z0,
    sigma_x, sigma_y, sigma_z,
    np.median(image_3d)
)

lower_bounds = [0,0,0,0,0,0,0,-np.inf]
upper_bounds = [np.inf]*8

###Main Fit
popt, _ = curve_fit(
    gaussian_3d,
    (x, y, z),
    image_3d.ravel(),
    p0=initial_guess,
    bounds=(lower_bounds,upper_bounds),
    maxfev=5000
)

amp, x0, y0, z0, sx, sy, sz, offset = popt
fwhm_x = 2.355 * sx * scale_x
fwhm_y = 2.355 * sy * scale_y
fwhm_z = 2.355 * sz * scale_z

print(f"=== Pour l'axe X ===")
print(f"   FWHM = {fwhm_x:.2f} microns")
print(f"=== Pour l'axe Y ===")
print(f"   FWHM = {fwhm_y:.2f} microns")
print(f"=== Pour l'axe Z ===")
print(f"   FWHM = {fwhm_z:.2f} microns")

###Sauvegarde des FWHM dans un fichier texte
os.makedirs(output_folder, exist_ok=True)
result_file = os.path.join(output_folder, "FWHM_results_3D.txt")
with open(result_file, "w") as f:
    f.write(f"fwhm_x = {fwhm_x:.2f}\n")
    f.write(f"fwhm_y = {fwhm_y:.2f}\n")
    f.write(f"fwhm_z = {fwhm_z:.2f}\n")

###EXtraction des plans XY, XZ, YZ
xg_xy, yg_xy = np.meshgrid(np.arange(X), np.arange(Y), indexing='xy')
fit_xy = amp * np.exp(-(((xg_xy - x0)**2)/(2*sx**2) + ((yg_xy - y0)**2)/(2*sy**2))) + offset
real_xy = image_3d[int(round(z0)), :, :]

xg_xz, zg_xz = np.meshgrid(np.arange(X), np.arange(Z), indexing='xy')
fit_xz = amp * np.exp(-(((xg_xz - x0)**2)/(2*sx**2) + ((zg_xz - z0)**2)/(2*sz**2))) + offset
real_xz = image_3d[:, int(round(y0)), :]

yg_yz, zg_yz = np.meshgrid(np.arange(Y), np.arange(Z), indexing='xy')
fit_yz = amp * np.exp(-(((yg_yz - y0)**2)/(2*sy**2) + ((zg_yz - z0)**2)/(2*sz**2))) + offset
real_yz = image_3d[:, :, int(round(x0))]

###Sauvegarde des Plans 
def save_comparison_fig(img1, img2, title1, title2, filename, cmap1='gray', cmap2='viridis'):
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    axs[0].imshow(img1, cmap=cmap1, aspect='auto')
    axs[0].set_title(title1)
    axs[1].imshow(img2, cmap=cmap2, aspect='auto')
    axs[1].set_title(title2)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, filename))
    plt.close()
       
save_comparison_fig(real_xy, fit_xy, "Image réelle - Plan XY", "Fit Gaussien - Plan XY", "plan_XY.png")
save_comparison_fig(real_xz, fit_xz, "Image réelle - Plan XZ", "Fit Gaussien - Plan XZ", "plan_XZ.png")
save_comparison_fig(real_yz, fit_yz, "Image réelle - Plan YZ", "Fit Gaussien - Plan YZ", "plan_YZ.png")

