import { useState, useCallback, useRef, useEffect } from "react";

const SCENARIOS = {
  baseline: { name: "Baseline Economy", maxFood: 100, maxTech: 80, curvature: 2, description: "A balanced economy with standard resources" },
  covid: { name: "COVID-19 Pandemic", maxFood: 100, maxTech: 55, curvature: 2.2, description: "Supply chains disrupted, tech production capacity reduced" },
  techBoom: { name: "Tech Revolution", maxFood: 100, maxTech: 120, curvature: 1.8, description: "New technology expands production possibilities for tech goods" },
  wartime: { name: "Wartime Economy", maxFood: 70, maxTech: 50, curvature: 2.5, description: "Resources diverted, capacity shrinks on both axes" },
  investment: { name: "After Investment", maxFood: 130, maxTech: 110, curvature: 1.9, description: "Years of capital investment expanded the frontier outward" },
};

function ppfY(x, maxX, maxY, curvature) {
  const ratio = x / maxX;
  return maxY * Math.pow(1 - Math.pow(ratio, curvature), 1 / curvature);
}

function ppfPoints(maxX, maxY, curvature, steps = 200) {
  const pts = [];
  for (let i = 0; i <= steps; i++) {
    const x = (i / steps) * maxX;
    const y = ppfY(x, maxX, maxY, curvature);
    pts.push({ x, y });
  }
  return pts;
}

function marginalOC(x, maxX, maxY, curvature) {
  const dx = 0.5;
  const y1 = ppfY(x, maxX, maxY, curvature);
  const y2 = ppfY(Math.min(x + dx, maxX), maxX, maxY, curvature);
  return Math.abs((y2 - y1) / dx);
}

const W = 520, H = 420, PAD = 60, PB = 50, PR = 30;
const plotW = W - PAD - PR, plotH = H - PB - 20;

function toSVG(x, y, maxX, maxY) {
  return { sx: PAD + (x / maxX) * plotW, sy: 20 + plotH - (y / maxY) * plotH };
}

