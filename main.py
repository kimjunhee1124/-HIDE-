import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HIDE - Pixel School EX", page_icon="👻", layout="wide")

GAME_HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box}
body{
  margin:0; background:#090a0f; color:#fff; font-family:monospace;
  overflow:hidden; user-select:none;
}
#wrap{display:flex; justify-content:center; align-items:center; min-height:760px}
#viewport{
  position:relative; width:1000px; height:650px;
  background:#111; border:4px solid #333; overflow:hidden;
  box-shadow:0 0 20px #000;
}

#map-container{
  position:absolute; top:0; left:0;
  width:2000px; height:2000px; /* 50x50 타일 * 40px */
  background:#4a4e57;
}

/* 타일 스타일 */
.tile{position:absolute; width:40px; height:40px; box-sizing:border-box;}
.wall{background:#23272e; border:2px solid #16181c; box-shadow:inset 0 0 5px #000;}
.floor{
  background: radial-gradient(circle, #5a5f68 10%, #4a4e57 90%);
  border:1px solid #42464e;
}
.cab{
  background:#875b38; border:3px solid #3b2518;
  box-shadow:inset 2px 2px #a8774d, inset -2px -2px #604126;
}
.cab:after{content:""; position:absolute; left:14px; top:16px; width:4px; height:4px; background:#1b130e;}
.key-item{
  background:#f1c40f; border:2px solid #b7950b; border-radius:50%;
  width:20px !important; height:20px !important; margin:10px;
  animation: pulse 1s infinite alternate;
}
@keyframes pulse { from { transform:scale(0.8); } to { transform:scale(1.1); } }

.door{background:#e74c3c; border:3px solid #78281f; text-align:center; line-height:34px; font-weight:bold;}

/* 엔티티 */
.sprite{
  position:absolute; width:36px; height:48px; z-index:10;
  transform:translate(-50%, -50%); image-rendering:pixelated;
}
.sprite svg{width:36px; height:48px; shape-rendering:crispEdges;}
.shadow{
  position:absolute; width:30px; height:10px; border-radius:50%;
  background:#0008; transform:translate(-50%, -50%); z-index:5;
}

/* UI/HUD */
.screen{position:absolute; inset:0; display:flex; align-items:center; justify-content:center; z-index:50;}
.hidden{display:none !important;}
#title{flex-direction:column; background:#111317;}
.title{font-size:56px; letter-spacing:6px; text-shadow:4px 4px #d00; margin-bottom:15px;}
.sub{color:#8a93a0; margin-bottom:30px; font-size:16px;}
.selects{display:flex; gap:20px;}
.pick{
  width:200px; height:220px; background:#1c2026; border:3px solid #434a54;
  cursor:pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px;
}
.pick:hover{border-color:#fff; background:#252b34;}

#hud{
  position:absolute; z-index:40; left:15px; top:15px; right:15px;
  display:flex; justify-content:space-between; pointer-events:none;
}
.panel{background:#000c; border:2px solid #555; padding:8px 15px; font-size:14px; border-radius:4px;}
#alert{
  position:absolute; z-index:40; left:50%; top:20px; transform:translateX(-50%);
  font-size:24px; background:#e74c3c; color:#fff; padding:4px 16px; font-weight:bold;
  display:none; border-radius:4px; box-shadow:0 0 10px #e74c3c;
}

#hideUI{
  position:absolute; z-index:100; inset:0; background:#050608;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
}
#keyDisplay{
  width:100px; height:100px; border:4px solid #fff; background:#222;
  display:flex; align-items:center; justify-content:center; font-size:50px; font-weight:bold; margin:20px;
}
.k-btn{width:50px; height:50px; background:#333; border:2px solid #aaa; color:#fff; font-weight:bold; font-size:18px;}

#gameover, #winScreen{background:#0a0000; flex-direction:column;}
.bigbtn{background:#c0392b; color:#fff; border:none; padding:12px 24px; font-size:18px; cursor:pointer; margin-top:20px;}
.bigbtn:hover{background:#e74c3c;}
</style>
</head>
<body>

<div id="wrap">
<div id="viewport">

  <!-- 타이틀 화면 -->
  <div id="title" class="screen">
    <div class="title">HIDE : SCHOOL</div>
    <div class="sub">50x50의 거대한 학교를 탈출하라. 열쇠를 찾아라!</div>
    <div class="selects">
      <div class="pick" onclick="startGame('male')">
        <div id="mPrev"></div><b>남학생</b>
      </div>
      <div class="pick" onclick="startGame('female')">
        <div id="fPrev"></div><b>여학생</b>
      </div>
    </div>
    <p style="color:#666; margin-top:20px;">이동: WASD / 방향키 | 캐비닛 은신: E</p>
  </div>

  <!-- 게임 월드 -->
  <div id="world" class="screen hidden">
    <div id="map-container">
      <div id="tiles"></div>
      <div id="pShadow" class="shadow"></div>
      <div id="mShadow" class="shadow"></div>
      <div id="player" class="sprite"></div>
      <div id="monster" class="sprite"></div>
    </div>

    <div id="hud">
      <div class="panel">❤️ HP: <span id="hp">3</span> | 🔑 열쇠: <span id="keyCount">0</span>/1</div>
      <div class="panel">미션: <span id="mission">열쇠를 찾아 탈출구로 가세요!</span></div>
    </div>
    <div id="alert">! 괴물이 접근 중 !</div>
  </div>

  <!-- 숨기 UI -->
  <div id="hideUI" class="hidden">
    <h2>캐비닛에 숨는 중...</h2>
    <p>지정된 키를 눌러 숨소리를 죽이세요!</p>
    <div id="keyDisplay">W</div>
    <div id="timer">8.0s</div>
  </div>

  <!-- 게임 오버 / 클리어 -->
  <div id="gameover" class="screen hidden">
    <h1 style="font-size:50px; color:#e74c3c;">GAME OVER</h1>
    <p id="overReason">잡히고 말았습니다...</p>
    <button class="bigbtn" onclick="location.reload()">다시 시도</button>
  </div>

  <div id="winScreen" class="screen hidden">
    <h1 style="font-size:50px; color:#2ecc71;">ESCAPE SUCCESS!</h1>
    <p>무사히 학교를 탈출했습니다!</p>
    <button class="bigbtn" style="background:#2ecc71;" onclick="location.reload()">다시 하기</button>
  </div>

</div>
</div>

<script>
const TILE_SIZE = 40;
const MAP_SIZE = 50; // 50x50 = 총 2,500칸

// 도트 SVG 그래픽
const maleSVG = `<svg viewBox="0 0 25 33"><rect x="7" y="2" width="11" height="9" fill="#26242b"/><rect x="6" y="11" width="13" height="8" fill="#f1c4a5"/><rect x="6" y="19" width="13" height="8" fill="#263c67"/><rect x="7" y="27" width="5" height="5" fill="#17191f"/><rect x="14" y="27" width="5" height="5" fill="#17191f"/></svg>`;
const femaleSVG = `<svg viewBox="0 0 25 33"><rect x="5" y="2" width="15" height="11" fill="#4a2d32"/><rect x="6" y="11" width="13" height="8" fill="#f1c4a5"/><rect x="6" y="19" width="13" height="8" fill="#a93226"/><rect x="7" y="27" width="5" height="5" fill="#20242d"/><rect x="14" y="27" width="5" height="5" fill="#20242d"/></svg>`;
const monsterSVG = `<svg viewBox="0 0 25 33"><rect x="6" y="3" width="13" height="23" fill="#333"/><rect x="8" y="7" width="9" height="8" fill="#111"/><rect x="10" y="9" width="3" height="3" fill="#f00"/><rect x="15" y="9" width="3" height="3" fill="#f00"/></svg>`;

document.getElementById('mPrev').innerHTML = `<div class="sprite" style="position:relative">${maleSVG}</div>`;
document.getElementById('fPrev').innerHTML = `<div class="sprite" style="position:relative">${femaleSVG}</div>`;

// 50x50 맵 생성 (0: 바닥, 1: 벽, 2: 캐비닛, 3: 열쇠, 4: 출구)
let mapData = [];
function generateMap() {
  for(let r=0; r<MAP_SIZE; r++) {
    let row = [];
    for(let c=0; c<MAP_SIZE; c++) {
      if(r===0 || r===MAP_SIZE-1 || c===0 || c===MAP_SIZE-1) {
        row.push(1); // 외곽 벽
      } else if(r % 4 === 0 && c % 4 === 0 && Math.random() > 0.3) {
        row.push(1); // 기둥/내부 벽
      } else {
        row.push(0);
      }
    }
    mapData.push(row);
  }
  
  // 특수 위치 지정
  mapData[2][2] = 0; // 시작점 안전지대
  mapData[5][5] = 2; // 캐비닛
  mapData[20][30] = 2;
  mapData[40][10] = 2;
  
  mapData[45][45] = 3; // 열쇠 위치
  mapData[48][48] = 4; // 출구 문
}
generateMap();

// 맵 렌더링
function renderMap() {
  const container = document.getElementById('tiles');
  let html = '';
  for(let r=0; r<MAP_SIZE; r++) {
    for(let c=0; c<MAP_SIZE; c++) {
      const type = mapData[r][c];
      let tileClass = 'floor';
      if(type === 1) tileClass = 'wall';
      else if(type === 2) tileClass = 'cab';
      else if(type === 3) tileClass = 'key-item';
      else if(type === 4) tileClass = 'door';

      html += `<div class="tile ${tileClass}" style="left:${c*TILE_SIZE}px; top:${r*TILE_SIZE}px;">${type===4?'EXIT':''}</div>`;
    }
  }
  container.innerHTML = html;
}
renderMap();

// 상태 변수
let px = 100, py = 100;
let mx = 800, my = 800;
let hp = 3, hasKey = false;
let isHidden = false, gameEnded = false;
let keysPressed = {};
let targetKey = 'W', hideTimer = 8.0;

function startGame(type) {
  document.getElementById('title').classList.add('hidden');
  document.getElementById('world').classList.remove('hidden');
  document.getElementById('player').innerHTML = type === 'male' ? maleSVG : femaleSVG;
  document.getElementById('monster').innerHTML = monsterSVG;
  requestAnimationFrame(gameLoop);
}

document.addEventListener('keydown', e => {
  const k = e.key.toLowerCase();
  keysPressed[k] = true;
  if(e.key === 'e' || e.key === 'E') checkCabinet();
  if(isHidden && ['w','a','s','d'].includes(k)) handleHideInput(k.toUpperCase());
});
document.addEventListener('keyup', e => keysPressed[e.key.toLowerCase()] = false);

// 충돌 감지
function isSolid(x, y) {
  const col = Math.floor(x / TILE_SIZE);
  const row = Math.floor(y / TILE_SIZE);
  if(row < 0 || row >= MAP_SIZE || col < 0 || col >= MAP_SIZE) return true;
  return mapData[row][col] === 1; // 벽은 통과 불가
}

// 플레이어 이동 및 타일 상호작용
function updatePlayer() {
  let speed = 3.5;
  let dx = 0, dy = 0;
  if(keysPressed['w'] || keysPressed['arrowup']) dy -= 1;
  if(keysPressed['s'] || keysPressed['arrowdown']) dy += 1;
  if(keysPressed['a'] || keysPressed['arrowleft']) dx -= 1;
  if(keysPressed['d'] || keysPressed['arrowright']) dx += 1;

  if(dx !== 0 && dy !== 0) { dx *= 0.7071; dy *= 0.7071; }

  let nx = px + dx * speed;
  let ny = py + dy * speed;

  if(!isSolid(nx, py)) px = nx;
  if(!isSolid(px, ny)) py = ny;

  // 열쇠/출구 상호작용
  const pCol = Math.floor(px / TILE_SIZE);
  const pRow = Math.floor(py / TILE_SIZE);

  if(mapData[pRow][pCol] === 3) {
    hasKey = true;
    mapData[pRow][pCol] = 0; // 열쇠 획득 후 제거
    renderMap();
    document.getElementById('keyCount').textContent = '1';
    document.getElementById('mission').textContent = '열쇠를 얻었습니다! 탈출구(48,48)로 가세요!';
  }

  if(mapData[pRow][pCol] === 4) {
    if(hasKey) win();
    else document.getElementById('mission').textContent = '열쇠가 필요합니다!';
  }
}

// 괴물 AI
function updateMonster() {
  let dist = Math.hypot(px - mx, py - my);
  if(dist < 400 && !isHidden) {
    document.getElementById('alert').style.display = 'block';
    let speed = 2.2;
    let angle = Math.atan2(py - my, px - mx);
    let nx = mx + Math.cos(angle) * speed;
    let ny = my + Math.sin(angle) * speed;
    if(!isSolid(nx, my)) mx = nx;
    if(!isSolid(mx, ny)) my = ny;

    if(dist < 30) lose("괴물에게 잡혔습니다!");
  } else {
    document.getElementById('alert').style.display = 'none';
  }
}

// 카메라 추적
function updateCamera() {
  const container = document.getElementById('map-container');
  // 화면 중앙(500, 325)에 플레이어가 위치하도록 맵 이동
  let camX = 500 - px;
  let camY = 325 - py;
  container.style.transform = `translate(${camX}px, ${camY}px)`;
}

function draw() {
  const p = document.getElementById('player');
  const m = document.getElementById('monster');
  p.style.left = px + 'px'; p.style.top = py + 'px';
  m.style.left = mx + 'px'; m.style.top = my + 'px';

  document.getElementById('pShadow').style.left = px + 'px';
  document.getElementById('pShadow').style.top = (py + 18) + 'px';
  document.getElementById('mShadow').style.left = mx + 'px';
  document.getElementById('mShadow').style.top = (my + 18) + 'px';
}

// 캐비닛 은신
function checkCabinet() {
  const pCol = Math.floor(px / TILE_SIZE);
  const pRow = Math.floor(py / TILE_SIZE);
  if(mapData[pRow][pCol] === 2 && !isHidden) {
    isHidden = true;
    document.getElementById('world').classList.add('hidden');
    document.getElementById('hideUI').classList.remove('hidden');
    hideTimer = 8.0;
    nextHideKey();
  }
}

function nextHideKey() {
  const keys = ['W', 'A', 'S', 'D'];
  targetKey = keys[Math.floor(Math.random() * 4)];
  document.getElementById('keyDisplay').textContent = targetKey;
}

function handleHideInput(k) {
  if(k === targetKey) {
    hideTimer = Math.min(8.0, hideTimer + 0.5);
    nextHideKey();
  } else {
    hp--;
    document.getElementById('hp').textContent = hp;
    if(hp <= 0) lose("숨어서 패닉에 빠졌습니다!");
  }
}

function updateHideLogic(dt) {
  hideTimer -= dt;
  document.getElementById('timer').textContent = hideTimer.toFixed(1) + 's';
  if(hideTimer <= 0) {
    isHidden = false;
    document.getElementById('hideUI').classList.add('hidden');
    document.getElementById('world').classList.remove('hidden');
    mx = Math.max(100, mx - 300); // 괴물이 멀어짐
  }
}

function lose(reason) {
  gameEnded = true;
  document.getElementById('world').classList.add('hidden');
  document.getElementById('hideUI').classList.add('hidden');
  document.getElementById('gameover').classList.remove('hidden');
  document.getElementById('overReason').textContent = reason;
}

function win() {
  gameEnded = true;
  document.getElementById('world').classList.add('hidden');
  document.getElementById('winScreen').classList.remove('hidden');
}

let lastTime = performance.now();
function gameLoop(now) {
  if(gameEnded) return;
  let dt = (now - lastTime) / 1000;
  lastTime = now;

  if(!isHidden) {
    updatePlayer();
    updateMonster();
    updateCamera();
    draw();
  } else {
    updateHideLogic(dt);
  }

  requestAnimationFrame(gameLoop);
}
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=700, scrolling=False)
