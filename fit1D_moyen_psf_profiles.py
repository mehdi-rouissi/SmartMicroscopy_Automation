# ================================================
# Script : fit des profils X, Y, Z et export FWHM
# Auteur : ROUISSI Mehdi
# Date : [la date]
# Description : Ce script extrait les tailles de pixel depuis un fichier .czi,
#               réalise un fit gaussien sur les profils X, Y et Z, affiche les résultats,
#               trace les courbes et enregistre les FWHM dans un fichier texte.
# ================================================

###Import des bibliothèques
import czifile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
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
    except Exception as e:
        print("Erreur lors de la lecture des métadonnées :", e)
        scale_x = scale_y = scale_z = None
    return scale_x, scale_y, scale_z

###Fonction pour fit gaussien et calcul de FWHM
def fit_gaussien(fichier_source, pixel_size):
    df = pd.read_csv(fichier_source, skiprows=2, header=None)
    df.columns = ['Distance [px]', 'Intensity']
    df['Distance [px]'] = pd.to_numeric(df['Distance [px]'], errors='coerce')
    df['Intensity'] = pd.to_numeric(df['Intensity'], errors='coerce')
    df = df.dropna()
    x = df['Distance [px]'].values
    y = df['Intensity'].values
    def gaussienne(x, a, x0, sigma):
        return a * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))
    popt, _ = curve_fit(gaussienne, x, y, p0=[max(y), x[np.argmax(y)], 1])
    a_fit, x0_fit, sigma_fit = popt
    FWHM_px = 2.355 * sigma_fit
    FWHM_micron = FWHM_px * pixel_size
    result = {
        'a': a_fit,
        'x0': x0_fit,
        'sigma': sigma_fit,
        'FWHM_px': FWHM_px,
        'FWHM_micron': FWHM_micron,
        'x': x,
        'y': y,
        'popt': popt
    }
    return result

###Main extraction des tailles 
zstack_path = sys.argv[1]
scale_x, scale_y, scale_z = extraire_pixel_size(zstack_path)

###Main fit des profils X, Y et Z
profil_folder = sys.argv[2]
fichiers = {
    'X': (profil_folder + 'profil_X_moyen.csv', scale_x),
    'Y': (profil_folder + 'profil_Y_moyen.csv', scale_y),
    'Z': (profil_folder + 'profil_Z_moyen.csv', scale_z)
}

resultats = {}
for axe, (fichier, pixel_size) in fichiers.items():
    resultats[axe] = fit_gaussien(fichier, pixel_size)


###Affichage des résultats du fit 
for axe, res in resultats.items():
    print(f"=== Pour l'axe {axe} ===")
    #print(f"   a = {res['a']:.2f}, x0 = {res['x0']:.2f}, sigma = {res['sigma']:.2f}")
    print(f"   FWHM = {res['FWHM_px']:.2f} pixels = {res['FWHM_micron']:.2f} microns")


###Sauvegarde des FWHM dans un fichier texte


output_folder = sys.argv[3]
output_path = os.path.join(output_folder, "FWHM1D_moyen_results.txt")
with open(output_path, "w") as f:
    f.write(f"fwhm_x = {resultats['X']['FWHM_micron']:.2f}\n")
    f.write(f"fwhm_y = {resultats['Y']['FWHM_micron']:.2f}\n")
    f.write(f"fwhm_z = {resultats['Z']['FWHM_micron']:.2f}\n")
print(f"FWHM et Courbes enregistrés dans :" ,output_folder)


###Tracer les courbes 
fig, axes = plt.subplots(3, 1, figsize=(8, 12))

for idx, (axe, res) in enumerate(resultats.items()):
    ax = axes[idx]
    ax.scatter(res['x'], res['y'], label='Données')
    x_fit = np.linspace(min(res['x']), max(res['x']), 500)
    y_fit = res['a'] * np.exp(-((x_fit - res['x0']) ** 2) / (2 * res['sigma'] ** 2))
    ax.plot(x_fit, y_fit, color='red', label='Fit gaussien')
    ax.set_xlabel('Distance [px]')
    ax.set_ylabel('Intensity')
    ax.set_title(f'Fit gaussien {axe}')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.savefig(output_folder + "fit1D_moyen_all_axes.png")
plt.close()
