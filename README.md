#  TP — Morphologie Mathématique & Segmentation (Sans librairie)

**Étudiant :** Ayoub chichti

## 📝 Description du projet
Ce projet est une implémentation complète des algorithmes fondamentaux de traitement d'image (Morphologie Mathématique), codée entièrement **"from scratch"**.

L'objectif était de manipuler des images sous forme de listes de listes et de recréer les opérations de base sans utiliser de bibliothèques externes comme OpenCV.

##  Fonctionnalités implémentées
J'ai réalisé l'intégralité du sujet, y compris les **parties optionnelles (Bonus)**.

### 1. Fondamentaux (Binaire)
- **Structure de données :** Gestion d'images sous forme de matrices (listes de listes).
- **Éléments structurants :** Carré, Ligne verticale, Croix.
- **Opérations :** Érosion, Dilatation, Ouverture, Fermeture.

### 2. Exercices d'application
- **Exercice 1 (Le Pont) :** Rupture d'un pont fin via une érosion verticale.
- **Exercice 2 (Filtre de taille) :** Utilisation de l'ouverture pour supprimer les petits objets (bruit) tout en gardant les gros.
- **Exercice 3 (Nettoyage) :** Implémentation de `remove_small_holes` pour boucher les trous dans les objets.

### 3. BONUS 
- **Niveaux de gris :** Implémentation de l'érosion (Minimum local) et de la dilatation (Maximum local).
- **Gestion de fichiers (I/O) :** Lecture et écriture manuelle du format **PGM ASCII (P2)**.
- **Segmentation automatique :** Implémentation de l'algorithme d'**Otsu** pour trouver le seuil optimal et binariser une image grise.

## 📂Contenu du dépôt
Voici les fichiers présents dans ce dépôt :

| Fichier | Description |
| :--- | :--- |
| `tp_morpho.py` | **Le code source complet.** Contient toutes les fonctions et les tests. |
| `test_input.pgm` | Image synthétique (gris) générée automatiquement par le script pour tester Otsu. |
| `test_result.pgm` | Résultat final de la segmentation par Otsu (Binarisée), prouvant que le code fonctionne. |



```bash
python tp_morpho.py
