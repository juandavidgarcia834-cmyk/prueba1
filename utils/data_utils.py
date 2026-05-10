import os

import pandas as pd
import streamlit as st

from config.constants import (
    CSV_PATH, CSV_COLS,
    SEG_CSV_PATH, SEG_COLS,
    CATALOGO_PATH,
)


def load_historial() -> pd.DataFrame:
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame(columns=CSV_COLS)
    try:
        df = pd.read_csv(CSV_PATH, dtype=str)
        for col in CSV_COLS:
            if col not in df.columns:
                df[col] = ""
        df["tipo_seguimiento"] = df["tipo_seguimiento"].fillna("RUTAS").replace("", "RUTAS")
        for col in ["volumen_declarado", "vol_estaciones", "diferencia", "num_estaciones"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        for col in ["solidos_ruta", "crioscopia_ruta", "st_pond", "ic_pond",
                    "st_carrotanque", "grasa_muestra", "proteina_muestra", "diferencia_solidos"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        if "fecha" in df.columns:
            df["_fecha_dt"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y", errors="coerce")
        return df
    except Exception:
        return pd.DataFrame(columns=CSV_COLS)


def save_ruta_to_csv(row: dict):
    if os.path.exists(CSV_PATH):
        df = load_historial()
        if "_fecha_dt" in df.columns:
            df = df.drop(columns=["_fecha_dt"])
    else:
        df = pd.DataFrame(columns=CSV_COLS)
    for col in CSV_COLS:
        if col not in df.columns:
            df[col] = ""
    new_row = pd.DataFrame([{k: row.get(k, "") for k in CSV_COLS}])
    df = pd.concat([df[CSV_COLS], new_row], ignore_index=True)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")


def load_seguimientos() -> pd.DataFrame:
    if not os.path.exists(SEG_CSV_PATH):
        return pd.DataFrame(columns=SEG_COLS)
    try:
        df = pd.read_csv(SEG_CSV_PATH, dtype=str)
        for col in SEG_COLS:
            if col not in df.columns:
                df[col] = ""
        for col in ["seg_grasa", "seg_st", "seg_ic", "seg_agua"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        if "sub_tipo_seguimiento" in df.columns:
            df["sub_tipo_seguimiento"] = df["sub_tipo_seguimiento"].replace("TERCEROS", "ESTACIONES")
        if "fecha" in df.columns:
            df["_fecha_dt"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y", errors="coerce")
        return df
    except Exception:
        return pd.DataFrame(columns=SEG_COLS)


@st.cache_data(ttl=300)
def load_catalogo() -> pd.DataFrame:
    """Carga el catálogo de estaciones. Retorna DataFrame vacío si no existe."""
    if not os.path.exists(CATALOGO_PATH):
        return pd.DataFrame(columns=["codigo", "nombre", "asesor"])
    try:
        df = pd.read_csv(CATALOGO_PATH, dtype=str)
        df["codigo"] = df["codigo"].str.strip()
        df["nombre"] = df["nombre"].str.strip().str.upper()
        if "asesor" not in df.columns:
            df["asesor"] = ""
        df["asesor"] = df["asesor"].fillna("").str.strip()
        return df.dropna(subset=["codigo", "nombre"])
    except Exception:
        return pd.DataFrame(columns=["codigo", "nombre", "asesor"])


def save_catalogo(df: pd.DataFrame):
    """Guarda el catálogo de estaciones asegurando el orden de columnas."""
    for col in ["codigo", "nombre", "asesor"]:
        if col not in df.columns:
            df[col] = ""
    df[["codigo", "nombre", "asesor"]].to_csv(CATALOGO_PATH, index=False)


def save_seguimiento_to_csv(row: dict):
    if os.path.exists(SEG_CSV_PATH):
        df = load_seguimientos()
        if "_fecha_dt" in df.columns:
            df = df.drop(columns=["_fecha_dt"])
    else:
        df = pd.DataFrame(columns=SEG_COLS)
    for col in SEG_COLS:
        if col not in df.columns:
            df[col] = ""
    new_row = pd.DataFrame([{k: row.get(k, "") for k in SEG_COLS}])
    df = pd.concat([df[SEG_COLS], new_row], ignore_index=True)
    df.to_csv(SEG_CSV_PATH, index=False, encoding="utf-8")


def delete_seg_row(orig_idx: int):
    df = load_seguimientos()
    df = df.drop(index=orig_idx)
    if "_fecha_dt" in df.columns:
        df = df.drop(columns=["_fecha_dt"])
    df[SEG_COLS].to_csv(SEG_CSV_PATH, index=False, encoding="utf-8")


def delete_seg_rows(orig_indices: list):
    df = load_seguimientos()
    df = df.drop(index=[i for i in orig_indices if i in df.index])
    if "_fecha_dt" in df.columns:
        df = df.drop(columns=["_fecha_dt"])
    df[SEG_COLS].to_csv(SEG_CSV_PATH, index=False, encoding="utf-8")


def update_seg_row_in_csv(orig_idx: int, new_vals: dict):
    df = load_seguimientos()
    for k, v in new_vals.items():
        if k in df.columns:
            try:
                if pd.api.types.is_numeric_dtype(df[k].dtype):
                    df.at[orig_idx, k] = v
                else:
                    df.at[orig_idx, k] = str(v) if v is not None and v != "" else ""
            except Exception:
                df.at[orig_idx, k] = str(v) if v is not None else ""
    if "_fecha_dt" in df.columns:
        df = df.drop(columns=["_fecha_dt"])
    df[SEG_COLS].to_csv(SEG_CSV_PATH, index=False, encoding="utf-8")


def delete_row_from_csv(orig_idx: int):
    df = load_historial()
    df = df.drop(index=orig_idx)
    if "_fecha_dt" in df.columns:
        df = df.drop(columns=["_fecha_dt"])
    df[CSV_COLS].to_csv(CSV_PATH, index=False, encoding="utf-8")


def delete_rows_from_csv(orig_indices: list):
    df = load_historial()
    df = df.drop(index=[i for i in orig_indices if i in df.index])
    if "_fecha_dt" in df.columns:
        df = df.drop(columns=["_fecha_dt"])
    df[CSV_COLS].to_csv(CSV_PATH, index=False, encoding="utf-8")


def update_row_in_csv(orig_idx: int, new_vals: dict):
    df = load_historial()
    for k, v in new_vals.items():
        if k in df.columns:
            df.at[orig_idx, k] = v
    if "_fecha_dt" in df.columns:
        df = df.drop(columns=["_fecha_dt"])
    df[CSV_COLS].to_csv(CSV_PATH, index=False, encoding="utf-8")
