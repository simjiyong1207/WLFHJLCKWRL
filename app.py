
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Neon Minesweeper",
    page_icon="💣",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GAME_HTML = r"""
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
:root {
  --bg:#090e1b;
  --panel:#111a2d;
  --text:#edf4ff;
  --muted:#91a4c3;
  --cyan:#5ce1e6;
  --red:#ff5577;
}
* { box-sizing:border-box; }
body {
  margin:0;
  padding:18px;
  background:radial-gradient(ellipse at top,#172747,#0b1222 55%,#080d18);
  color:var(--text);
  font-family:system-ui,-apple-system,"Segoe UI",sans-serif;
}
.wrap { max-width:1050px; margin:auto; }
.hero {
  display:flex; justify-content:space-between;
  align-items:center; gap:14px; flex-wrap:wrap;
  margin-bottom:18px;
}
.kicker {
  color:var(--cyan); letter-spacing:.18em;
  font-size:11px; font-weight:900;
}
h1 { margin:6px 0; font-size:clamp(27px,4vw,40px); }
.subtitle { color:var(--muted); font-size:13px; }
.pill {
  border:1px solid #31506c; background:#102239;
  padding:9px 12px; border-radius:999px;
  color:#b9f7f5; font-size:12px; font-weight:800;
}
.toolbar {
  display:flex; flex-wrap:wrap; gap:9px;
  align-items:center; background:var(--panel);
  border:1px solid #263751; border-radius:16px;
  padding:12px; margin-bottom:12px;
}
select,.action {
  border:1px solid #354a69; background:#1a2941;
  color:var(--text); border-radius:10px;
  padding:10px 13px; font-weight:800;
  font-size:13px; cursor:pointer;
}
.action:hover { background:#2a4164; }
.action.primary {
  background:linear-gradient(135deg,#00a9b8,#4778ff);
  border:0; color:white;
}
.stat { margin-left:auto; display:flex; gap:8px; }
.statbox {
  min-width:85px; background:#0b1425;
  border:1px solid #253752; padding:7px 12px;
  border-radius:11px; text-align:center;
}
.statbox small {
  display:block; color:var(--muted);
  font-size:10px; font-weight:800;
}
.statbox strong { display:block; font-size:20px; }
.status {
  display:flex; align-items:center; gap:10px;
  border:1px solid #293c58; border-radius:13px;
  background:#111b2d; padding:12px;
  margin-bottom:12px; font-weight:750; font-size:13px;
}
.orb {
  width:9px; height:9px; border-radius:50%;
  background:var(--cyan); box-shadow:0 0 12px var(--cyan);
  flex:none;
}
.status.win { border-color:#1e8069; color:#a7ffe0; }
.status.lose { border-color:#9f3150; color:#ffc0ce; }
.status.lose .orb { background:var(--red); }
.board-shell {
  padding:clamp(7px,1.5vw,14px);
  background:linear-gradient(145deg,#17243b,#0d1526);
  border:1px solid #2a3d5b; border-radius:18px;
  box-shadow:0 18px 55px #0005; overflow:hidden;
}
.board {
  display:grid; gap:clamp(2px,.45vw,5px);
  width:100%; user-select:none;
}
.cell {
  display:flex; align-items:center; justify-content:center;
  min-width:0; aspect-ratio:1; padding:0;
  border:1px solid #3a4f70; border-radius:6px;
  background:linear-gradient(145deg,#2a3b59,#1b2941);
  box-shadow:inset 0 1px #ffffff12,0 2px 0 #0a1020;
  color:white; font-size:clamp(11px,2.2vw,22px);
  font-weight:950; cursor:pointer;
  transition:transform .12s,background .14s,border-color .14s;
}
.cell:not(.opened):hover {
  transform:translateY(-2px);
  border-color:#66dbe7;
  box-shadow:0 0 12px #52d8e555;
}
.cell:active { transform:scale(.94); }
.cell.opened {
  cursor:default; background:#e7eef8;
  border-color:#d4e0f0; color:#17243b;
  animation:pop .16s ease-out;
}
.cell.opened.empty { background:#cbd7e8; }
.cell.flagged {
  background:linear-gradient(145deg,#493050,#30203d);
  border-color:#a56bc0;
}
.cell.mine {
  background:linear-gradient(145deg,#ff7890,#d72f58);
  border-color:#ffb1bd; color:white;
  animation:minePop .38s ease-out;
}
.cell.exploded {
  box-shadow:0 0 0 3px #ff526f,0 0 35px #ff315f;
}
.num1{color:#1263d6!important}
.num2{color:#13814f!important}
.num3{color:#d12c42!important}
.num4{color:#5133b5!important}
.num5{color:#a34b18!important}
.num6{color:#008b98!important}
.num7{color:#1e293b!important}
.num8{color:#667085!important}

@keyframes pop {
  from {transform:scale(.78);opacity:.5}
  to {transform:scale(1);opacity:1}
}
@keyframes minePop {
  0% {transform:scale(.5) rotate(-8deg)}
  55% {transform:scale(1.16) rotate(4deg)}
  100% {transform:scale(1)}
}
@keyframes shake {
  0%,100% {transform:translateX(0)}
  20%,60% {transform:translateX(-5px)}
  40%,80% {transform:translateX(5px)}
}
@keyframes boom {
  0% {transform:translate(-50%,-50%) scale(.2);opacity:1}
  45% {transform:translate(-50%,-50%) scale(8);opacity:.9}
  100% {transform:translate(-50%,-50%) scale(13);opacity:0}
}
@keyframes confettiFall {
  to {transform:translate(var(--dx),100vh) rotate(720deg);opacity:0}
}
.shake { animation:shake .35s ease-in-out; }
.explosion {
  position:fixed; z-index:99; pointer-events:none;
  left:50%; top:44%; width:12px; height:12px;
  border-radius:50%; background:#fff6a8;
  box-shadow:0 0 20px 10px #ff6b35,0 0 55px 25px #ff315f;
  animation:boom .55s ease-out forwards;
}
.confetti {
  position:fixed; z-index:100; top:-14px;
  width:7px; height:12px; border-radius:2px;
  pointer-events:none;
  animation:confettiFall 2.3s ease-in forwards;
}
.footer {
  display:flex; justify-content:space-between;
  flex-wrap:wrap; gap:8px; color:#879bb9;
  font-size:11px; padding:12px 3px;
}
@media(max-width:560px) {
  body {padding:9px}
  .stat {margin-left:0;width:100%}
  .statbox {flex:1}
  .cell {font-size:clamp(9px,2.7vw,15px);border-radius:3px}
  .board {gap:2px}
}
@media(prefers-reduced-motion:reduce) {
  *,*::before,*::after {
    animation-duration:.01ms!important;
    transition-duration:.01ms!important;
  }
}
</style>
</head>

<body>
<div class="wrap">
  <header class="hero">
    <div>
      <div class="kicker">NEON ARCADE · CLASSIC PUZZLE</div>
      <h1>💣 Minesweeper</h1>
      <div class="subtitle">
        안전한 칸을 모두 열고 지뢰를 피해 클리어하세요.
      </div>
    </div>
    <div class="pill">✦ FIRST CLICK SAFE</div>
  </header>

  <div class="toolbar">
    <label for="level" style="font-size:12px;color:#a9bbd6;font-weight:800">
      난이도
    </label>
    <select id="level">
      <option value="easy">초급 · 9×9</option>
      <option value="medium">중급 · 12×12</option>
      <option value="hard">고급 · 16×16</option>
    </select>
    <button class="action primary" id="newGame">↻ 새 게임</button>
    <button class="action" id="hint">? 조작법</button>

    <div class="stat">
      <div class="statbox">
        <small>MINES LEFT</small>
        <strong id="mineCount">010</strong>
      </div>
      <div class="statbox">
        <small>TIME</small>
        <strong id="timer">000</strong>
      </div>
    </div>
  </div>

  <div class="status" id="status">
    <span class="orb"></span>
    <span id="statusText">첫 칸을 열어 게임을 시작하세요.</span>
  </div>

  <main class="board-shell" id="boardShell">
    <div class="board" id="board"></div>
  </main>

  <div class="footer">
    <span>🖱️ 좌클릭: 열기 · 우클릭: 깃발 · 좌+우 동시 클릭: 주변 칸 열기</span>
    <span>📱 모바일: 길게 눌러 깃발 · 열린 숫자 칸 다시 탭: 주변 칸 열기</span>
  </div>
</div>

<script>
(() => {
  const levels = {
    easy:   {rows:9, cols:9, mines:10},
    medium: {rows:12, cols:12, mines:25},
    hard:   {rows:16, cols:16, mines:45}
  };

  const $ = id => document.getElementById(id);
  let game, timerId = null, startedAt = 0, seconds = 0;
  let touchTimer = null, longPressed = false, chordHandledAt = 0, chordHandledIndex = -1;

  function startGame() {
    clearInterval(timerId);
    timerId = null;
    seconds = 0;
    startedAt = 0;

    const cfg = levels[$('level').value];

    game = {
      ...cfg,
      minesSet: new Set(),
      numbers: Array(cfg.rows * cfg.cols).fill(0),
      opened: new Set(),
      flags: new Set(),
      over: false,
      started: false,
      first: true
    };

    $('timer').textContent = '000';
    $('mineCount').textContent = String(cfg.mines).padStart(3,'0');
    setStatus('첫 칸을 열어 게임을 시작하세요.','');
    drawBoard();
  }

  function neighbors(i) {
    const r = Math.floor(i / game.cols);
    const c = i % game.cols;
    const out = [];

    for (let nr=Math.max(0,r-1); nr<=Math.min(game.rows-1,r+1); nr++) {
      for (let nc=Math.max(0,c-1); nc<=Math.min(game.cols-1,c+1); nc++) {
        if (nr!==r || nc!==c) out.push(nr*game.cols+nc);
      }
    }
    return out;
  }

  function placeMines(first) {
    // 첫 칸과 주변 8칸을 안전하게 만든다.
    const blocked = new Set([first,...neighbors(first)]);
    const candidates = [];

    for (let i=0; i<game.rows*game.cols; i++) {
      if (!blocked.has(i)) candidates.push(i);
    }

    // 난이도별 지뢰 개수를 정확히 배치한다.
    while (game.minesSet.size < game.mines) {
      const idx = Math.floor(Math.random()*candidates.length);
      game.minesSet.add(candidates.splice(idx,1)[0]);
    }

    game.numbers = game.numbers.map((_,i) =>
      game.minesSet.has(i)
        ? -1
        : neighbors(i).filter(n=>game.minesSet.has(n)).length
    );

    game.first = false;
  }

  function drawBoard() {
    const board = $('board');
    board.innerHTML = '';
    board.style.gridTemplateColumns =
      `repeat(${game.cols},minmax(0,1fr))`;

    const frag = document.createDocumentFragment();

    for (let i=0; i<game.rows*game.cols; i++) {
      const cell = document.createElement('button');
      cell.type = 'button';
      cell.className = 'cell';
      cell.dataset.index = i;

      cell.setAttribute(
        'aria-label',
        `행 ${Math.floor(i/game.cols)+1}, 열 ${i%game.cols+1}`
      );

      updateCell(cell,i);

      // 마우스 좌+우 버튼을 함께 누르면 열린 숫자 칸의 주변을 한꺼번에 연다.
      // 모바일에서는 열린 숫자 칸을 다시 탭해도 같은 기능을 실행한다.
      cell.addEventListener('mousedown',e => {
        if (e.buttons === 3 && game.opened.has(i)) {
          e.preventDefault();
          chordHandledAt = Date.now();
          chordHandledIndex = i;
          chord(i);
        }
      });

      cell.addEventListener('click',e => {
        if (longPressed) {
          longPressed = false;
          return;
        }
        if (game.opened.has(i)) {
          if (e.pointerType === 'touch' || window.matchMedia('(pointer: coarse)').matches) {
            chord(i);
          }
          return;
        }
        openCell(i);
      });

      cell.addEventListener('contextmenu',e => {
        e.preventDefault();
        // 좌+우 동시 클릭으로 처리된 직후의 우클릭 메뉴는 깃발로 처리하지 않는다.
        if (chordHandledIndex === i && Date.now() - chordHandledAt < 500) return;
        toggleFlag(i);
      });

      // 모바일에서 길게 누르면 깃발을 꽂는다.
      cell.addEventListener('touchstart',() => {
        longPressed = false;
        touchTimer = setTimeout(() => {
          longPressed = true;
          toggleFlag(i);
        },520);
      },{passive:true});

      cell.addEventListener('touchend',() => {
        clearTimeout(touchTimer);
      },{passive:true});

      cell.addEventListener('touchmove',() => {
        clearTimeout(touchTimer);
      },{passive:true});

      frag.appendChild(cell);
    }

    board.appendChild(frag);
  }

  function updateCell(cell,i) {
    const opened = game.opened.has(i);
    const flagged = game.flags.has(i);
    const mine = game.minesSet.has(i);

    cell.className = 'cell';
    cell.textContent = '';
    cell.disabled = false;

    if (opened) {
      cell.classList.add('opened');

      if (mine) {
        cell.classList.add('mine');
        cell.textContent = '💥';
      } else {
        const n = game.numbers[i];

        if (n>0) {
          cell.textContent = n;
          cell.classList.add('num'+n);
        } else {
          cell.classList.add('empty');
        }
      }
    } else if (flagged) {
      cell.classList.add('flagged');
      cell.textContent = '🚩';
      if (game.over) cell.disabled = true;
    } else if (game.over && mine) {
      cell.classList.add('mine');
      cell.textContent = '💣';
      cell.disabled = true;
    } else if (game.over) {
      cell.disabled = true;
    }

    cell.setAttribute(
      'aria-label',
      opened
        ? (mine ? '폭발한 지뢰' : `열린 칸 ${game.numbers[i]||'빈칸'}`)
        : flagged ? '깃발 표시된 칸' : '닫힌 칸'
    );
  }

  function refreshCells() {
    document.querySelectorAll('.cell').forEach(el =>
      updateCell(el,Number(el.dataset.index))
    );

    $('mineCount').textContent =
      String(game.mines-game.flags.size).padStart(3,'0');
  }

  function setStatus(message,mode) {
    $('statusText').textContent = message;
    $('status').className = 'status'+(mode?' '+mode:'');
  }

  function startClock() {
    if (game.started) return;

    game.started = true;
    startedAt = Date.now();

    timerId = setInterval(() => {
      seconds = Math.floor((Date.now()-startedAt)/1000);
      $('timer').textContent =
        String(Math.min(seconds,999)).padStart(3,'0');
    },250);
  }

  function openCell(i) {
    if (game.over || game.opened.has(i) || game.flags.has(i)) return;

    if (game.first) placeMines(i);
    if (!game.started) startClock();

    if (game.minesSet.has(i)) {
      game.opened.add(i);
      game.over = true;
      clearInterval(timerId);
      refreshCells();

      const target = document.querySelector(
        `.cell[data-index="${i}"]`
      );

      if (target) target.classList.add('exploded');

      $('boardShell').classList.remove('shake');
      void $('boardShell').offsetWidth;
      $('boardShell').classList.add('shake');

      const boom = document.createElement('div');
      boom.className = 'explosion';
      document.body.appendChild(boom);
      setTimeout(()=>boom.remove(),650);

      setStatus(
        '💥 펑! 지뢰를 밟았어요. 새 게임으로 다시 도전하세요.',
        'lose'
      );
      return;
    }

    // 빈칸을 열면 주변의 빈칸도 자동으로 열린다.
    const queue = [i];

    while (queue.length) {
      const current = queue.pop();

      if (
        game.opened.has(current) ||
        game.flags.has(current) ||
        game.minesSet.has(current)
      ) continue;

      game.opened.add(current);

      if (game.numbers[current]===0) {
        for (const n of neighbors(current)) {
          if (!game.opened.has(n)) queue.push(n);
        }
      }
    }

    refreshCells();

    const safeTotal = game.rows*game.cols-game.mines;

    if (game.opened.size===safeTotal) {
      game.over = true;
      clearInterval(timerId);
      refreshCells();

      setStatus(
        `🏆 완벽해요! ${seconds}초 만에 클리어했습니다.`,
        'win'
      );

      confetti();
    } else {
      const n = game.numbers[i];

      setStatus(
        n
          ? `주변에 지뢰가 ${n}개 있어요. 신중하게 다음 칸을 고르세요.`
          : '안전한 빈칸! 주변 영역이 열렸어요.',
        ''
      );
    }
  }

  function chord(i) {
    if (game.over || !game.opened.has(i)) return;

    const number = game.numbers[i];
    if (number <= 0) return;

    const around = neighbors(i);
    const flagCount = around.filter(n => game.flags.has(n)).length;

    // 숫자와 주변 깃발 수가 일치할 때만 열린다.
    if (flagCount !== number) {
      setStatus(`이 칸은 ${number}를 가리켜요. 주변 깃발 수를 확인하세요.`, '');
      return;
    }

    const targets = around.filter(n => !game.opened.has(n) && !game.flags.has(n));
    if (!targets.length) return;

    for (const target of targets) {
      if (game.over) break;
      openCell(target);
    }
  }

  function toggleFlag(i) {
    if (game.over || game.opened.has(i)) return;

    if (game.flags.has(i)) {
      game.flags.delete(i);
    } else {
      if (game.flags.size>=game.mines) {
        setStatus(
          '깃발을 모두 사용했어요. 기존 깃발을 먼저 옮겨 주세요.',
          ''
        );
        return;
      }
      game.flags.add(i);
    }

    refreshCells();

    setStatus(
      game.flags.has(i) ? '🚩 깃발을 꽂았어요.' : '깃발을 제거했어요.',
      ''
    );
  }

  function confetti() {
    const colors = [
      '#5ce1e6','#a78bfa','#ffcf70',
      '#45f0ad','#ff7890','#ffffff'
    ];

    for (let i=0; i<65; i++) {
      const p = document.createElement('i');
      p.className = 'confetti';
      p.style.left = Math.random()*100+'vw';
      p.style.background = colors[i%colors.length];
      p.style.setProperty('--dx',(Math.random()*240-120)+'px');
      p.style.animationDelay = Math.random()*.65+'s';

      document.body.appendChild(p);
      setTimeout(()=>p.remove(),3100);
    }
  }

  $('newGame').addEventListener('click',startGame);
  $('level').addEventListener('change',startGame);

  $('hint').addEventListener('click',() => {
    alert(
      '왼쪽 클릭: 칸 열기\\n'+
      '오른쪽 클릭: 깃발 꽂기/제거\\n'+
      '열린 숫자 칸에서 좌+우 동시 클릭: 주변 칸 열기\\n'+
      '모바일: 길게 눌러 깃발, 열린 숫자 칸 다시 탭해 주변 칸 열기\\n'+
      '첫 번째 칸과 주변은 안전합니다.'
    );
  });

  startGame();
})();
</script>
</body>
</html>
"""

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    [data-testid="stHeader"], footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(
    GAME_HTML,
    height=940,
    scrolling=True,
)
