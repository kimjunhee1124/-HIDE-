
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HIDE - Pixel School", page_icon="👻", layout="wide")

GAME_HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box}
body{
  margin:0;background:#111;color:#fff;font-family:monospace;
  overflow:hidden;
}
#wrap{display:flex;justify-content:center;align-items:center;min-height:760px}
#game{
  position:relative;width:1100px;height:700px;
  background:#242831;border:4px solid #111;overflow:hidden;
  image-rendering:pixelated;box-shadow:0 0 0 3px #59606b;
}
.screen{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.hidden{display:none!important}
#title{flex-direction:column;background:#15181d}
.title{
  font-size:64px;letter-spacing:8px;text-shadow:5px 5px #000;
  margin-bottom:20px
}
.sub{color:#aeb7c4;margin-bottom:35px;font-size:18px}
.selects{display:flex;gap:30px}
.pick{
  width:240px;height:270px;background:#252b34;border:4px solid #586170;
  cursor:pointer;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:15px
}
.pick:hover{border-color:#fff;transform:translateY(-3px)}
.pick b{font-size:22px}

#hud{
  position:absolute;z-index:20;left:15px;top:12px;right:15px;
  display:flex;justify-content:space-between;pointer-events:none
}
.panel{
  background:#111c;border:3px solid #69717d;padding:8px 12px;
  box-shadow:3px 3px #000;font-size:15px
}
#hp{color:#ff4d55}
#msg{
  position:absolute;z-index:30;left:50%;top:50%;transform:translate(-50%,-50%);
  background:#111;border:4px solid #fff;padding:25px 40px;text-align:center;
  box-shadow:8px 8px #000;display:none
}
#msg h2{margin:0 0 12px;font-size:35px}
#msg button,.bigbtn{
  background:#303744;color:#fff;border:3px solid #aab2bd;padding:10px 18px;
  font-family:monospace;font-weight:bold;cursor:pointer
}
#msg button:hover,.bigbtn:hover{background:#465061}

