let startTime = null, actionCount = 0, timerHandle = null;

function pad(n) { return String(n).padStart(2, "0"); }

function tickTimer() {
  const e = Math.floor((Date.now() - startTime) / 1000);
  document.getElementById("session-time").textContent =
    `${pad(Math.floor(e/3600))}:${pad(Math.floor(e%3600/60))}:${pad(e%60)}`;
}

async function startBot() {
  const ok = await window.pywebview.api.start_bot();
  if (ok) {
    const dot = document.getElementById("status-dot");
    dot.style.cssText = "background:#FF4655; animation: glow 1.4s ease-in-out infinite;";
    document.getElementById("status").textContent = "ACTIVE";
    document.getElementById("status").style.color = "#FF4655";
    document.getElementById("start-btn").disabled = true;
    document.getElementById("stop-btn").style.cssText = "border: 1px solid rgba(255,70,85,0.6); color: rgba(255,70,85,0.85)";
    document.getElementById("stop-btn").disabled = false;
    startTime = Date.now(); actionCount = 0;
    document.getElementById("action-count").textContent = "0";
    timerHandle = setInterval(tickTimer, 1000);
  }
}

async function stopBot() {
  await window.pywebview.api.stop_bot();
  const dot = document.getElementById("status-dot");
  dot.style.cssText = "background: rgba(255,255,255,0.1); animation: none;";
  document.getElementById("status").textContent = "STANDBY";
  document.getElementById("status").style.color = "rgba(255,255,255,0.25)";
  document.getElementById("start-btn").disabled = false;
  document.getElementById("stop-btn").style.cssText = "border: 1px solid rgba(255,70,85,0.25); color: rgba(255,70,85,0.35)";
  document.getElementById("stop-btn").disabled = true;
  clearInterval(timerHandle); startTime = null;
}

function on_action() {
  actionCount++;
  document.getElementById("action-count").textContent = actionCount;
}
function update_status(running) { if (running) startBot(); else stopBot(); }

