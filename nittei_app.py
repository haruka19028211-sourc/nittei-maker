import streamlit as st
import datetime

# ===== ページの基本設定 =====
st.set_page_config(page_title="日程調整メーカー", page_icon="📅")

st.title("📅 日程調整メーカー")
st.write("候補の日付と時間を選ぶと、コピーできる定型文を作ります。")

# ===== セッション（選んだ候補を覚えておく箱）=====
# Streamlitは画面を再描画するたびに変数が消えるので、
# 「session_state」という消えない箱に候補リストを保存する
if "kouho" not in st.session_state:
    st.session_state.kouho = []

# ===== 入力エリア =====
st.subheader("① 候補を追加する")

col1, col2, col3 = st.columns(3)

with col1:
    hizuke = st.date_input("日付", datetime.date.today())

with col2:
    kaishi = st.time_input("開始時刻", datetime.time(10, 0))

with col3:
    shuryo = st.time_input("終了時刻", datetime.time(12, 0))

# 終日チェック
syujitsu = st.checkbox("終日（時間を指定しない）")

# 追加ボタン
if st.button("➕ この候補を追加"):
    st.session_state.kouho.append({
        "日付": hizuke,
        "開始": kaishi,
        "終了": shuryo,
        "終日": syujitsu,
    })

# ===== 追加済みの候補を表示 =====
st.subheader("② 追加された候補")

if len(st.session_state.kouho) == 0:
    st.info("まだ候補がありません。上で追加してください。")
else:
    # 曜日を日本語にするためのリスト（月曜=0）
    youbi = ["月", "火", "水", "木", "金", "土", "日"]

    for i, k in enumerate(st.session_state.kouho):
        d = k["日付"]
        w = youbi[d.weekday()]
        if k["終日"]:
            text = f"{d.month}月{d.day}日（{w}）　終日"
        else:
            text = (f"{d.month}月{d.day}日（{w}）　"
                    f"{k['開始'].strftime('%H:%M')}〜{k['終了'].strftime('%H:%M')}")

        c1, c2 = st.columns([5, 1])
        c1.write(f"・{text}")
        if c2.button("削除", key=f"del_{i}"):
            st.session_state.kouho.pop(i)
            st.rerun()

    # ===== 定型文の生成 =====
    st.subheader("③ コピー用の文面")

    youbi = ["月", "火", "水", "木", "金", "土", "日"]
    lines = ["以下の日程でご都合いかがでしょうか。", ""]
    for k in st.session_state.kouho:
        d = k["日付"]
        w = youbi[d.weekday()]
        if k["終日"]:
            lines.append(f"{d.month}月{d.day}日（{w}）　終日")
        else:
            lines.append(f"{d.month}月{d.day}日（{w}）　"
                         f"{k['開始'].strftime('%H:%M')}〜{k['終了'].strftime('%H:%M')}")

    moji = "\n".join(lines)

    # コピーしやすいテキストエリアで表示
    st.text_area("この文章をコピーしてください", moji, height=200)

    # 全部リセット
    if st.button("🗑 すべてリセット"):
        st.session_state.kouho = []
        st.rerun()
