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

**Objectif :** Automatiser le suivi de plusieurs gastruloïdes vivants dans une boîte de Petri, en déclenchant des acquisitions différenciées selon leur état de fluorescence (GFP, mCherry), avec une logique d'adaptation dynamique au comportement biologique.

### Fonctionnalités :
- Scan initial de la boîte pour localiser automatiquement les échantillons par analyse d’image
- Validation manuelle des échantillons détectés (interface utilisateur)
- Suivi automatisé en 3 groupes :
  - **Groupe 1** : Acquisitions GFP toutes les 30 minutes
  - **Groupe 2** : Acquisitions GFP + mCherry avec intervalle croissant selon apparition de GFP
  - **Groupe 3** : Acquisitions GFP + mCherry en faible exposition toutes les 30 minutes
- Changement automatique de groupe selon détection de signal vert ou rouge
- Sauvegarde structurée des images (par échantillon, par groupe, avec horodatage)

### Fichiers :
- `Macro_Gastruloides.xml` : Script Zen pour la localisation initiale et le suivi intelligent en temps réel
- Le script gère automatiquement l’ajout/suppression de tuiles, le positionnement, l’analyse d’image, et la gestion du temps entre acquisitions.

---

## Technologies utilisées

- **Langages** : IronPython, Python 3
- **Microscope** : Zeiss Celldiscoverer 7 (CD7)
- **Logiciels** : Zen Blue + OAD (Open Application Development), Zen Macro Editor
- **Bibliothèques Python** : NumPy, SciPy, matplotlib (utilisées dans les scripts externes)

---
