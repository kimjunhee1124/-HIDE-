// 1. 괴물 목표 지점을 '빈 공간'으로만 선택하는 로직으로 변경
function pickMonsterNewTarget() {
  let validTiles = [];
  for(let r = 2; r < MAP_SIZE - 2; r++) {
    for(let c = 2; c < MAP_SIZE - 2; c++) {
      // 벽이 아니고 캐비닛이 아닌 빈 길(0) 위치만 추려냅니다.
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

// 2. 초기 괴물 위치 세팅 (generateMap 내부)
// 괴물이 시작하자마자 낑기지 않는 확실한 빈 타일(예: 맵 중상단)로 위치 지정
mx = 12 * TILE_SIZE + 20;
my = 12 * TILE_SIZE + 20;

// 3. updateMonster 내부 벽 부딪힘 보완
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
    let nx = mx + Math.cos(angle) * speed;
    let ny = my + Math.sin(angle) * speed;

    let moved = false;
    if(!isSolid(nx, my)) { mx = nx; moved = true; }
    if(!isSolid(mx, ny)) { my = ny; moved = true; }
    
    // 벽에 막혀 전혀 움직이지 못하는 경우 미세 위치 우회
    if(!moved) {
      if(!isSolid(mx + speed, my)) mx += speed;
      else if(!isSolid(mx - speed, my)) mx -= speed;
    }

    if(dist < 28) lose("괴물에게 붙잡혔습니다!");
  } 
  // 정찰 상태
  else {
    isChased = false;
    document.getElementById('alert').style.display = 'none';
    
    let tDist = Math.hypot(mTargetX - mx, mTargetY - my);
    if(tDist < 20) {
      pickMonsterNewTarget();
    } else {
      let speed = 1.8;
      let angle = Math.atan2(mTargetY - my, mTargetX - mx);
      let nx = mx + Math.cos(angle) * speed;
      let ny = my + Math.sin(angle) * speed;

      let movedX = false, movedY = false;
      if(!isSolid(nx, my)) { mx = nx; movedX = true; }
      if(!isSolid(mx, ny)) { my = ny; movedY = true; }

      // 벽에 걸리면 바로 목표 재설정
      if(!movedX && !movedY) {
        pickMonsterNewTarget();
      }
    }
  }
}
