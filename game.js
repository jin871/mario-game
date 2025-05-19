const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let marioX = 50;
let marioY = 300;
let velocityY = 0;
let gravity = 1;
let isJumping = false;

document.addEventListener("keydown", function (e) {
  if (e.code === "Space" && !isJumping) {
    velocityY = -15;
    isJumping = true;
  }
});

function update() {
  velocityY += gravity;
  marioY += velocityY;

  if (marioY > 300) {
    marioY = 300;
    velocityY = 0;
    isJumping = false;
  }
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // マリオ（赤い四角）
  ctx.fillStyle = "red";
  ctx.fillRect(marioX, marioY, 30, 30);
}

function gameLoop() {
  update();
  draw();
  requestAnimationFrame(gameLoop);
}

gameLoop();
