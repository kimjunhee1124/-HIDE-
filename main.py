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
  margin:0; background:#07080b; color:#fff; font-family:'Courier New', monospace;
  overflow:hidden; user-select:none;
}
#wrap{display:flex; justify-content:center; align-items:center; min-height:760px}
#viewport{
  position:relative; width:1000px; height:650px;
  background:#0e1015; border:4px solid #2d333f; overflow:hidden;
  box-shadow:0 0 25px rgba(0,0,0,0.9);
}

#map-container{
  position:absolute; top:0; left:0;
  width:2000px; height:2000px; /* 50x50 타일 * 40px */
  background:#323741;
}

/* 타일 디자인 (Pixel Art Style) */
.tile{position:absolute; width:40px; height:40px; box-sizing:border-box; image-rendering:pixelated;}
.wall{
  background:#1a1d24; 
  border:3px solid #0d0e12; 
  box-shadow:inset 2px 2px 0 #2a2f3a, inset -2px -2px 0 #121419;
}
.floor{
  background: #3a3f4b;
  border-right:1px solid #303540;
  border-bottom:1px solid #303540;
}

/* 회색 철제 캐비닛 (Grey Steel Cabinet) */
.cab{
  background:#5a626e; 
  border:3px solid #1e2229;
  box-shadow:inset 3px 3px 0 #7c8594, inset -3px -3px 0 #3a4049;
  position:absolute;
}
.cab::before{
  content:""; position:absolute; left:6px; top:6px; right:6px; height:8px;
  background:#3e444d; border-bottom:2px solid #6f7785;
}
.cab::after{
  content:""; position:absolute; right:6px; top:20px; width:4px; height:6px;
  background:#d0d7e1; box-shadow:0 1px 0 #111;
}

/* 열쇠 아이템 */
.key-item{
  background:transparent;
  display:flex; align-items:center; justify-content:center;
}
.key-icon{
  width:20px; height:20px;
  animation: bounce 0.8s infinite alternate;
}
@keyframes bounce { from { transform:translateY(-2px); } to { transform:translateY(3px); } }

.door{
  background:#8b2626; border:3px solid #3a0d0d; text-align:center; 
  line-height:34px; font-weight:bold; color:#ffb3b3; font-size:12px;
  box-shadow:inset 2px 2px 0 #ad3b3b;
}

/* 엔티티 및 스프라이트 */
.sprite{
  position:absolute; width:32px; height:42px; z-index:10;
  transform:translate(-50%, -50%); image-rendering:pixelated;
}
.sprite svg{width:32px; height:42px; shape-rendering:crispEdges;}
.shadow{
  position:absolute; width:26px; height:8px; border-radius:50%;
  background:rgba(0,0,0,0.5); transform:translate(-50%, -50%); z-index:5;
}

/* UI / HUD */
.screen{position:absolute; inset:0; display:flex; align-items:center; justify-content:center; z-index:50;}
.hidden{display:none !important;}
#title{flex-direction:column; background:#0b0c10;}
.title{font-size:52px; letter-spacing:4px; text-shadow:4px 4px #8b0000; margin-bottom:10px; color:#f0f0f0;}
.sub{color:#7a8391; margin-bottom:25px; font-size:15px;}
.selects{display:flex; gap:25px;}
.pick{
  width:180px; height:200px; background:#161920; border:3px solid #3a4150;
  cursor:pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px;
  transition: transform 0.1s;
}
.pick:hover{border-color:#fff; background:#202530; transform:translateY(-3px);}

#hud{
  position:absolute; z-index:40; left:15px; top:15px; right:15px;
  display:flex; justify-content:space-between; pointer-events:none;
}
.panel{background:rgba(10,12,16,0.85); border:2px solid #4a5260; padding:8px 14px; font-size:14px; border-radius:2px;}
#alert{
  position:absolute; z-index:40; left:50%; top:20px; transform:translateX(-50%);
  font-size:20px; background:#c0392b; color:#fff; padding:4px 16px; font-weight:bold;
  display:none; border:2px solid #000; box-shadow:3px 3px 0 #000;
}

#hideUI{
  position:absolute; z-index:100; inset:0; background:#050608;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
}
#keyDisplay{
  width:90px; height:90px; border:4px solid #fff; background:#1c2029;
  display:flex; align-items:center; justify-content:center; font-size:48px; font-weight:bold; margin:20px;
  box-shadow:5px 5px 0 #000;
}

