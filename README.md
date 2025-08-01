# SmartMicroscopy_Zeiss

Ce dépôt contient deux projets développés lors d’un stage de fin d’études à l’IBDM (Institut de Biologie du Développement de Marseille), dans le cadre de l’automatisation de processus d’imagerie en microscopie intelligente à l’aide d’un microscope Zeiss CD7 et du logiciel Zen Blue.

## Projet 1 – Mesure automatique de la résolution (PSF)

**Objectif :** Automatiser l’acquisition de billes fluorescentes (PSF) et en extraire les profils X, Y, Z pour mesurer la résolution du système à l’aide d’un ajustement gaussien (fit 1D, 1D moyenné et 3D).

### Fonctionnalités :
- Acquisition automatisée (autofocus, auto-exposition, contrôle saturation/dynamique)
- Sélection de la bille la plus isolée et la plus intense
- Centrage automatique pour acquisition Z-Stack
- Extraction des profils X, Y, Z
- Envoi à des scripts Python externes pour le fit et calcul de la FWHM

### Fichiers :
- `Macro_PSF.xml` : Script Zen pour automatiser acquisition et traitement
- `fit1D_psf_profiles.py` : Fit gaussien 1D
- `fit1D_moyen_psf_profiles.py` : Fit 1D avec profils moyennés (réduction du bruit)
- `fit3D_psf.py` : Fit gaussien 3D

---

## Projet 2 – Suivi de fluorescence dans les gastruloïdes

**Objectif :** Localiser plusieurs échantillons dans une boîte de Petri, puis automatiser des acquisitions en fonction de leur emplacement et du canal (BF, vert, rouge) à intervalles réguliers.

### Fonctionnalités :
- Détection initiale des échantillons par analyse d’image (image BF)
- Enregistrement automatique de chaque échantillon toutes les heures
- Acquisition en plusieurs canaux : brightfield, GFP (vert), mCherry (rouge)
- Sauvegarde organisée par échantillon et horodatage

### Fichiers :
- `Macro_Gastruloides.xml` : Script Zen pour localisation et suivi automatisé

---

## Technologies utilisées

- **Langages** : IronPython, Python 3
- **Microscope** : Zeiss Celldiscoverer 7 (CD7)
- **Logiciels** : Zen Blue + OAD (Open Application Development), Zen Macro Editor
- **Bibliothèques Python** : NumPy, SciPy, matplotlib (utilisées dans les scripts externes)

---
