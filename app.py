
import random
from collections import deque

import streamlit as st

st.set_page_config(page_title="지뢰찾기", page_icon="💣", layout="centered")

LEVELS = {
    "초급": (9, 9, 10),
    "중급": (12, 12, 25),
    "고급": (16, 16, 45),
}


def new_game(level):
    rows, cols, mine_count = LEVELS[level]
    mines = set(random.sample(range(rows * cols), mine_count))
    numbers = {}

    for i in range(rows * cols):
        r, c = divmod(i, cols)
        numbers[i] = sum(
            (nr * cols + nc) in mines
            for nr in range(max(0, r - 1), min(rows, r + 2))
            for nc in range(max(0, c - 1), min(cols, c + 2))
            if (nr, nc) != (r, c)
        )

    st.session_state.game = {
        "level": level,
        "rows": rows,
        "cols": cols,
        "mines": mines,
        "numbers": numbers,
        "revealed": set(),
        "flags": set(),
        "over": False,
        "won": False,
    }


def reveal(game, start):
    queue = deque([start])

    while queue:
        i = queue.popleft()

        if i in game["revealed"] or i in game["flags"]:
            continue

        if i in game["mines"]:
            game["over"] = True
            game["won"] = False
            game["revealed"].add(i)
            return

        game["revealed"].add(i)

        if game["numbers"][i] == 0:
            r, c = divmod(i, game["cols"])

            for nr in range(max(0, r - 1), min(game["rows"], r + 2)):
                for nc in range(max(0, c - 1), min(game["cols"], c + 2)):
                    neighbor = nr * game["cols"] + nc

                    if neighbor not in game["revealed"]:
                        queue.append(neighbor)

    safe_cells = game["rows"] * game["cols"] - len(game["mines"])
    if len(game["revealed"]) == safe_cells:
        game["over"] = True
        game["won"] = True


st.title("💣 지뢰찾기")
st.caption("지뢰를 피해 모든 안전한 칸을 열어 보세요!")

if "game" not in st.session_state:
    new_game("초급")

game = st.session_state.game

level = st.selectbox(
    "난이도 선택",
    list(LEVELS.keys()),
    index=list(LEVELS.keys()).index(game["level"]),
)

if level != game["level"]:
    new_game(level)
    st.rerun()

if st.button("🔄 새 게임", use_container_width=True):
    new_game(level)
    st.rerun()

flag_mode = st.toggle("🚩 깃발 모드", value=False)

remaining = len(game["mines"]) - len(game["flags"])
st.metric("남은 지뢰 수 (깃발 기준)", remaining)

if game["over"]:
    if game["won"]:
        st.success("🎉 승리! 모든 안전한 칸을 열었어요!")
    else:
        st.error("💥 지뢰를 밟았어요! 새 게임을 시작해 보세요.")

for r in range(game["rows"]):
    columns = st.columns(game["cols"], gap="small")

    for c in range(game["cols"]):
        i = r * game["cols"] + c
        is_revealed = i in game["revealed"]
        is_flagged = i in game["flags"]

        if is_revealed:
            if i in game["mines"]:
                label = "💥"
            else:
                n = game["numbers"][i]
                label = str(n) if n else "·"
        else:
            label = "🚩" if is_flagged else "⬜"

        if game["over"] and i in game["mines"] and not is_revealed:
            label = "💣"

        disabled = game["over"] or is_revealed

        if columns[c].button(
            label,
            key=f"cell_{r}_{c}",
            disabled=disabled,
            use_container_width=True,
        ):
            if flag_mode:
                if i in game["flags"]:
                    game["flags"].remove(i)
                else:
                    game["flags"].add(i)
            elif i not in game["flags"]:
                reveal(game, i)

            st.rerun()

st.caption("깃발을 놓으려면 깃발 모드를 켜고 칸을 누르세요.")
