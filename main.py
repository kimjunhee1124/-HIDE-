import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HIDE - Pixel School EX", page_icon="👻", layout="wide")

GAME_HTML = """
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
  width:1000px; height:1000px;
  background:#323741;
}

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
  background:#27ae60; border:3px solid #1e8449; text-align:center; 
  line-height:34px; font-weight:bold; color:#e8f8f5; font-size:10px;
  box-shadow:inset 2px 2px 0 #52be80;
}

.sprite{
  position:absolute; width:32px; height:42px; z-index:10;
  transform:translate(-50%, -50%); image-rendering:pixelated;
}
.sprite svg{width:32px; height:42px; shape-rendering:crispEdges;}
.shadow{
  position:absolute; width:26px; height:8px; border-radius:50%;
  background:rgba(0,0,0,0.5); transform:translate(-50%, -50%); z-index:5;
}

.screen{position:absolute; inset:0; display:flex; align-items:center; justify-content:center; z-index:50;}
.hidden{display:none !important;}
#title{flex-direction:column; background:#0b0c10;}
.title{font-size:52px; letter-spacing:4px; text-shadow:4px 4px #8b0000; margin-bottom:10px; color:#f0f0f0;}
.sub{color:#7a8391; margin-bottom:20px; font-size:15px;}
.controls-box{
  background:#161920; border:2px solid #3a4150; padding:15px 25px; border-radius:8px;
  margin-bottom:20px; text-align:center; color:#2ecc71;
}
.selects{display:flex; gap:25px;}
.pick{
  width:180px; height:180px; background:#161920; border:3px solid #3a4150;
  cursor:pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px;
  transition: transform 0.1s;
}
.pick:hover{border-color:#fff; background:#202530; transform:translateY(-3px);}

#hud{
  position:absolute; z-index:40; left:15px; top:15px; right:15px;
  display:flex; justify-content:space-between; pointer-events:none; gap:10px;
}
.panel{background:rgba(10,12,16,0.85); border:2px solid #4a5260; padding:8px 14px; font-size:14px; border-radius:2px;}
#alert{
  position:absolute; z-index:40; left:50%; top:20px; transform:translateX(-50%);
  font-size:20px; background:#c0392b; color:#fff; padding:4px 16px; font-weight:bold;
  display:none; border:2px solid #000; box-shadow:3px 3px 0 #000;
}

#tutorialNotice{
  position:absolute; z-index:90; inset:0; background:rgba(0,0,0,0.8);
  display:flex; align-items:center; justify-content:center;
}
.notice-box{
  background:#161920; border:3px solid #3498db; padding:25px 35px; border-radius:8px;
  max-width:550px; text-align:center; box-shadow:0 0 20px rgba(52,152,219,0.4);
}
.notice-box h2{color:#3498db; margin-top:0;}
.notice-box ul{text-align:left; color:#dcdde1; line-height:1.6; margin:15px 0;}

#hideUI{
  position:absolute; z-index:100; inset:0;
  background: radial-gradient(circle, rgba(10, 15, 20, 0.3) 30%, rgba(0, 0, 0, 0.95) 90%);
  backdrop-filter: blur(2px);
  display:flex; flex-direction:column; align-items:center; justify-content:center;
}

#gaugeContainer{
  width:260px; height:16px; background:#1a1a1a; border:2px solid #e74c3c;
  border-radius:8px; margin:10px auto 15px auto; overflow:hidden;
  box-shadow:0 0 10px rgba(231, 76, 60, 0.5);
}
#gaugeBar{
  width:100%; height:100%; background:linear-gradient(90deg, #e74c3c, #ff6b6b);
  transition: width 0.1s linear;
}

#keyDisplay{
  width:85px; height:85px; border:4px solid #e74c3c; background:rgba(22, 25, 32, 0.9);
  display:flex; align-items:center; justify-content:center; font-size:48px; font-weight:bold; margin:10px auto;
  box-shadow:0 0 20px rgba(231, 76, 60, 0.6); color:#fff;
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

  <div id="title" class="screen">
    <div class="title">👻 HIDE : PIXEL SCHOOL</div>
    <div class="sub">괴물이 당신보다 미세하게 빠릅니다! 캐비닛을 활용하세요!</div>
    
    <div class="controls-box">
      <div style="font-size:16px; font-weight:bold; margin-bottom:6px; color:#fff;">🎮 조작 안내</div>
      <div>이동: <b>W, A, S, D</b> 또는 <b>방향키</b></div>
      <div>상호작용 (은신 / 열쇠 획득 / 이동): <b style="color:#f1c40f;">[ E ] Key</b></div>
    </div>

    <div class="selects">
      <div class="pick" onclick="startGame('male')">
        <div id="mPrev"></div><b>남학생</b>
      </div>
      <div class="pick" onclick="startGame('female')">
        <div id="fPrev"></div><b>여학생</b>
      </div>
    </div>
  </div>

  <div id="world" class="screen hidden">
    <div id="map-container">
      <div id="tiles"></div>
      <div id="pShadow" class="shadow"></div>
      <div id="mShadow" class="shadow"></div>
      <div id="player" class="sprite"></div>
      <div id="monster" class="sprite"></div>
    </div>

    <div id="tutorialNotice">
      <div class="notice-box">
        <h2>📢 [튜토리얼 스테이지]</h2>
        <p style="color:#f1c40f; font-weight:bold;">괴물과의 조우를 체험하고 탈출하세요!</p>
        <ul>
          <li><b>목표:</b> 랜덤 위치의 열쇠(🔑)를 찾으세요.</li>
          <li><b>은신 연습:</b> 괴물이 다가오면 캐비닛에 숨어 QTE 미션을 수행하세요.</li>
          <li><b>입장:</b> 열쇠로 우측 하단의 START 문을 열어 본 게임으로 향하세요.</li>
        </ul>
        <button class="bigbtn" style="background:#2980b9; border-color:#3498db;" onclick="closeTutorial()">이해했습니다 (시작)</button>
      </div>
    </div>

    <div id="hud">
      <div class="panel">❤️ HP: <span id="hp">3</span> | 🔑 열쇠: <span id="keyCount">0</span>/1</div>
      <div class="panel">상태: <span id="mission" style="color:#f1c40f;">[튜토리얼] 열쇠를 찾으세요!</span></div>
      <div class="panel" style="color:#aaa;">조작: WASD(이동) / E(상호작용)</div>
    </div>
    <div id="alert">! 경고: 괴물이 추격 중 !</div>
  </div>

  <div id="hideUI" class="hidden">
    <div id="qteBox" style="text-align:center;">
      <h2 id="hideTitle" style="color:#e74c3c; margin:0 0 10px 0; text-shadow:2px 2px #000;">⚠️ 괴물이 바로 앞에 있습니다! 숨소리를 참으세요!</h2>
      <p id="hideSub" style="color:#bdc3c7; margin:0; text-shadow:1px 1px #000;">게이지가 다 떨어지기 전에 알맞은 키를 누르세요!</p>
      
      <div id="gaugeContainer">
        <div id="gaugeBar"></div>
      </div>

      <div id="keyDisplay">W</div>
      <div style="font-size:16px; color:#ddd; margin-top:5px; text-shadow:1px 1px #000;">남은 횟수: <b id="reqCount" style="color:#f1c40f;">5</b>회</div>
    </div>
    
    <div id="safeBox" class="hidden" style="text-align:center;">
      <h2 style="color:#2ecc71; margin:0 0 10px 0; text-shadow:2px 2px #000;">🤫 안전하게 은신 중입니다...</h2>
      <p style="color:#bdc3c7; margin:0; text-shadow:1px 1px #000;">괴물은 당신을 인식하지 못합니다. 밖으로 나가려면 <b>[E]</b> 키를 누르세요.</p>
    </div>
  </div>

  <div id="gameover" class="screen hidden">
    <h1 style="font-size:48px; color:#c0392b; text-shadow:3px 3px #000;">GAME OVER</h1>
    <p id="overReason" style="color:#a6a6a6;">괴물에게 붙잡혔습니다...</p>
    <button class="bigbtn" onclick="location.reload()">다시 시작</button>
  </div>

  <div id="winScreen" class="screen hidden">
    <h1 style="font-size:40px; color:#27ae60; text-shadow:3px 3px #000;">🎓 튜토리얼 클리어!</h1>
    <p style="color:#a6a6a6;">기본 생존 수칙을 모두 익혔습니다. 이제 본 게임으로 입장합니다...</p>
    <button class="bigbtn" style="background:#27ae60; border-color:#2ecc71;" onclick="location.reload()">본 게임 시작하기</button>
  </div>

</div>
</div>

<script>
let audioCtx = null;

function playLockerSound() {
  try {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(150, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.15);

    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start();
    osc.stop(audioCtx.currentTime + 0.15);
  } catch(e) {}
}

const TILE_SIZE = 40;
const MAP_SIZE = 25;
const MAX_HIDE_TIME = 6.0;

const maleSVG = `
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="1" width="8" height="2" fill="#2c3e50"/>
  <rect x="3" y="2" width="10" height="4" fill="#2c3e50"/>
  <rect x="4" y="5" width="8" height="5" fill="#f3d2b3"/>
  <rect x="5" y="7" width="2" height="2" fill="#111"/>
  <rect x="9" y="7" width="2" height="2" fill="#111"/>
  <rect x="6" y="7" width="1" height="1" fill="#fff"/>
  <rect x="10" y="7" width="1" height="1" fill="#fff"/>
  <rect x="3" y="10" width="10" height="5" fill="#2980b9"/>
  <rect x="7" y="10" width="2" height="3" fill="#fff"/>
  <rect x="7" y="12" width="2" height="2" fill="#c0392b"/>
  <rect x="4" y="15" width="3" height="4" fill="#34495e"/>
  <rect x="9" y="15" width="3" height="4" fill="#34495e"/>
  <rect x="3" y="18" width="4" height="2" fill="#111"/>
  <rect x="9" y="18" width="4" height="2" fill="#111"/>
</svg>`;

const femaleSVG = `
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="1" width="10" height="3" fill="#5d4037"/>
  <rect x="2" y="3" width="12" height="7" fill="#5d4037"/>
  <rect x="4" y="5" width="8" height="5" fill="#f3d2b3"/>
  <rect x="5" y="7" width="2" height="2" fill="#111"/>
  <rect x="9" y="7" width="2" height="2" fill="#111"/>
  <rect x="6" y="7" width="1" height="1" fill="#fff"/>
  <rect x="10" y="7" width="1" height="1" fill="#fff"/>
  <rect x="4" y="8" width="1" height="1" fill="#e84393"/>
  <rect x="11" y="8" width="1" height="1" fill="#e84393"/>
  <rect x="3" y="10" width="10" height="4" fill="#2980b9"/>
  <rect x="7" y="10" width="2" height="2" fill="#fff"/>
  <rect x="3" y="14" width="10" height="3" fill="#c0392b"/>
  <rect x="5" y="17" width="2" height="2" fill="#f3d2b3"/>
  <rect x="9" y="17" width="2" height="2" fill="#f3d2b3"/>
  <rect x="4" y="18" width="3" height="2" fill="#111"/>
  <rect x="9" y="18" width="3" height="2" fill="#111"/>
</svg>`;

const monsterSVG = `
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="2" width="10" height="15" fill="#1e272c"/>
  <rect x="2" y="5" width="12" height="10" fill="#2c3e50"/>
  <rect x="4" y="6" width="3" height="3" fill="#e74c3c"/>
  <rect x="9" y="6" width="3" height="3" fill="#e74c3c"/>
  <rect x="5" y="7" width="1" height="1" fill="#fff"/>
  <rect x="10" y="7" width="1" height="1" fill="#fff"/>
  <rect x="5" y="11" width="6" height="2" fill="#000"/>
  <rect x="6" y="11" width="1" height="1" fill="#fff"/>
  <rect x="9" y="11" width="1" height="1" fill="#fff"/>
  <rect x="3" y="17" width="3" height="3" fill="#111"/>
  <rect x="10" y="17" width="3" height="3" fill="#111"/>
</svg>`;

const keySVG = `
<svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="key-icon">
  <path d="M6 2 C3.8 2 2 3.8 2 6 C2 8.2 3.8 10 6 10 C7 10 7.9 9.6 8.5 9 L11 11.5 L11 13 L13 13 L13 11 L14 11 L14 9 L11.5 6.5 C11.9 5.9 12 5 12 4 C12 2 10 2 6 2 Z M6 4 C7.1 4 8 4.9 8 6 C8 7.1 7.1 8 6 8 C4.9 8 4 7.1 4 6 C4 4.9 4.9 4 6 4 Z" fill="#f1c40f"/>
</svg>`;

document.getElementById('mPrev').innerHTML = `<div class="sprite" style="position:relative">${maleSVG}</div>`;
document.getElementById('fPrev').innerHTML = `<div class="sprite" style="position:relative">${femaleSVG}</div>`;

let mapData = [];
function generateMap() {
  mapData = [];
  let freeTiles = [];

  for(let r=0; r<MAP_SIZE; r++) {
    let row = [];
    for(let c=0; c<MAP_SIZE; c++) {
      if(r===0 || r===MAP_SIZE-1 || c===0 || c===MAP_SIZE-1) {
        row.push(1);
      } else if(r % 4 === 0 && c % 4 === 0 && Math.random() > 0.3) {
        row.push(1);
      } else {
        row.push(0);
        if(r > 4 && c > 4 && !(r === MAP_SIZE-2 && c === MAP_SIZE-2)) {
          freeTiles.push({r, c});
        }
      }
    }
    mapData.push(row);
  }
  
  // 플레이어 스폰 주변 안전지대
  mapData[1][1] = 0; mapData[1][2] = 0;
  mapData[2][1] = 0; mapData[2][2] = 0;

  // 괴물 전용 안전 출발 통로 (절대 벽이 들어설 수 없는 공간)
  mapData[10][10] = 0; mapData[10][11] = 0; mapData[10][12] = 0;
  mapData[11][10] = 0; mapData[11][11] = 0; mapData[11][12] = 0;
  mapData[12][10] = 0; mapData[12][11] = 0; mapData[12][12] = 0;

  mapData[3][3] = 2;
  mapData[8][12] = 2;
  mapData[12][8] = 2;
  mapData[18][18] = 2;

  if(freeTiles.length > 0) {
    let randomIndex = Math.floor(Math.random() * freeTiles.length);
    let keyPos = freeTiles[randomIndex];
    mapData[keyPos.r][keyPos.c] = 3;
  }

  mapData[MAP_SIZE-2][MAP_SIZE-2] = 4;
}
generateMap();

function renderMap() {
  const container = document.getElementById('tiles');
  let html = '';
  for(let r=0; r<MAP_SIZE; r++) {
    for(let c=0; c<MAP_SIZE; c++) {
      const type = mapData[r][c];
      let tileClass = 'floor';
      let content = '';

      if(type === 1) tileClass = 'wall';
      else if(type === 2) tileClass = 'cab';
      else if(type === 3) { tileClass = 'key-item'; content = keySVG; }
      else if(type === 4) { tileClass = 'door'; content = 'START'; }

      html += `<div class="tile ${tileClass}" style="left:${c*TILE_SIZE}px; top:${r*TILE_SIZE}px;">${content}</div>`;
    }
  }
  container.innerHTML = html;
}
renderMap();

let px = 100, py = 100;
// 괴물 시작 위치: 빈 공간이 확정된 (11, 11) 타일의 중심 좌표
let mx = 11 * TILE_SIZE + 20, my = 11 * TILE_SIZE + 20;
let hp = 3, hasKey = false;
let isHidden = false, isChased = false, isQTEActive = false, gameEnded = false;
let isPaused = true;
let keysPressed = {};

let stealthTimer = 0;
let targetKey = 'W';
let hideTimer = MAX_HIDE_TIME;
let requiredPresses = 5;

let mTargetX = 11 * TILE_SIZE + 20, mTargetY = 11 * TILE_SIZE + 20;

function startGame(type) {
  playLockerSound();
  document.getElementById('title').classList.add('hidden');
  document.getElementById('world').classList.remove('hidden');
  document.getElementById('player').innerHTML = type === 'male' ? maleSVG : femaleSVG;
  document.getElementById('monster').innerHTML = monsterSVG;
  pickMonsterNewTarget();
  requestAnimationFrame(gameLoop);
}

function closeTutorial() {
  playLockerSound();
  document.getElementById('tutorialNotice').classList.add('hidden');
  isPaused = false;
}

document.addEventListener('keydown', e => {
  if(isPaused) return;

  const k = e.key.toLowerCase();
  keysPressed[k] = true;

  if(e.key === 'e' || e.key === 'E') {
    handleInteraction();
    return;
  }

  if(isHidden && isQTEActive && ['w','a','s','d'].includes(k)) {
    handleHideInput(k.toUpperCase());
  }
});

document.addEventListener('keyup', e => keysPressed[e.key.toLowerCase()] = false);

// 사방 12px 범위를 검사하여 박스 충돌 판정
function isSolid(x, y) {
  const r = 12;
  const points = [
    {x: x - r, y: y - r},
    {x: x + r, y: y - r},
    {x: x - r, y: y + r},
    {x: x + r, y: y + r}
  ];

  for(let p of points) {
    let col = Math.floor(p.x / TILE_SIZE);
    let row = Math.floor(p.y / TILE_SIZE);
    if(row < 0 || row >= MAP_SIZE || col < 0 || col >= MAP_SIZE) return true;
    if(mapData[row][col] === 1) return true;
  }
  return false;
}

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

  const pCol = Math.floor(px / TILE_SIZE);
  const pRow = Math.floor(py / TILE_SIZE);
  const tileType = mapData[pRow][pCol];

  if(tileType === 2) {
    document.getElementById('mission').textContent = '[E] 키를 눌러 캐비닛에 숨으세요!';
  } else if(tileType === 3) {
    document.getElementById('mission').textContent = '[E] 키를 눌러 열쇠를 줍으세요!';
  } else if(tileType === 4) {
    if(hasKey) document.getElementById('mission').textContent = '[E] 키를 눌러 본 게임 스타트 문으로 이동하세요!';
    else document.getElementById('mission').textContent = '스타트 문입니다. 열쇠가 필요합니다!';
  } else if(!hasKey) {
    document.getElementById('mission').textContent = '[튜토리얼] 랜덤 위치의 열쇠를 찾으세요!';
  } else {
    document.getElementById('mission').textContent = '[튜토리얼 완료 가능] START 문(우측 하단)으로 이동하세요!';
  }
}

function handleInteraction() {
  const pCol = Math.floor(px / TILE_SIZE);
  const pRow = Math.floor(py / TILE_SIZE);
  const tileType = mapData[pRow][pCol];

  if(isHidden) {
    if(!isQTEActive) {
      exitCabinetSafe();
    }
    return;
  }

  if(tileType === 2) {
    playLockerSound();
    
    let monsterDist = Math.hypot(px - mx, py - my);
    
    if(isChased || monsterDist < 260) {
      isHidden = true;
      isQTEActive = true;
      
      mx = px + 15;
      my = py + 20;

      document.getElementById('hideUI').classList.remove('hidden');
      document.getElementById('qteBox').classList.remove('hidden');
      document.getElementById('safeBox').classList.add('hidden');
      
      hideTimer = MAX_HIDE_TIME;
      requiredPresses = 5;
      document.getElementById('reqCount').textContent = requiredPresses;
      document.getElementById('gaugeBar').style.width = '100%';
      nextHideKey();
    } 
    else {
      isHidden = true;
      isQTEActive = false;
      document.getElementById('hideUI').classList.remove('hidden');
      document.getElementById('qteBox').classList.add('hidden');
      document.getElementById('safeBox').classList.remove('hidden');
    }
  } 
  else if(tileType === 3) {
    hasKey = true;
    mapData[pRow][pCol] = 0;
    renderMap();
    document.getElementById('keyCount').textContent = '1';
    document.getElementById('mission').textContent = '열쇠 획득! 스타트 문으로 이동하세요!';
  }
  else if(tileType === 4) {
    if(hasKey) win();
  }
}

function pickMonsterNewTarget() {
  let validTiles = [];
  for(let r = 1; r < MAP_SIZE - 1; r++) {
    for(let c = 1; c < MAP_SIZE - 1; c++) {
      if(mapData[r][c] === 0) {
        validTiles.push({r, c});
      }
    }
  }

  if(validTiles.length > 0) {
    let pick = validTiles[Math.floor(Math.random() * validTiles.length)];
    mTargetX = pick.c * TILE_SIZE + 20;
    mTargetY = pick.r * TILE_SIZE + 20;
  }
}

function updateMonster() {
  if(isHidden && isQTEActive) {
    document.getElementById('alert').style.display = 'block';
    return;
  }

  let dist = Math.hypot(px - mx, py - my);
  
  // 추격 상태
  if(dist < 260 && !isHidden && stealthTimer <= 0) {
    isChased = true;
    document.getElementById('alert').style.display = 'block';
    
    let speed = 2.9;
    let angle = Math.atan2(py - my, px - mx);
    let vx = Math.cos(angle) * speed;
    let vy = Math.sin(angle) * speed;

    let movedX = false, movedY = false;

    if(!isSolid(mx + vx, my)) {
      mx += vx;
      movedX = true;
    }
    if(!isSolid(mx, my + vy)) {
      my += vy;
      movedY = true;
    }

    // 완전히 막혔을 때 탈출(우회) 로직
    if(!movedX && !movedY) {
      if(!isSolid(mx + speed, my)) mx += speed;
      else if(!isSolid(mx - speed, my)) mx -= speed;
      else if(!isSolid(mx, my + speed)) my += speed;
      else if(!isSolid(mx, my - speed)) my -= speed;
    }

    if(dist < 28) lose("괴물에게 붙잡혔습니다!");
  } 
  // 배회(순찰) 상태
  else {
    isChased = false;
    document.getElementById('alert').style.display = 'none';
    
    let tDist = Math.hypot(mTargetX - mx, mTargetY - my);
    if(tDist < 25) {
      pickMonsterNewTarget();
    } else {
      let speed = 1.8;
      let angle = Math.atan2(mTargetY - my, mTargetX - mx);
      let vx = Math.cos(angle) * speed;
      let vy = Math.sin(angle) * speed;

      let movedX = false, movedY = false;
      if(!isSolid(mx + vx, my)) { mx += vx; movedX = true; }
      if(!isSolid(mx, my + vy)) { my += vy; movedY = true; }

      // 배회 도중 벽에 막히면 목표 지점을 새로 갱신
      if(!movedX && !movedY) {
        pickMonsterNewTarget();
      }
    }
  }
}

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

function nextHideKey() {
  const keys = ['W', 'A', 'S', 'D'];
  targetKey = keys[Math.floor(Math.random() * 4)];
  document.getElementById('keyDisplay').textContent = targetKey;
}

function handleHideInput(k) {
  if(k === targetKey) {
    requiredPresses--;
    document.getElementById('reqCount').textContent = requiredPresses;
    if(requiredPresses <= 0) {
      exitCabinetQTESuccess();
      return;
    }
    nextHideKey();
  } else {
    hp--;
    document.getElementById('hp').textContent = hp;
    if(hp <= 0) lose("캐비닛 안에서 소음을 내 잡히고 말았습니다!");
  }
}

function updateHideLogic(dt) {
  if(!isQTEActive) return;
  
  hideTimer -= dt;
  let percentage = Math.max(0, (hideTimer / MAX_HIDE_TIME) * 100);
  document.getElementById('gaugeBar').style.width = percentage + '%';
  
  if(hideTimer <= 0) {
    lose("시간 내에 숨소리를 조절하지 못해 괴물에게 캐비닛이 열렸습니다!");
  }
}

function exitCabinetQTESuccess() {
  isQTEActive = false;
  isChased = false;
  
  pickMonsterNewTarget();
  mx = mTargetX; 
  my = mTargetY;
  stealthTimer = 2.0;

  document.getElementById('qteBox').classList.add('hidden');
  document.getElementById('safeBox').classList.remove('hidden');
  document.getElementById('mission').textContent = '괴물이 당신을 놓치고 떠났습니다! 원하는 때에 [E] 키를 눌러 나가세요.';
}

function exitCabinetSafe() {
  playLockerSound();
  isHidden = false;
  document.getElementById('hideUI').classList.add('hidden');
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

  if(!isPaused) {
    if(stealthTimer > 0) stealthTimer -= dt;

    if(!isHidden) {
      updatePlayer();
    } else if(isQTEActive) {
      updateHideLogic(dt);
    }

    updateMonster();
    updateCamera();
    draw();
  }

  requestAnimationFrame(gameLoop);
}
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=700, scrolling=False)
