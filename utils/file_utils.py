import os
import re

from config.constants import FOTOS_DIR
from utils.time_utils import now_col


def save_fotos_to_disk(uploaded_files: list, prefix: str) -> list:
    """Guarda imágenes en FOTOS_DIR y retorna la lista de rutas relativas."""
    saved = []
    if not uploaded_files:
        return saved
    ts = now_col().strftime("%Y%m%d_%H%M%S")
    safe_prefix = re.sub(r"[^A-Z0-9_\-]", "_", prefix.upper())
    for i, uf in enumerate(uploaded_files, start=1):
        ext = uf.name.rsplit(".", 1)[-1].lower()
        ext = ext if ext in ("jpg", "jpeg", "png") else "jpg"
        fname = f"{safe_prefix}_{ts}_{i}.{ext}"
        fpath = os.path.join(FOTOS_DIR, fname)
        uf.seek(0)
        with open(fpath, "wb") as fh:
            fh.write(uf.read())
        uf.seek(0)
        saved.append(fpath)
    return saved
