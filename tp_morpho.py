import sys

# =============================================================================
# 1. UTILITAIRES & AFFICHAGE
# =============================================================================

def dims(img):
    """Retourne (hauteur, largeur)."""
    if not img: return 0, 0
    return len(img), len(img[0])

def zeros(h, w, val=0):
    """Crée une image vide h x w remplie de val."""
    return [[val for _ in range(w)] for _ in range(h)]

def pretty_bin(img, titre="Image Binaire"):
    """Affichage ASCII (1=#, 0=.)"""
    print(f"--- {titre} ---")
    for row in img:
        print("".join('# ' if v else '. ' for v in row))
    print()

def pretty_gray(img, titre="Image Grise"):
    """Affichage ASCII Niveaux de Gris (0..255)."""
    chars = " .:-=+*#%@"
    print(f"--- {titre} ---")
    for row in img:
        line = []
        for v in row:
            val = max(0, min(255, int(v)))
            idx = int((val / 256.0) * len(chars))
            line.append(chars[idx])
        print(" ".join(line))
    print()

# =============================================================================
# 2. ÉLÉMENTS STRUCTURANTS
# =============================================================================

def strel_square(k):
    """Carré k x k (k impair)."""
    r = k // 2
    return [(dy, dx) for dy in range(-r, r+1) for dx in range(-r, r+1)]

def strel_line_vertical(k):
    """Ligne verticale de hauteur k."""
    r = k // 2
    return [(dy, 0) for dy in range(-r, r+1)]

# =============================================================================
# 3. MORPHOLOGIE BINAIRE
# =============================================================================

def erode_bin(img, se):
    h, w = dims(img)
    out = zeros(h, w, 0)
    for y in range(h):
        for x in range(w):
            ok = True
            for dy, dx in se:
                yy, xx = y + dy, x + dx
                if not (0 <= yy < h and 0 <= xx < w) or img[yy][xx] == 0:
                    ok = False
                    break
            out[y][x] = 1 if ok else 0
    return out

def dilate_bin(img, se):
    h, w = dims(img)
    out = zeros(h, w, 0)
    for y in range(h):
        for x in range(w):
            hit = False
            for dy, dx in se:
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and img[yy][xx] == 1:
                    hit = True
                    break
            out[y][x] = 1 if hit else 0
    return out

def opening_bin(img, se):
    return dilate_bin(erode_bin(img, se), se)

def closing_bin(img, se):
    return erode_bin(dilate_bin(img, se), se)

# =============================================================================
# 4. MORPHOLOGIE NIVEAUX DE GRIS (BONUS 1)
# =============================================================================

def erode_gray(img, se):
    h, w = dims(img)
    out = zeros(h, w)
    for y in range(h):
        for x in range(w):
            min_val = 255
            for dy, dx in se:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w:
                    val = img[ny][nx]
                else:
                    val = 255 # Bord infini
                if val < min_val: min_val = val
            out[y][x] = min_val
    return out

def dilate_gray(img, se):
    h, w = dims(img)
    out = zeros(h, w)
    for y in range(h):
        for x in range(w):
            max_val = 0
            for dy, dx in se:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w:
                    val = img[ny][nx]
                else:
                    val = 0 # Bord noir
                if val > max_val: max_val = val
            out[y][x] = max_val
    return out

# =============================================================================
# 5. OUTILS AVANCÉS (LABELING & TROUS)
# =============================================================================

def connected_components_4(img):
    h, w = dims(img)
    labels = zeros(h, w, 0)
    current = 0
    for y in range(h):
        for x in range(w):
            if img[y][x] == 1 and labels[y][x] == 0:
                current += 1
                q = [(y, x)]
                labels[y][x] = current
                while q:
                    yy, xx = q.pop(0)
                    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ny, nx = yy+dy, xx+dx
                        if 0 <= ny < h and 0 <= nx < w:
                            if img[ny][nx] == 1 and labels[ny][nx] == 0:
                                labels[ny][nx] = current
                                q.append((ny, nx))
    return labels, current

def remove_small_objects(img, min_size):
    labels, n = connected_components_4(img)
    h, w = dims(img)
    sizes = [0]*(n+1)
    for row in labels:
        for lab in row:
            if lab > 0: sizes[lab] += 1
    out = zeros(h, w, 0)
    for y in range(h):
        for x in range(w):
            lab = labels[y][x]
            out[y][x] = 1 if (lab > 0 and sizes[lab] >= min_size) else 0
    return out

def invert_img(img):
    return [[1 - v for v in row] for row in img]

def remove_small_holes(img, max_hole_size):
    inv = invert_img(img)
    cleaned = remove_small_objects(inv, max_hole_size + 1)
    return invert_img(cleaned)

# =============================================================================
# 6. GESTION PGM & OTSU (BONUS 2)
# =============================================================================

