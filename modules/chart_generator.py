"""
真圓環圖表生成模組（雲端版）
- 字型用 Noto Sans CJK TC（Streamlit Cloud 透過 packages.txt 安裝）
- 字型 fallback 鏈：Noto → 微軟正黑 → PingFang → DejaVu
"""
import io
import math
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 字型 fallback：雲端用 Noto，本機 Windows 用微軟正黑體
plt.rcParams["font.family"] = [
    "Noto Sans CJK TC",
    "Noto Sans TC",
    "Microsoft JhengHei",
    "PingFang TC",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False


COLORS = {
    "bg":       "#000000",
    "card":     "#0F0F14",
    "ring_bg":  "#1F1F28",
    "text":     "#FFFFFF",
    "text_dim": "#888888",
    "bull":     "#FBBF24",
    "bear":     "#EF4444",
    "wait":     "#888888",
    "brand":    "#A855F7",
}


def _圖to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=COLORS["bg"],
                bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def _依分數取色(score: float, 滿分: float = 100,
                  bull_threshold: float = 70, wait_threshold: float = 40) -> str:
    pct = (score / 滿分) * 100
    if pct >= bull_threshold:
        return COLORS["bull"]
    if pct >= wait_threshold:
        return "#F59E0B"
    return COLORS["bear"]


def 生成Enjoy圓環(score: float, status: str = "HOLD",
                    副標: str = "Enjoy Index") -> bytes:
    色 = _依分數取色(score)
    fig, ax = plt.subplots(figsize=(7, 7), dpi=120)
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)

    ax.add_patch(patches.Wedge((0, 0), 1.0, 0, 360, width=0.18,
                                facecolor=COLORS["ring_bg"], edgecolor="none"))
    end_angle = 90 - (score / 100) * 360
    if end_angle < -270:
        end_angle = -270
    ax.add_patch(patches.Wedge((0, 0), 1.0, end_angle, 90, width=0.18,
                                facecolor=色, edgecolor="none"))

    end_rad = math.radians(end_angle)
    ax.add_patch(patches.Circle(
        (0.91 * math.cos(end_rad), 0.91 * math.sin(end_rad)),
        0.04, facecolor=色, edgecolor="white", linewidth=1.5, zorder=10))

    ax.text(0,  0.30, 副標, ha="center", va="center",
            fontsize=14, color=COLORS["text_dim"])
    ax.text(0, -0.02, f"{score}", ha="center", va="center",
            fontsize=72, color=色, fontweight="bold")
    ax.text(0, -0.30, "/ 100", ha="center", va="center",
            fontsize=14, color=COLORS["text_dim"])
    乾淨status = status.lstrip("🔴🟢🟡⚪ ").strip()
    ax.text(0, -0.50, 乾淨status, ha="center", va="center",
            fontsize=20, color=色, fontweight="bold")
    return _圖to_bytes(fig)


def 生成資金規劃圓環(火力比例: int, 子彈金額: float, 建議: str) -> bytes:
    色 = (COLORS["bull"] if 建議 == "BE HAPPY"
          else "#F59E0B" if 建議 == "WAIT"
          else COLORS["bear"])
    fig, ax = plt.subplots(figsize=(7, 7), dpi=120)
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.add_patch(patches.Wedge((0, 0), 1.0, 0, 360, width=0.18,
                                facecolor=COLORS["ring_bg"], edgecolor="none"))
    end_angle = 90 - (火力比例 / 100) * 360
    ax.add_patch(patches.Wedge((0, 0), 1.0, end_angle, 90, width=0.18,
                                facecolor=色, edgecolor="none"))
    ax.text(0,  0.35, "今日子彈", ha="center", va="center",
            fontsize=14, color=COLORS["text_dim"])
    ax.text(0,  0.05, f"NT$ {子彈金額:,.0f}", ha="center", va="center",
            fontsize=30, color=色, fontweight="bold")
    ax.text(0, -0.25, f"火力 {火力比例}%", ha="center", va="center",
            fontsize=16, color=COLORS["text_dim"])
    ax.text(0, -0.50, 建議, ha="center", va="center",
            fontsize=18, color=色, fontweight="bold")
    return _圖to_bytes(fig)
