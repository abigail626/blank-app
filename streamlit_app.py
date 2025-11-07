import streamlit as st
import random

st.set_page_config(page_title="무지개 뽑기", page_icon="🌈", layout="centered")

# 색 정의: (한국어 이름, hex)
COLORS = [
    ("빨강", "#FF0000"),
    ("주황", "#FF7F00"),
    ("노랑", "#FFFF00"),
    ("초록", "#00CC44"),
    ("파랑", "#0000FF"),
    ("남색", "#4B0082"),
    ("보라", "#8A2BE2"),
]

def hex_to_rgb(hex_color: str):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def readable_text_color(hex_color: str) -> str:
    # 밝기 계산: 단순한 Y' (luma) 계산으로 흰/검정 결정
    r, g, b = hex_to_rgb(hex_color)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "#000000" if luminance > 180 else "#FFFFFF"

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🌈 무지개 뽑기")
st.write("아래에서 한 번 눌러서 빨주노초파남보 중 하나를 랜덤으로 뽑아보세요!")

# 옵션: 몇 개 뽑을지
count = st.number_input("몇 개를 뽑을까요?", min_value=1, max_value=7, value=1, step=1)

col1, col2 = st.columns([2, 1])
with col1:
    if st.button("🎲 뽑기!"):
        picks = [random.choice(COLORS) for _ in range(count)]
        # history에 추가 (가장 최근이 맨 앞)
        for p in picks:
            st.session_state.history.insert(0, p)
        # 화면에 결과 표시
        for name, hexc in picks:
            text_color = readable_text_color(hexc)
            st.markdown(
                f"<div style='background:{hexc}; color:{text_color}; padding:30px; border-radius:12px; text-align:center; font-size:28px; margin:10px 0'>{name}</div>",
                unsafe_allow_html=True,
            )

with col2:
    if st.button("♻️ 초기화"):
        st.session_state.history = []
        st.experimental_rerun()

st.markdown("---")
st.subheader("최근 뽑기 이력")
if not st.session_state.history:
    st.info("아직 뽑은 내역이 없습니다. '뽑기!'를 눌러보세요.")
else:
    # 이력 표시는 가볍게 상자 형태로 보여줌
    for idx, (name, hexc) in enumerate(st.session_state.history[:20], start=1):
        text_color = readable_text_color(hexc)
        st.markdown(
            f"<div style='display:flex;align-items:center;margin:6px 0'>"
            f"<div style='width:36px;height:24px;background:{hexc};border-radius:4px;margin-right:10px;'></div>"
            f"<div style='flex:1;font-weight:600'>{idx}. {name}</div>"
            f"<div style='color:#666;font-size:12px;margin-left:8px'>{hexc}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption("원하면 색 이름 대신 영어/이모지 추가, 효과음, 애니메이션 등 더 개선해드릴게요.")