def save_pgm(img, filename):
    h, w = dims(img)
    with open(filename, 'w') as f:
        f.write("P2\n")
        f.write(f"{w} {h}\n255\n")
        for row in img:
            f.write(" ".join(str(max(0, min(255, int(v)))) for v in row) + "\n")
    print(f"[IO] Image sauvegardée : {filename}")

def load_pgm(filename):
    with open(filename, 'r') as f:
        tokens = f.read().split()
    assert tokens[0] == 'P2'
    w, h = int(tokens[1]), int(tokens[2])
    data = tokens[4:]
    img = []
    idx = 0
    for y in range(h):
        row = []
        for x in range(w):
            row.append(int(data[idx]))
            idx += 1
        img.append(row)
    print(f"[IO] Image chargée : {filename} ({w}x{h})")
    return img

def otsu_threshold(img):
    hist = [0] * 256
    total_pixels = 0
    for row in img:
        for v in row:
            hist[int(v)] += 1
            total_pixels += 1
    
    sum_total = sum(i * hist[i] for i in range(256))
    weight_bg = 0
    sum_bg = 0
    max_variance = -1.0
    threshold = 0
    
    for t in range(256):
        weight_bg += hist[t]
        if weight_bg == 0: continue
        weight_fg = total_pixels - weight_bg
        if weight_fg == 0: break
        
        sum_bg += t * hist[t]
        mean_bg = sum_bg / weight_bg
        mean_fg = (sum_total - sum_bg) / weight_fg
        
        var = weight_bg * weight_fg * (mean_bg - mean_fg) ** 2
        if var > max_variance:
            max_variance = var
            threshold = t
    return threshold

def apply_threshold(img, thr):
    return [[1 if val > thr else 0 for val in row] for row in img]

# =============================================================================
# 7. MAIN (TESTS)
# =============================================================================

if __name__ == "__main__":
    print("=== TP MORPHOLOGIE MATHEMATIQUE (COMPLET) ===\n")

    # --- EXERCICE 1 ---
    print(">>> Exercice 1 : Le Pont")
    img_pont = [
        [0,0,0,0,0,0,0,0],
        [0,1,1,0,0,1,1,0],
        [0,1,1,1,1,1,1,0],
        [0,1,1,0,0,1,1,0],
        [0,0,0,0,0,0,0,0]
    ]
    pretty_bin(img_pont, "Originale")
    pretty_bin(erode_bin(img_pont, strel_line_vertical(3)), "Après Érosion Verticale")

    # --- EXERCICE 2 ---
    print("\n>>> Exercice 2 : Filtre de taille")
    img_t = zeros(7, 10)
    img_t[1][1] = 1 # 1px
    for y in range(1,4):
        for x in range(4,7): img_t[y][x] = 1 # 3x3
    pretty_bin(img_t, "Originale (1px + 3x3)")
    pretty_bin(opening_bin(img_t, strel_square(3)), "Ouverture k=3")
    pretty_bin(opening_bin(img_t, strel_square(5)), "Ouverture k=5")

    # --- EXERCICE 3 ---
    print("\n>>> Exercice 3 : Trous")
    img_h = [[1,1,1,1,1],[1,0,1,1,1],[1,1,1,0,1],[1,1,1,1,1]]
    pretty_bin(img_h, "Originale")
    pretty_bin(remove_small_holes(img_h, 1), "Trous nettoyés")

    # --- BONUS GRIS ---
    print("\n>>> BONUS 1 : Niveaux de Gris")
    img_gray = [
        [ 50,  50,  50,  50,  50],
        [ 50, 100, 100, 100,  50],
        [ 50, 100, 255, 100,  50],
        [ 50, 100, 100, 100,  50],
        [ 50,  50,  50,  50,  50]
    ]
    pretty_gray(img_gray, "Originale")
    pretty_gray(erode_gray(img_gray, strel_square(3)), "Erosion")
    pretty_gray(dilate_gray(img_gray, strel_square(3)), "Dilatation")

    # --- BONUS PGM & OTSU ---
    print("\n>>> BONUS 2 : PGM & Otsu")
    
    # Création d'une image test et sauvegarde
    img_syn = zeros(10, 10, 50)
    for y in range(3, 7):
        for x in range(3, 7): img_syn[y][x] = 200
    
    save_pgm(img_syn, "test_input.pgm")
    
    # Lecture + Otsu
    img_lue = load_pgm("test_input.pgm")
    thr = otsu_threshold(img_lue)
    print(f"Seuil Otsu trouvé : {thr}")
    
    img_final = apply_threshold(img_lue, thr)
    pretty_bin(img_final, "Résultat Binarisé")
    
    # Sauvegarde résultat
    save_pgm([[v*255 for v in row] for row in img_final], "test_result.pgm")
    
    print("\n=== TP TERMINÉ AVEC SUCCÈS ===")