#gameover, #winScreen{background:#0a0505; flex-direction:column;}
.bigbtn{
  background:#962d22; color:#fff; border:2px solid #e74c3c; padding:10px 22px; 
  font-size:16px; font-family:inherit; cursor:pointer; margin-top:20px; box-shadow:4px 4px 0 #000;
}
.bigbtn:hover{background:#c0392b;}
</style>
</head>
<body>

<div id="wrap">
<div id="viewport">

  <!-- 타이틀 화면 -->
  <div id="title" class="screen">
    <div class="title">👻 HIDE : PIXEL SCHOOL</div>
    <div class="sub">어두운 학교 안, 괴물을 피해 열쇠를 찾아 탈출하라!</div>
    <div class="selects">
      <div class="pick" onclick="startGame('male')">
        <div id="mPrev"></div><b>남학생</b>
      </div>
      <div class="pick" onclick="startGame('female')">
        <div id="fPrev"></div><b>여학생</b>
      </div>
    </div>
    <p style="color:#5a6270; margin-top:25px; font-size:13px;">이동: WASD / 방향키 | 철제 캐비닛 은신: E</p>
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
      <div class="panel">목표: <span id="mission">열쇠를 찾고 출구로 탈출하세요!</span></div>
    </div>
    <div id="alert">! 경고: 괴물이 추격 중 !</div>
  </div>

  <!-- 숨기 UI -->
  <div id="hideUI" class="hidden">
    <h2 style="color:#bdc3c7;">철제 캐비닛 안...</h2>
    <p style="color:#7f8c8d;">화면에 나타나는 키를 신속하게 입력해 숨소리를 죽이세요!</p>
    <div id="keyDisplay">W</div>
    <div id="timer" style="font-size:22px; color:#e74c3c;">8.0s</div>
  </div>

  <!-- 게임 오버 / 클리어 -->
  <div id="gameover" class="screen hidden">
    <h1 style="font-size:48px; color:#c0392b; text-shadow:3px 3px #000;">GAME OVER</h1>
    <p id="overReason" style="color:#a6a6a6;">괴물에게 붙잡혔습니다...</p>
    <button class="bigbtn" onclick="location.reload()">다시 시작</button>
  </div>

  <div id="winScreen" class="screen hidden">
    <h1 style="font-size:48px; color:#27ae60; text-shadow:3px 3px #000;">ESCAPE SUCCESS!</h1>
    <p style="color:#a6a6a6;">무사히 학교를 탈출했습니다!</p>
    <button class="bigbtn" style="background:#27ae60; border-color:#2ecc71;" onclick="location.reload()">다시 시작</button>
  </div>

</div>
</div>

<script>
const TILE_SIZE = 40;
const MAP_SIZE = 50; // 50x50 = 총 2,500칸

// 귀여운 픽셀 도트 SVG 그래픽
const maleSVG = `
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
  <!-- 머리카락 -->
  <rect x="4" y="1" width="8" height="2" fill="#2c3e50"/>
  <rect x="3" y="2" width="10" height="4" fill="#2c3e50"/>
  <!-- 얼굴 -->
  <rect x="4" y="5" width="8" height="5" fill="#f3d2b3"/>
  <!-- 눈 -->
  <rect x="5" y="7" width="2" height="2" fill="#111"/>
  <rect x="9" y="7" width="2" height="2" fill="#111"/>
  <rect x="6" y="7" width="1" height="1" fill="#fff"/>
  <rect x="10" y="7" width="1" height="1" fill="#fff"/>
  <!-- 교복 상의 -->
  <rect x="3" y="10" width="10" height="5" fill="#2980b9"/>
  <rect x="7" y="10" width="2" height="3" fill="#fff"/>
  <rect x="7" y="12" width="2" height="2" fill="#c0392b"/> <!-- 넥타이 -->
  <!-- 바지 및 신발 -->
  <rect x="4" y="15" width="3" height="4" fill="#34495e"/>
  <rect x="9" y="15" width="3" height="4" fill="#34495e"/>
  <rect x="3" y="18" width="4" height="2" fill="#111"/>
  <rect x="9" y="18" width="4" height="2" fill="#111"/>
</svg>`;

const femaleSVG = `
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
  <!-- 머리카락 -->
  <rect x="3" y="1" width="10" height="3" fill="#5d4037"/>
  <rect x="2" y="3" width="12" height="7" fill="#5d4037"/>
  <!-- 얼굴 -->
  <rect x="4" y="5" width="8" height="5" fill="#f3d2b3"/>
  <!-- 눈 & 볼터치 -->
  <rect x="5" y="7" width="2" height="2" fill="#111"/>
  <rect x="9" y="7" width="2" height="2" fill="#111"/>
  <rect x="6" y="7" width="1" height="1" fill="#fff"/>
  <rect x="10" y="7" width="1" height="1" fill="#fff"/>
  <rect x="4" y="8" width="1" height="1" fill="#e84393"/>
  <rect x="11" y="8" width="1" height="1" fill="#e84393"/>
  <!-- 교복 상의 및 치마 -->
  <rect x="3" y="10" width="10" height="4" fill="#2980b9"/>
  <rect x="7" y="10" width="2" height="2" fill="#fff"/>
  <rect x="3" y="14" width="10" height="3" fill="#c0392b"/> <!-- 세일러 치마 -->
  <!-- 다리 및 신발 -->
  <rect x="5" y="17" width="2" height="2" fill="#f3d2b3"/>
  <rect x="9" y="17" width="2" height="2" fill="#f3d2b3"/>
  <rect x="4" y="18" width="3" height="2" fill="#111"/>
  <rect x="9" y="18" width="3" height="2" fill="#111"/>
</svg>`;

const monsterSVG = `
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
  <!-- 몸체 -->
  <rect x="3" y="2" width="10" height="15" fill="#1e272c"/>
  <rect x="2" y="5" width="12" height="10" fill="#2c3e50"/>
  <!-- 붉은 눈 -->
  <rect x="4" y="6" width="3" height="3" fill="#e74c3c"/>
  <rect x="9" y="6" width="3" height="3" fill="#e74c3c"/>
  <rect x="5" y="7" width="1" height="1" fill="#fff"/>
  <rect x="10" y="7" width="1" height="1" fill="#fff"/>
  <!-- 입 -->
  <rect x="5" y="11" width="6" height="2" fill="#000"/>
  <rect x="6" y="11" width="1" height="1" fill="#fff"/>
  <rect x="9" y="11" width="1" height="1" fill="#fff"/>
  <!-- 그림자 다리 -->
  <rect x="3" y="17" width="3" height="3" fill="#111"/>
  <rect x="10" y="17" width="3" height="3" fill="#111"/>
</svg>`;

const keySVG = `
<svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="key-icon">
  <path d="M6 2 C3.8 2 2 3.8 2 6 C2 8.2 3.8 10 6 10 C7 10 7.9 9.6 8.5 9 L11 11.5 L11 13 L13 13 L13 11 L14 11 L14 9 L11.5 6.5 C11.9 5.9 12 5 12 4 C12 2 10 2 6 2 Z M6 4 C7.1 4 8 4.9 8 6 C8 7.1 7.1 8 6 8 C4.9 8 4 7.1 4 6 C4 4.9 4.9 4 6 4 Z" fill="#f1c40f"/>
</svg>`;

document.getElementById('mPrev').innerHTML = `<div class="sprite" style="position:relative">${maleSVG}</div>`;
document.getElementById('fPrev').innerHTML = `<div class="sprite" style="position:relative">${femaleSVG}</div>`;

// 맵 데이터 생성 (0: 바닥, 1: 벽, 2: 회색 철제 캐비닛, 3: 열쇠, 4: 출구)
let mapData = [];
function generateMap() {
  for(let r=0; r<MAP_SIZE; r++) {
    let row = [];
    for(let c=0; c<MAP_SIZE; c++) {
      if(r===0 || r===MAP_SIZE-1 || c===0 || c===MAP_SIZE-1) {
        row.push(1); // 외곽 벽
      } else if(r % 5 === 0 && c % 5 === 0 && Math.random() > 0.2) {
        row.push(1); // 내벽
      } else {
        row.push(0);
      }
    }
    mapData.push(row);
  }
  
  // 특수 위치 지정 및 철제 캐비닛 수동 배치
  mapData[2][2] = 0; // 플레이어 시작점
  
  // 회색 철제 캐비닛 배치 (2번)
  mapData[4][4] = 2;
  mapData[12][8] = 2;
  mapData[22][18] = 2;
  mapData[35][10] = 2;
  mapData[42][38] = 2;
  mapData[18][42] = 2;

  mapData[44][44] = 3; // 열쇠 위치
  mapData[48][48] = 4; // 출구
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
      let content = '';

      if(type === 1) tileClass = 'wall';
      else if(type === 2) tileClass = 'cab'; // 회색 철제 캐비닛
      else if(type === 3) { tileClass = 'key-item'; content = keySVG; }
      else if(type === 4) { tileClass = 'door'; content = 'EXIT'; }

      html += `<div class="tile ${tileClass}" style="left:${c*TILE_SIZE}px; top:${r*TILE_SIZE}px;">${content}</div>`;
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

// 이동 충돌 판단 (벽만 통과 불가)
function isSolid(x, y) {
  const col = Math.floor(x / TILE_SIZE);
  const row = Math.floor(y / TILE_SIZE);
  if(row < 0 || row >= MAP_SIZE || col < 0 || col >= MAP_SIZE) return true;
  return mapData[row][col] === 1; 
}

// 플레이어 이동 로직
function updatePlayer() {
  let speed = 3.2;
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

  // 아이템/상호작용 체크
  const pCol = Math.floor(px / TILE_SIZE);
  const pRow = Math.floor(py / TILE_SIZE);

  if(mapData[pRow][pCol] === 3) {
    hasKey = true;
    mapData[pRow][pCol] = 0; // 열쇠 습득
    renderMap();
    document.getElementById('keyCount').textContent = '1';
    document.getElementById('mission').textContent = '열쇠를 얻었습니다! (48,48) 출구로 이동하세요!';
  }

  if(mapData[pRow][pCol] === 4) {
    if(hasKey) win();
    else document.getElementById('mission').textContent = '열쇠가 필요합니다!';
  }
}

// 괴물 AI
function updateMonster() {
  let dist = Math.hypot(px - mx, py - my);
  if(dist < 380 && !isHidden) {
    document.getElementById('alert').style.display = 'block';
    let speed = 2.1;
    let angle = Math.atan2(py - my, px - mx);
    let nx = mx + Math.cos(angle) * speed;
    let ny = my + Math.sin(angle) * speed;
    if(!isSolid(nx, my)) mx = nx;
    if(!isSolid(mx, ny)) my = ny;

    if(dist < 28) lose("괴물에게 잡혔습니다!");
  } else {
    document.getElementById('alert').style.display = 'none';
  }
}

// 카메라 이동
function updateCamera() {
  const container = document.getElementById('map-container');
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
  document.getElementById('pShadow').style.top = (py + 16) + 'px';
  document.getElementById('mShadow').style.left = mx + 'px';
  document.getElementById('mShadow').style.top = (my + 16) + 'px';
}

// 회색 철제 캐비닛 은신
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
    hideTimer = Math.min(8.0, hideTimer + 0.4);
    nextHideKey();
  } else {
    hp--;
    document.getElementById('hp').textContent = hp;
    if(hp <= 0) lose("캐비닛 안에서 소음을 내 잡히고 말았습니다!");
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