export default function PPFExplorer() {
  const [scenario, setScenario] = useState("baseline");
  const [compareScenario, setCompareScenario] = useState(null);
  const [pointX, setPointX] = useState(50);
  const [dragging, setDragging] = useState(false);
  const [showSteps, setShowSteps] = useState(false);
  const svgRef = useRef(null);

  const sc = SCENARIOS[scenario];
  const compSc = compareScenario ? SCENARIOS[compareScenario] : null;
  const maxAxisX = Math.max(sc.maxFood, compSc?.maxFood || 0, 140);
  const maxAxisY = Math.max(sc.maxTech, compSc?.maxTech || 0, 130);

  const clampedX = Math.min(pointX, sc.maxFood);
  const currentY = ppfY(clampedX, sc.maxFood, sc.maxTech, sc.curvature);
  const moc = marginalOC(clampedX, sc.maxFood, sc.maxTech, sc.curvature);
  const points = ppfPoints(sc.maxFood, sc.maxTech, sc.curvature);
  const compPoints = compSc ? ppfPoints(compSc.maxFood, compSc.maxTech, compSc.curvature) : [];

  const ptSVG = toSVG(clampedX, currentY, maxAxisX, maxAxisY);

  const pathD = points.map((p, i) => {
    const { sx, sy } = toSVG(p.x, p.y, maxAxisX, maxAxisY);
    return `${i === 0 ? "M" : "L"}${sx},${sy}`;
  }).join(" ");

  const compPathD = compPoints.map((p, i) => {
    const { sx, sy } = toSVG(p.x, p.y, maxAxisX, maxAxisY);
    return `${i === 0 ? "M" : "L"}${sx},${sy}`;
  }).join(" ");

  const handleMouseMove = useCallback((e) => {
    if (!dragging || !svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const dataX = ((mouseX - PAD) / plotW) * maxAxisX;
    setPointX(Math.max(0, Math.min(dataX, sc.maxFood)));
  }, [dragging, maxAxisX, sc.maxFood]);

  const handleTouchMove = useCallback((e) => {
    if (!dragging || !svgRef.current) return;
    e.preventDefault();
    const rect = svgRef.current.getBoundingClientRect();
    const touchX = e.touches[0].clientX - rect.left;
    const dataX = ((touchX - PAD) / plotW) * maxAxisX;
    setPointX(Math.max(0, Math.min(dataX, sc.maxFood)));
  }, [dragging, maxAxisX, sc.maxFood]);

  useEffect(() => {
    if (dragging) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", () => setDragging(false));
      window.addEventListener("touchmove", handleTouchMove, { passive: false });
      window.addEventListener("touchend", () => setDragging(false));
    }
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", () => setDragging(false));
      window.removeEventListener("touchmove", handleTouchMove);
      window.removeEventListener("touchend", () => setDragging(false));
    };
  }, [dragging, handleMouseMove, handleTouchMove]);

  const gridLines = [];
  for (let v = 20; v < maxAxisX; v += 20) {
    const { sx } = toSVG(v, 0, maxAxisX, maxAxisY);
    gridLines.push(<line key={`gx${v}`} x1={sx} y1={20} x2={sx} y2={20 + plotH} stroke="var(--text-color)" opacity="0.06" />);
    gridLines.push(<text key={`tx${v}`} x={sx} y={20 + plotH + 16} textAnchor="middle" fill="var(--text-color)" opacity="0.5" fontSize="11">{v}</text>);
  }
  for (let v = 20; v < maxAxisY; v += 20) {
    const { sy } = toSVG(0, v, maxAxisX, maxAxisY);
    gridLines.push(<line key={`gy${v}`} x1={PAD} y1={sy} x2={PAD + plotW} y2={sy} stroke="var(--text-color)" opacity="0.06" />);
    gridLines.push(<text key={`ty${v}`} x={PAD - 8} y={sy + 4} textAnchor="end" fill="var(--text-color)" opacity="0.5" fontSize="11">{v}</text>);
  }

  const steps = [
    { food: 0, label: "All Tech" },
    { food: sc.maxFood * 0.25, label: "Mostly Tech" },
    { food: sc.maxFood * 0.5, label: "Balanced" },
    { food: sc.maxFood * 0.75, label: "Mostly Food" },
    { food: sc.maxFood, label: "All Food" },
  ];

  return (
    <div style={{ fontFamily: "'Source Serif 4', 'Georgia', serif", maxWidth: 900, margin: "0 auto", padding: "24px 16px", color: "var(--text-color)" }}>
      <h1 style={{ fontSize: 22, fontWeight: 700, marginBottom: 2, letterSpacing: "-0.3px" }}>
        Production Possibilities Frontier
      </h1>
      <p style={{ fontSize: 13, opacity: 0.6, marginBottom: 20, fontFamily: "'DM Sans', sans-serif" }}>
        Chapter 1 &mdash; Case, Fair & Oster &middot; Drag the point along the frontier to explore tradeoffs
      </p>

      <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
        <div style={{ flex: "1 1 520px", minWidth: 320 }}>
          <svg ref={svgRef} viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", background: "var(--bg-color)", borderRadius: 8, border: "1px solid var(--border-color)", cursor: dragging ? "grabbing" : "default", touchAction: "none" }}>
            {gridLines}
            <line x1={PAD} y1={20} x2={PAD} y2={20 + plotH} stroke="var(--text-color)" opacity="0.3" />
            <line x1={PAD} y1={20 + plotH} x2={PAD + plotW} y2={20 + plotH} stroke="var(--text-color)" opacity="0.3" />
            <text x={PAD + plotW / 2} y={H - 6} textAnchor="middle" fill="var(--text-color)" fontSize="13" fontWeight="600">Food (units)</text>
            <text x={16} y={20 + plotH / 2} textAnchor="middle" fill="var(--text-color)" fontSize="13" fontWeight="600" transform={`rotate(-90, 16, ${20 + plotH / 2})`}>Technology (units)</text>

            {compSc && <path d={compPathD} fill="none" stroke="#f59e0b" strokeWidth="2" strokeDasharray="6 4" opacity="0.6" />}

            <path d={`${pathD} L${PAD + (sc.maxFood / maxAxisX) * plotW},${20 + plotH} L${PAD},${20 + plotH} Z`} fill="var(--text-color)" opacity="0.04" />
            <path d={pathD} fill="none" stroke="#2563eb" strokeWidth="2.5" />

            <line x1={ptSVG.sx} y1={ptSVG.sy} x2={ptSVG.sx} y2={20 + plotH} stroke="#2563eb" strokeDasharray="4 3" opacity="0.4" />
            <line x1={ptSVG.sx} y1={ptSVG.sy} x2={PAD} y2={ptSVG.sy} stroke="#2563eb" strokeDasharray="4 3" opacity="0.4" />

            {showSteps && steps.map((s, i) => {
              const sy = ppfY(s.food, sc.maxFood, sc.maxTech, sc.curvature);
              const { sx, sy: ssy } = toSVG(s.food, sy, maxAxisX, maxAxisY);
              return <g key={i}>
                <circle cx={sx} cy={ssy} r={4} fill="#f59e0b" stroke="#fff" strokeWidth="1.5" />
                <text x={sx} y={ssy - 10} textAnchor="middle" fontSize="10" fill="var(--text-color)" opacity="0.7">{s.label}</text>
              </g>;
            })}

            <circle cx={ptSVG.sx} cy={ptSVG.sy} r={8} fill="#2563eb" stroke="#fff" strokeWidth="2.5"
              style={{ cursor: "grab", filter: "drop-shadow(0 2px 4px rgba(37,99,235,0.3))" }}
              onMouseDown={() => setDragging(true)}
              onTouchStart={() => setDragging(true)} />

            <text x={ptSVG.sx} y={20 + plotH + 30} textAnchor="middle" fill="#2563eb" fontSize="12" fontWeight="700">{clampedX.toFixed(0)}</text>
            <text x={PAD - 28} y={ptSVG.sy + 4} textAnchor="middle" fill="#2563eb" fontSize="12" fontWeight="700">{currentY.toFixed(0)}</text>
          </svg>
        </div>

        <div style={{ flex: "1 1 280px", minWidth: 260, fontFamily: "'DM Sans', sans-serif", fontSize: 13 }}>
          <div style={{ background: "var(--bg-color)", border: "1px solid var(--border-color)", borderRadius: 8, padding: 16, marginBottom: 12 }}>
            <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 10 }}>Current Production</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
              <div style={{ background: "var(--secondary-bg)", borderRadius: 6, padding: "8px 10px" }}>
                <div style={{ opacity: 0.5, fontSize: 11 }}>Food</div>
                <div style={{ fontSize: 20, fontWeight: 700, color: "#2563eb" }}>{clampedX.toFixed(1)}</div>
              </div>
              <div style={{ background: "var(--secondary-bg)", borderRadius: 6, padding: "8px 10px" }}>
                <div style={{ opacity: 0.5, fontSize: 11 }}>Technology</div>
                <div style={{ fontSize: 20, fontWeight: 700, color: "#2563eb" }}>{currentY.toFixed(1)}</div>
              </div>
            </div>
            <div style={{ marginTop: 10, padding: "8px 10px", background: "#fef3c7", borderRadius: 6, color: "#92400e" }}>
              <div style={{ fontSize: 11, fontWeight: 600 }}>Marginal Opportunity Cost</div>
              <div style={{ fontSize: 15, fontWeight: 700 }}>1 more food = {moc.toFixed(2)} tech lost</div>
              <div style={{ fontSize: 11, opacity: 0.7, marginTop: 2 }}>
                {moc < 0.5 ? "Low tradeoff -- food is cheap here" : moc < 1.5 ? "Moderate tradeoff" : "Expensive! Food production is costly at this point"}
              </div>
            </div>
          </div>

          <div style={{ background: "var(--bg-color)", border: "1px solid var(--border-color)", borderRadius: 8, padding: 16, marginBottom: 12 }}>
            <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 8 }}>Scenarios</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
              {Object.entries(SCENARIOS).map(([key, s]) => (
                <button key={key} onClick={() => { setScenario(key); setPointX(Math.min(pointX, s.maxFood)); }}
                  style={{ padding: "6px 10px", borderRadius: 6, border: scenario === key ? "2px solid #2563eb" : "1px solid var(--border-color)",
                    background: scenario === key ? "#2563eb11" : "transparent", cursor: "pointer", textAlign: "left",
                    fontSize: 12, color: "var(--text-color)", fontFamily: "inherit" }}>
                  <span style={{ fontWeight: 600 }}>{s.name}</span>
                </button>
              ))}
            </div>
            <p style={{ fontSize: 11, opacity: 0.6, marginTop: 8, lineHeight: 1.4 }}>{sc.description}</p>
          </div>

          <div style={{ background: "var(--bg-color)", border: "1px solid var(--border-color)", borderRadius: 8, padding: 16, marginBottom: 12 }}>
            <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 8 }}>Compare With</div>
            <select value={compareScenario || ""} onChange={(e) => setCompareScenario(e.target.value || null)}
              style={{ width: "100%", padding: "6px 8px", borderRadius: 6, border: "1px solid var(--border-color)", fontSize: 12, background: "var(--bg-color)", color: "var(--text-color)", fontFamily: "inherit" }}>
              <option value="">None</option>
              {Object.entries(SCENARIOS).filter(([k]) => k !== scenario).map(([key, s]) => (
                <option key={key} value={key}>{s.name}</option>
              ))}
            </select>
            {compSc && <p style={{ fontSize: 11, color: "#f59e0b", marginTop: 6 }}>Dashed orange = {compSc.name}</p>}
          </div>

          <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12, cursor: "pointer" }}>
            <input type="checkbox" checked={showSteps} onChange={(e) => setShowSteps(e.target.checked)} />
            Show step-by-step points along frontier
          </label>
        </div>
      </div>

      <div style={{ marginTop: 20, padding: 16, background: "var(--secondary-bg)", borderRadius: 8, fontSize: 13, lineHeight: 1.6, fontFamily: "'DM Sans', sans-serif" }}>
        <strong>What you're seeing:</strong> This economy produces <strong>{clampedX.toFixed(0)} units of food</strong> and <strong>{currentY.toFixed(0)} units of technology</strong>.
        It's operating <strong>on the frontier</strong> (efficient -- no resources wasted).
        {moc < 0.5 && " At this point, food is cheap to produce because most resources are already in tech. "}
        {moc >= 0.5 && moc < 1.5 && " The tradeoff is moderate here -- resources are reasonably balanced. "}
        {moc >= 1.5 && " Producing more food here is expensive -- the best food-producing resources are already in use, so you're pulling tech-specialized resources into food production. This is increasing opportunity cost in action. "}
        {compareScenario && ` Compared to the ${compSc.name} scenario, the frontier has ${sc.maxFood * sc.maxTech > compSc.maxFood * compSc.maxTech ? "expanded" : "contracted"} -- meaning the economy can produce ${sc.maxFood * sc.maxTech > compSc.maxFood * compSc.maxTech ? "more" : "less"} of everything.`}
      </div>
    </div>
  );
}
