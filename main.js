const TOTAL_FRAMES = 6572;
const JSON_DIR = "http://localhost:8000/";
const FRAME_DELAY = 33;
const TARGET_W = 640.86;
const TARGET_H = 360;

const chartLine = document.querySelector('.line-chart__line');

if (!chartLine) {
  console.error('Cannot find .line-chart__line on this page.');
} else {
  const chartSvg = chartLine.closest('svg');

  if (!chartSvg) {
    console.error('Found path but not its parent SVG.');
  } else {
    const holder = document.createElement('div');
    holder.className = 'ba-animation-wrapper';

    Object.assign(holder.style, {
      height: TARGET_H + 'px',
      minHeight: TARGET_H + 'px',
      display: 'block',
      boxSizing: 'border-box',
      position: 'relative',
      overflow: 'visible',
      zIndex: 1
    });

    const svgParent = chartSvg.parentElement;
    svgParent.insertBefore(holder, chartSvg);
    holder.appendChild(chartSvg);

    chartSvg.setAttribute('height', TARGET_H);
    chartSvg.style.height = TARGET_H + 'px';

    const existingViewBox = chartSvg.getAttribute('viewBox');

    if (!existingViewBox) {
      chartSvg.setAttribute('viewBox', `0 $${TARGET_H}`);
    }

    let ancestor = holder.parentElement;

    for (let step = 0; ancestor && ancestor !== document.body && step < 12; step++) {
      const computed = window.getComputedStyle(ancestor);

      if (computed.display.includes('flex') || computed.display.includes('grid')) {
        ancestor.style.flex = ancestor.style.flex || '0 0 auto';
      }

      ancestor.style.maxHeight = ancestor.style.maxHeight || 'none';

      if (computed.overflow !== 'visible') {
        ancestor.style.overflow = 'visible';
      }

      ancestor.style.minHeight = ancestor.style.minHeight || TARGET_H + 'px';

      ancestor = ancestor.parentElement;
    }
  }
}

const frameLine = document.querySelector(".line-chart__line");
const frameSvg = frameLine.closest("svg");

frameSvg.setAttribute("width", TARGET_W);
frameSvg.setAttribute("height", TARGET_H);
frameSvg.style.width = TARGET_W + "px";
frameSvg.style.height = TARGET_H + "px";

frameSvg.setAttribute("viewBox", `0 0 ${TARGET_W} ${TARGET_H}`);

function loadFrame(index) {
  const name = `frame_${index.toString().padStart(4, "0")}.json`;

  return fetch(JSON_DIR + name)
    .then(response => response.json())
    .then(payload => {
      frameLine.setAttribute("d", payload.path);
    })
    .catch(error => console.error("Frame error:", name, error));
}

async function play() {
  for (let i = 0; i < TOTAL_FRAMES; i++) {
    await loadFrame(i);
    await new Promise(resolve => setTimeout(resolve, FRAME_DELAY));
  }
}

play();