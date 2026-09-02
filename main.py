import random
import time
import streamlit as st

st.set_page_config(
    page_title="HIDE - 픽셀 생존 게임",
    page_icon="👻",
    layout="centered",
)

MAP_W = 13
MAP_H = 9

MAP = [
    "#############",
    "#...........#",
    "#..C........#",
    "#...........#",
    "#.....##....#",
    "#........C..#",
    "#...........#",
    "#E..........#",
    "#############",
]

FLOOR = {
    (x, y)
    for y, row in enumerate(MAP)
    for x, tile in enumerate(row)
    if tile != "#"
}

CABINETS = {
    (x, y)
    for y, row in enumerate(MAP)
    for x, tile in enumerate(row)
    if tile == "C"
}

EXIT = next(
    ((x, y) for y, row in enumerate(MAP) for x, tile in enumerate(row) if tile == "E"),
    None
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #11131a;
}

.block-container {
    max-width: 900px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.pixel-title {
    font-family: monospace;
    font-weight: 900;
    font-size: 38px;
    letter-spacing: 5px;
    text-align: center;
    color: #f5f5f5;
    text-shadow: 4px 4px 0 #4b4f60;
    margin-bottom: 0.1rem;
}

.subtitle {
    text-align: center;
    color: #aeb4c5;
    font-family: monospace;
    margin-bottom: 1.2rem;
}

.card {
    background: #1b1e29;
    border: 3px solid #343949;
    border-radius: 10px;
    padding: 18px;
    box-shadow: 0 6px 0 #0a0b0f;
}

.map-wrap {
    display: flex;
    justify-content: center;
    margin: 10px 0 16px 0;
}

.map {
    display: grid;
    grid-template-columns: repeat(13, 34px);
    grid-template-rows: repeat(9, 34px);
    gap: 2px;
    background: #0b0d12;
    padding: 6px;
    border: 4px solid #303442;
    image-rendering: pixelated;
}

.tile {
    width: 34px;
    height: 34px;
    position: relative;
    box-sizing: border-box;
}

.wall {
    background: #3a3e4b;
    border: 2px solid #555a6b;
}

.floor {
    background: #747b67;
    border: 1px solid #666d5b;
}

.exit {
    background: #59657d;
    border: 2px solid #91a3c7;
}

.cabinet {
    background: #8c5b46;
    border: 3px solid #5d392d;
}

.cabinet-icon {
    text-align: center;
    font-size: 22px;
    line-height: 34px;
}

.player {
    position: absolute;
    width: 22px;
    height: 25px;
    left: 6px;
    top: 5px;
    border-radius: 4px;
    border: 2px solid #20232b;
    box-shadow: 2px 2px 0 #252833;
}

.player.male {
    background: linear-gradient(#5aa5e8 0 42%, #26334f 42% 100%);
}

.player.female {
    background: linear-gradient(#ef8eb2 0 42%, #4a3858 42% 100%);
}

.player::before {
    content: "";
    position: absolute;
    width: 12px;
    height: 9px;
    left: 3px;
    top: -7px;
    background: #f2c7a5;
    border: 2px solid #20232b;
    border-radius: 3px;
}

.monster {
    position: absolute;
    width: 23px;
    height: 24px;
    left: 5px;
    top: 5px;
    background: #a65c9c;
    border: 2px solid #34213a;
    border-radius: 7px 7px 3px 3px;
}

.monster::before,
.monster::after {
    content: "";
    position: absolute;
    width: 4px;
    height: 4px;
    background: #f8eeee;
    top: 5px;
}

.monster::before {
    left: 4px;
}

.monster::after {
    right: 4px;
}

.stat {
    background: #12141b;
    border: 2px solid #303544;
    padding: 8px 10px;
    border-radius: 6px;
    font-family: monospace;
    color: #dce1ee;
    margin-bottom: 8px;
}

.big-key {
    font-family: monospace;
    font-size: 80px;
    font-weight: 900;
    text-align: center;
    color: #ffffff;
    text-shadow: 6px 6px 0 #555b70;
    padding: 20px;
    border: 5px solid #555b70;
    background: #242836;
    border-radius: 12px;
    margin: 12px 0;
}

.warning {
    text-align: center;
    font-family: monospace;
    font-weight: 900;
    color: #ffb4b4;
    font-size: 20px;
}

.gameover {
    text-align: center;
    font-family: monospace;
    font-size: 42px;
    font-weight: 900;
    color: #ff8d8d;
    text-shadow: 4px 4px 0 #4b2020;
    padding: 20px;
}

.clear {
    text-align: center;
    font-family: monospace;
    font-size: 38px;
    font-weight: 900;
    color: #ffe58a;
    text-shadow: 4px 4px 0 #594a20;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)


def reset_game(gender="male"):
    st.session_state.gender = gender
    st.session_state.player = [1, 7]
    st.session_state.monster = [11, 1]
    st.session_state.mode = "explore"
    st.session_state.hp = 3
    st.session_state.noise = 0
    st.session_state.target_key = random.choice("WASD")
    st.session_state.hide_until = 0.0
    st.session_state.hide_total = 10.0
    st.session_state.hide_started = 0.0
    st.session_state.message = (
        "학교 안을 탐색해 보자. 캐비닛은 위험할 때 숨을 수 있는 장소다."
    )


if "mode" not in st.session_state:
    st.session_state.mode = "start"


# =============================
# 시작 화면
# =============================

if st.session_state.mode == "start":

    st.markdown(
        '<div class="pixel-title">H I D E</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">PIXEL SURVIVAL ADVENTURE</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">
        <h3 style="text-align:center;">캐릭터를 선택하세요</h3>

        <p style="text-align:center;color:#aeb4c5;">
        학교를 탐험하다 괴물에게 쫓기면 캐비닛에 숨으세요.<br>
        숨어 있는 동안 나타나는 W / A / S / D를 맞혀 살아남으세요!
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="card" style="text-align:center;">
            <div style="font-size:64px;">🧑🏻‍🎓</div>
            <h3>남학생</h3>
            <p style="color:#9ebee8;">파란 교복</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("남학생으로 시작", use_container_width=True):
            reset_game("male")
            st.rerun()

    with col2:

        st.markdown("""
        <div class="card" style="text-align:center;">
            <div style="font-size:64px;">👩🏻‍🎓</div>
            <h3>여학생</h3>
            <p style="color:#e8a4c0;">분홍빛 교복</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("여학생으로 시작", use_container_width=True):
            reset_game("female")
            st.rerun()

    st.stop()


# =============================
# GAME OVER
# =============================

if st.session_state.mode == "gameover":

    st.markdown(
        '<div class="gameover">GAME OVER</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="text-align:center;color:#aeb4c5;font-family:monospace;">'
        '괴물에게 발각되었습니다.</p>',
        unsafe_allow_html=True
    )

    if st.button("다시 시작", use_container_width=True):
        reset_game(st.session_state.gender)
        st.rerun()

    st.stop()


# =============================
# CLEAR
# =============================

if st.session_state.mode == "clear":

    st.markdown(
        '<div class="clear">ESCAPED!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="text-align:center;color:#aeb4c5;font-family:monospace;">'
        '학교를 빠져나오는 데 성공했습니다!</p>',
        unsafe_allow_html=True
    )

    if st.button("다시 플레이", use_container_width=True):
        reset_game(st.session_state.gender)
        st.rerun()

    st.stop()


# =============================
# 이동
# =============================

def enter_hide():

    st.session_state.mode = "hide"
    st.session_state.hide_started = time.time()
    st.session_state.hide_until = time.time() + 10.0
    st.session_state.hide_total = 10.0
    st.session_state.target_key = random.choice("WASD")
    st.session_state.message = "숨었다! 들키지 않으려면 화면의 키를 빠르게 입력하자."


def move_player(dx, dy):

    x, y = st.session_state.player

    nx = x + dx
    ny = y + dy

    if (nx, ny) not in FLOOR:
        st.session_state.message = "벽이다."
        return

    st.session_state.player = [nx, ny]

    st.session_state.noise = min(
        100,
        st.session_state.noise + 4
    )

    st.session_state.message = "발소리가 났다..."

    mx, my = st.session_state.monster

    if random.random() < 0.75:

        options = []

        if nx > mx and (mx + 1, my) in FLOOR:
            options.append((mx + 1, my))

        if nx < mx and (mx - 1, my) in FLOOR:
            options.append((mx - 1, my))

        if ny > my and (mx, my + 1) in FLOOR:
            options.append((mx, my + 1))

        if ny < my and (mx, my - 1) in FLOOR:
            options.append((mx, my - 1))

        if options:
            st.session_state.monster = list(
                random.choice(options)
            )

    if st.session_state.player == st.session_state.monster:
        enter_hide()


def hide_success():

    st.session_state.mode = "explore"

    st.session_state.monster = [11, 1]

    st.session_state.player = [1, 7]

    st.session_state.noise = max(
        0,
        st.session_state.noise - 30
    )

    st.session_state.message = (
        "괴물이 지나갔다. 이제 조용히 출구를 찾아보자."
    )


# =============================
# 탐험
# =============================

if st.session_state.mode == "explore":

    st.markdown(
        '<div class="pixel-title">H I D E</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f'<div class="stat">'
            f'♥ HP: {"♥" * st.session_state.hp}'
            f'</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="stat">'
            f'🔊 소음: {st.session_state.noise}%'
            f'</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="stat">📍 학교 1층</div>',
            unsafe_allow_html=True
        )

    px, py = st.session_state.player
    mx, my = st.session_state.monster

    cells = []

    for y, row in enumerate(MAP):

        for x, tile in enumerate(row):

            if tile == "#":
                cls = "wall"
            else:
                cls = "floor"

            inner = ""

            if tile == "E":

                cls = "exit"

                inner = (
                    '<div style="text-align:center;'
                    'line-height:34px;">🚪</div>'
                )

            if tile == "C":

                cls = "cabinet"

                inner = (
                    '<div class="cabinet-icon">▣</div>'
                )

            if [x, y] == [mx, my]:

                inner = '<div class="monster"></div>'

            if [x, y] == [px, py]:

                inner = (
                    f'<div class="player '
                    f'{st.session_state.gender}"></div>'
                )

            cells.append(
                f'<div class="tile {cls}">{inner}</div>'
            )

    map_html = (
        '<div class="map-wrap">'
        '<div class="map">'
        + "".join(cells)
        + "</div></div>"
    )

    st.markdown(
        map_html,
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div style="text-align:center;'
        f'color:#c4cad8;font-family:monospace;">'
        f'{st.session_state.message}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        '<div style="text-align:center;'
        'font-family:monospace;">MOVE</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with b:

        if st.button("▲", use_container_width=True):
            move_player(0, -1)
            st.rerun()

    a, b, c = st.columns(3)

    with a:

        if st.button("◀", use_container_width=True):
            move_player(-1, 0)
            st.rerun()

    with b:

        if st.button("▼", use_container_width=True):
            move_player(0, 1)
            st.rerun()

    with c:

        if st.button("▶", use_container_width=True):
            move_player(1, 0)
            st.rerun()

    if tuple(st.session_state.player) in CABINETS:

        st.write("")

        if st.button(
            "🗄️ 캐비닛에 숨기",
            use_container_width=True
        ):
            enter_hide()
            st.rerun()

    if st.session_state.player == list(EXIT):

        st.write("")

        if st.button(
            "🚪 출구로 나가기",
            use_container_width=True
        ):
            st.session_state.mode = "clear"
            st.rerun()

    st.caption(
        "팁: 괴물이 가까워지면 캐비닛으로 도망가세요."
    )


# =============================
# 캐비닛 숨기 미니게임
# =============================

elif st.session_state.mode == "hide":

    remaining = max(
        0.0,
        st.session_state.hide_until - time.time()
    )

    if remaining <= 0:

        hide_success()
        st.rerun()

    st.markdown(
        '<div class="pixel-title">H I D E</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="warning">'
        '쉿... 괴물이 캐비닛 앞에 있다.'
        '</div>',
        unsafe_allow_html=True
    )

    progress = (
        remaining /
        st.session_state.hide_total
    )

    st.progress(progress)

    st.markdown(
        f'<div style="text-align:center;'
        f'color:#bfc5d5;font-family:monospace;">'
        f'남은 시간: {remaining:.1f}초'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="big-key">'
        f'{st.session_state.target_key}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="text-align:center;'
        'color:#aeb4c5;font-family:monospace;">'
        '화면의 키를 눌러 숨은 상태를 유지하세요!'
        '</p>',
        unsafe_allow_html=True
    )

    keys = st.columns(4)

    for i, key in enumerate("WASD"):

        with keys[i]:

            if st.button(
                key,
                use_container_width=True,
                key=f"hide_{key}_{st.session_state.target_key}"
            ):

                if key == st.session_state.target_key:

                    st.session_state.target_key = random.choice(
                        "WASD"
                    )

                    st.session_state.hide_until = min(
                        st.session_state.hide_until + 0.15,
                        st.session_state.hide_started + 10.0
                    )

                else:

                    st.session_state.hp -= 1

                    st.session_state.message = (
                        "잘못된 버튼! 캐비닛이 흔들렸다."
                    )

                    st.session_state.target_key = random.choice(
                        "WASD"
                    )

                    st.session_state.hide_until -= 1.2

                    if st.session_state.hp <= 0:
                        st.session_state.mode = "gameover"

                st.rerun()

    st.write("")

    st.caption(
        "실수하면 생존 시간이 크게 줄어듭니다. "
        "0초까지 버티면 탈출 성공!"
    )

    time.sleep(0.08)

    st.rerun()
