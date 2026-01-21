from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    raw_dir: Path
    processed_dir: Path
    reports_dir: Path
    figures_dir: Path


def get_paths() -> ProjectPaths:
    root = Path(__file__).resolve().parents[1]
    raw_dir = root / "raw"
    processed_dir = root / "data" / "processed"
    reports_dir = root / "reports"
    figures_dir = reports_dir / "figures"
    return ProjectPaths(
        root=root,
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        reports_dir=reports_dir,
        figures_dir=figures_dir,
    )


def ensure_dirs() -> ProjectPaths:
    paths = get_paths()
    paths.processed_dir.mkdir(parents=True, exist_ok=True)
    paths.reports_dir.mkdir(parents=True, exist_ok=True)
    paths.figures_dir.mkdir(parents=True, exist_ok=True)
    return paths


def _build_daily_orders_from_raw(raw_path: Path) -> pd.DataFrame:
    df = pd.read_csv(raw_path)
    if "order_purchase_timestamp" not in df.columns:
        raise ValueError("order_purchase_timestamp column not found in raw orders dataset")
    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"], errors="coerce"
    )
    df = df.dropna(subset=["order_purchase_timestamp"])
    if "order_status" in df.columns:
        df = df[~df["order_status"].isin(["canceled", "unavailable"])]
    df["date"] = df["order_purchase_timestamp"].dt.date
    daily = (
        df.groupby("date", as_index=False)
        .size()
        .rename(columns={"size": "orders"})
    )
    daily["date"] = pd.to_datetime(daily["date"])
    return daily.sort_values("date")


def load_orders_daily(path: Optional[Path] = None) -> pd.DataFrame:
    paths = ensure_dirs()
    daily_path = path or (paths.processed_dir / "orders_daily.csv")
    if daily_path.exists():
        daily = pd.read_csv(daily_path, parse_dates=["date"])
    else:
        raw_path = paths.raw_dir / "olist_orders_dataset.csv"
        if not raw_path.exists():
            raise FileNotFoundError(
                f"Missing {daily_path} and raw orders file {raw_path}"
            )
        daily = _build_daily_orders_from_raw(raw_path)
        daily.to_csv(daily_path, index=False)
    if "orders" not in daily.columns:
        raise ValueError("orders column missing in daily orders data")
    daily = daily.sort_values("date")
    daily["orders"] = pd.to_numeric(daily["orders"], errors="coerce")
    daily = daily.dropna(subset=["orders"])
    return daily


def save_figure(fig, filename: str) -> Path:
    paths = ensure_dirs()
    output_path = paths.figures_dir / filename
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    return output_path


def mape(actual: np.ndarray, forecast: np.ndarray) -> float:
    actual = np.asarray(actual, dtype=float)
    forecast = np.asarray(forecast, dtype=float)
    mask = actual != 0
    if not mask.any():
        return float("nan")
    return np.mean(np.abs((actual[mask] - forecast[mask]) / actual[mask])) * 100