#map{
  position:absolute;inset:0;
  background:
   linear-gradient(#0002 1px,transparent 1px),
   linear-gradient(90deg,#0002 1px,transparent 1px),
   #6c7075;
  background-size:50px 50px;
}
.wall{
  position:absolute;background:#343941;border:4px solid #1a1d22;
  box-shadow:inset 0 0 0 3px #505762
}
.cab{
  position:absolute;width:48px;height:66px;background:#875b38;
  border:4px solid #3b2518;box-shadow:inset 4px 0 #a8774d,inset -4px 0 #604126;
}
.cab:after{content:"";position:absolute;left:20px;top:28px;width:5px;height:5px;background:#1b130e}
.exit{
  position:absolute;width:58px;height:72px;background:#25333b;border:5px solid #111;
  display:flex;align-items:center;justify-content:center;font-size:26px
}
.exit span{background:#2c9b56;padding:2px 5px}

.sprite{
  position:absolute;width:50px;height:66px;z-index:10;
  transform:translate(-50%,-50%);
  image-rendering:pixelated;
}
.sprite svg{width:50px;height:66px;shape-rendering:crispEdges}
.shadow{
  position:absolute;width:42px;height:14px;border-radius:50%;
  background:#0006;transform:translate(-50%,-50%);z-index:5
}
#monster{z-index:12}
#alert{
 position:absolute;z-index:25;left:50%;top:88px;transform:translateX(-50%);
 font-size:30px;background:#fff;color:#d11;border:3px solid #111;
 padding:2px 10px;display:none;box-shadow:4px 4px #000
}

#hideUI{
 position:absolute;z-index:40;inset:0;background:#090a0d;
 display:flex;flex-direction:column;align-items:center;justify-content:center
}
#hideUI h2{font-size:35px;margin:0 0 8px}
#hideUI p{color:#aeb7c4}
#key{
 width:130px;height:130px;border:6px solid #ddd;background:#30343b;
 display:flex;align-items:center;justify-content:center;
 font-size:70px;font-weight:bold;margin:20px
}
#timer{font-size:24px}
#keyBtns{display:grid;grid-template-columns:60px 60px 60px;gap:5px}
.k{height:55px;background:#353b45;border:3px solid #8c95a2;color:white;font:bold 22px monospace}
.k:nth-child(1){grid-column:2}
.k:nth-child(2){grid-column:1}.k:nth-child(3){grid-column:2}.k:nth-child(4){grid-column:3}
.note{color:#8f98a6;margin-top:15px}

#gameover{background:#090a0d;flex-direction:column}
#gameover h1{font-size:60px;margin:0 0 10px}
</style>
</head>
<body>
<div id="wrap">
<div id="game">

<div id="title" class="screen">
  <div class="title">HIDE</div>
  <div class="sub">학교 안에서 무언가가 너를 쫓아온다.</div>
  <div class="selects">
    <div class="pick" onclick="startGame('male')">
      <div id="malePreview"></div><b>남학생</b>
    </div>
    <div class="pick" onclick="startGame('female')">
      <div id="femalePreview"></div><b>여학생</b>
    </div>
  </div>
  <div class="note">방향키 / WASD로 이동 · 캐비닛에 가까이 가서 E</div>
</div>

<div id="world" class="screen hidden">
  <div id="map">
    <div class="wall" style="left:0;top:0;width:1100px;height:55px"></div>
    <div class="wall" style="left:0;bottom:0;width:1100px;height:55px"></div>
    <div class="wall" style="left:0;top:0;width:55px;height:700px"></div>
    <div class="wall" style="right:0;top:0;width:55px;height:700px"></div>
    <div class="wall" style="left:250px;top:125px;width:430px;height:45px"></div>
    <div class="wall" style="left:250px;top:125px;width:45px;height:220px"></div>
    <div class="wall" style="left:680px;top:125px;width:45px;height:220px"></div>
    <div class="wall" style="left:250px;top:300px;width:180px;height:45px"></div>
    <div class="wall" style="left:545px;top:300px;width:180px;height:45px"></div>

    <div class="cab" style="left:120px;top:160px"></div>
    <div class="cab" style="left:860px;top:470px"></div>
    <div class="cab" style="left:850px;top:170px"></div>
    <div class="exit" style="left:965px;top:65px"><span>↗</span></div>

    <div id="pShadow" class="shadow"></div>
    <div id="mShadow" class="shadow"></div>
    <div id="player" class="sprite"></div>
    <div id="monster" class="sprite"></div>
  </div>

  <div id="hud">
    <div class="panel">❤️ <span id="hp">3</span>　소음: <span id="noise">0</span>%</div>
    <div class="panel">목표: <span id="objective">출구로 이동</span></div>
  </div>
  <div id="alert">!</div>
</div>

<div id="hideUI" class="hidden">
  <h2>캐비닛 안에 숨었다!</h2>
  <p>화면에 나타난 키를 빠르게 눌러 버텨!</p>
  <div id="key">W</div>
  <div id="timer">남은 시간 8.0초</div>
  <div id="keyBtns">
    <button class="k" onclick="pressKey('W')">W</button>
    <button class="k" onclick="pressKey('A')">A</button>
    <button class="k" onclick="pressKey('S')">S</button>
    <button class="k" onclick="pressKey('D')">D</button>
  </div>
  <div class="note">키보드 W A S D도 사용할 수 있어.</div>
</div>

<div id="gameover" class="screen hidden">
  <h1>GAME OVER</h1>
  <p id="overText">잡혔다!</p>
  <button class="bigbtn" onclick="location.reload()">다시 시작</button>
</div>

<div id="msg">
  <h2 id="msgTitle"></h2><p id="msgText"></p>
  <button onclick="location.reload()">다시 시작</button>
</div>
</div>
</div>

<script>
// 실제 도트처럼 보이도록 SVG를 코드 안에서 직접 픽셀 블록으로 구성
const male = `
<svg viewBox="0 0 25 33" xmlns="http://www.w3.org/2000/svg">
<rect x="7" y="2" width="11" height="9" fill="#26242b"/>
<rect x="5" y="5" width="15" height="7" fill="#26242b"/>
<rect x="8" y="7" width="3" height="3" fill="#f1c4a5"/>
<rect x="14" y="7" width="3" height="3" fill="#f1c4a5"/>
<rect x="6" y="11" width="13" height="8" fill="#f1c4a5"/>
<rect x="7" y="11" width="11" height="2" fill="#302b31"/>
<rect x="8" y="15" width="3" height="1" fill="#302b31"/>
<rect x="14" y="15" width="3" height="1" fill="#302b31"/>
<rect x="6" y="19" width="13" height="8" fill="#263c67"/>
<rect x="9" y="19" width="7" height="3" fill="#f4f4ef"/>
<rect x="11" y="22" width="3" height="3" fill="#d53e49"/>
<rect x="7" y="27" width="5" height="5" fill="#17191f"/>
<rect x="14" y="27" width="5" height="5" fill="#17191f"/>
<rect x="5" y="31" width="8" height="2" fill="#4a3a35"/>
<rect x="13" y="31" width="8" height="2" fill="#4a3a35"/>
</svg>`;

const female = `
<svg viewBox="0 0 25 33" xmlns="http://www.w3.org/2000/svg">
<rect x="5" y="2" width="15" height="11" fill="#4a2d32"/>
<rect x="4" y="6" width="17" height="11" fill="#4a2d32"/>
<rect x="8" y="7" width="3" height="3" fill="#f1c4a5"/>
<rect x="14" y="7" width="3" height="3" fill="#f1c4a5"/>
<rect x="6" y="11" width="13" height="8" fill="#f1c4a5"/>
<rect x="7" y="11" width="11" height="2" fill="#4a2d32"/>
<rect x="8" y="15" width="3" height="1" fill="#302b31"/>
<rect x="14" y="15" width="3" height="1" fill="#302b31"/>
<rect x="6" y="19" width="13" height="8" fill="#263c67"/>
<rect x="9" y="19" width="7" height="3" fill="#f4f4ef"/>
<rect x="11" y="22" width="3" height="3" fill="#d53e49"/>
<rect x="7" y="27" width="5" height="5" fill="#20242d"/>
<rect x="14" y="27" width="5" height="5" fill="#20242d"/>
<rect x="5" y="31" width="8" height="2" fill="#4a3a35"/>
<rect x="13" y="31" width="8" height="2" fill="#4a3a35"/>
</svg>`;

const monster = `
<svg viewBox="0 0 25 33" xmlns="http://www.w3.org/2000/svg">
<rect x="6" y="3" width="13" height="23" fill="#b9b5b5"/>
<rect x="4" y="8" width="17" height="13" fill="#aaa6a6"/>
<rect x="7" y="1" width="11" height="5" fill="#c9c5c5"/>
<rect x="8" y="7" width="9" height="8" fill="#1b1b1e"/>
<rect x="10" y="9" width="3" height="3" fill="#d51d2a"/>
<rect x="15" y="9" width="3" height="3" fill="#d51d2a"/>
<rect x="3" y="17" width="6" height="8" fill="#333338"/>
<rect x="16" y="17" width="6" height="8" fill="#333338"/>
<rect x="6" y="24" width="6" height="7" fill="#333338"/>
<rect x="14" y="24" width="6" height="7" fill="#333338"/>
<rect x="4" y="30" width="8" height="3" fill="#16171a"/>
<rect x="14" y="30" width="8" height="3" fill="#16171a"/>
</svg>`;

document.getElementById('malePreview').innerHTML =
  '<div class="sprite" style="position:relative;transform:none;margin:auto">'+male+'</div>';
document.getElementById('femalePreview').innerHTML =
  '<div class="sprite" style="position:relative;transform:none;margin:auto">'+female+'</div>';

let playerType='male';
let px=180, py=500, mx=760, my=210;
let hp=3, noise=0, running=false, hidden=false, gameEnded=false;
let target='W', hideLeft=8, last=performance.now();
const speed=3.0;

function startGame(type){
  playerType=type;
  document.getElementById('title').classList.add('hidden');
  document.getElementById('world').classList.remove('hidden');
  document.getElementById('player').innerHTML = type==='male' ? male : female;
  document.getElementById('monster').innerHTML = monster;
  requestAnimationFrame(loop);
}

const keys={};
document.addEventListener('keydown',e=>{
  keys[e.key.toLowerCase()]=true;
  if(hidden && ['w','a','s','d'].includes(e.key.toLowerCase())){
    pressKey(e.key.toUpperCase());
  }
  if(e.key.toLowerCase()==='e' && running && !hidden) tryHide();
});
document.addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);

function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function dist(ax,ay,bx,by){return Math.hypot(ax-bx,ay-by)}

function blocked(x,y){
  if(x<80||x>1020||y<90||y>620) return true;
  // inner wall collision
  const rects=[
    [250,125,680,170],[250,125,295,345],[680,125,725,345],
    [250,300,430,345],[545,300,725,345]
  ];
  for(const r of rects){
    if(x>r[0]-18&&x<r[2]+18&&y>r[1]-18&&y<r[3]+18) return true;
  }
  return false;
}

function updatePlayer(){
  let dx=0,dy=0;
  if(keys['w']||keys['arrowup'])dy-=1;
  if(keys['s']||keys['arrowdown'])dy+=1;
  if(keys['a']||keys['arrowleft'])dx-=1;
  if(keys['d']||keys['arrowright'])dx+=1;
  if(dx||dy){
    const l=Math.hypot(dx,dy);dx/=l;dy/=l;
    const nx=px+dx*speed, ny=py+dy*speed;
    if(!blocked(nx,py))px=nx;
    if(!blocked(px,ny))py=ny;
    noise=clamp(noise+0.08,0,100);
  }else{
    noise=clamp(noise-0.04,0,100);
  }
}

function updateMonster(dt){
  const d=dist(px,py,mx,my);
  if(d<330 && !hidden){
    const dx=(px-mx)/Math.max(d,1), dy=(py-my)/Math.max(d,1);
    const ms=1.15+noise/100*1.4;
    const nx=mx+dx*ms, ny=my+dy*ms;
    if(!blocked(nx,my))mx=nx;
    if(!blocked(mx,ny))my=ny;
    document.getElementById('alert').style.display='block';
  }else{
    document.getElementById('alert').style.display='none';
  }
  if(d<34 && !hidden) lose('괴물에게 잡혔어!');
}

function draw(){
  const p=document.getElementById('player'),m=document.getElementById('monster');
  p.style.left=px+'px';p.style.top=py+'px';
  m.style.left=mx+'px';m.style.top=my+'px';
  document.getElementById('pShadow').style.left=px+'px';
  document.getElementById('pShadow').style.top=(py+24)+'px';
  document.getElementById('mShadow').style.left=mx+'px';
  document.getElementById('mShadow').style.top=(my+24)+'px';
  document.getElementById('noise').textContent=Math.round(noise);
  document.getElementById('hp').textContent=hp;
}

function tryHide(){
  const cabs=[[144,193],[884,503],[874,203]];
  let nearest=999;
  for(const c of cabs)nearest=Math.min(nearest,dist(px,py,c[0],c[1]));
  if(nearest<80) beginHide();
}

function beginHide(){
  hidden=true;
  document.getElementById('world').classList.add('hidden');
  document.getElementById('hideUI').classList.remove('hidden');
  hideLeft=8; newTarget();
}

function newTarget(){
  target=['W','A','S','D'][Math.floor(Math.random()*4)];
  document.getElementById('key').textContent=target;
}

function pressKey(k){
  if(!hidden)return;
  if(k===target){
    hideLeft=Math.min(8,hideLeft+0.35);
    newTarget();
  }else{
    hp--;
    hideLeft-=0.8;
    if(hp<=0 || hideLeft<=0) lose('버티지 못했어!');
  }
}

function endHide(){
  hidden=false;
  document.getElementById('hideUI').classList.add('hidden');
  document.getElementById('world').classList.remove('hidden');
  // 괴물이 잠깐 다른 곳으로 이동
  mx=760;my=210;
  noise=0;
}

function lose(text){
  if(gameEnded)return;
  gameEnded=true;
  document.getElementById('world').classList.add('hidden');
  document.getElementById('hideUI').classList.add('hidden');
  document.getElementById('gameover').classList.remove('hidden');
  document.getElementById('overText').textContent=text;
}

function win(){
  gameEnded=true;
  document.getElementById('world').classList.add('hidden');
  document.getElementById('msg').style.display='block';
  document.getElementById('msgTitle').textContent='탈출 성공!';
  document.getElementById('msgText').textContent='학교를 무사히 빠져나왔다.';
}

function loop(now){
  if(gameEnded)return;
  const dt=Math.min((now-last)/1000,0.05); last=now;

  if(!hidden){
    updatePlayer();
    updateMonster(dt);
    draw();

    // 출구
    if(px>930 && py<145) win();
  }else{
    hideLeft-=dt;
    document.getElementById('timer').textContent='남은 시간 '+Math.max(0,hideLeft).toFixed(1)+'초';
    if(hideLeft<=0) endHide();
  }
  requestAnimationFrame(loop);
}
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=760, scrolling=False)
