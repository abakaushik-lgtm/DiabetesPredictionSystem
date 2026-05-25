/* ==========================================================================
   Dual-Theme Quantum Core & Clinical Diagnostics Engine Script
   ========================================================================== */

// DOM Elements
const body = document.body;
const predictionForm = document.getElementById('prediction-form');
const output = document.getElementById('prediction-output');
const statusText = document.getElementById('status-text');
const statusDot = document.querySelector('.status-dot');

// Mode-Specific String Mappings
const INTERFACE_TEXTS = {
  clinical: {
    docTitle: "Aether Clinical Console",
    dashTitle: "Clinical Telemetry System",
    dashSubtitle: "Aether Medical AI Core Diagnostics",
    logo: "🏥",
    configTitle: "📋 Clinical Diagnostics Form",
    
    // Labels
    labelIntensity: "🩸 Fasting Blood Glucose",
    labelCoherence: "🧬 HbA1c Coherence Index",
    labelDensity: "💉 Insulin Particle Density",
    labelGravity: "⚖️ Body Mass Index (BMI)",
    labelAge: "🎂 Patient Age (Years)",
    
    // Telemetry labels
    sumTitle: "📈 Clinical Database Summary",
    sumLabelRows: "Patient Cohort Size",
    sumLabelCols: "Dataset Columns",
    sumLabelIntensity: "Mean Glucose Level",
    sumLabelCoherence: "Mean HbA1c Coherence",
    
    // Button
    submitBtn: "🚀 Run Diagnostics Check",
    
    // Output Card
    resultTitle: "📡 Diagnostics Telemetry",
    resultDesc: "Diagnostics data successfully compiled. Health prediction ready.",
    
    // Deploy Section
    deployTitle: "🧪 Treatment Regimen Deployer",
    sliderLabel: "Local Gravitational Coefficient",
    recLabel1: "Recommended Insulin Flow",
    recLabel2: "Recommended Spin Coherence",
    recLabel3: "Recommended Particle Density"
  },
  
  quantum: {
    docTitle: "Q.E.M.A.D. Core Control",
    dashTitle: "Quantum Antigravity Core",
    dashSubtitle: "QEMAD Drive Telemetry & Wave Predicter",
    logo: "⚛️",
    configTitle: "📟 Field Configuration Interface",
    
    // Labels
    labelIntensity: "🔋 Electromagnetic Field Intensity (T)",
    labelCoherence: "🌀 Quantum Spin Coherence (%)",
    labelDensity: "📊 Particle Density (kg/m³)",
    labelGravity: "🌍 Local Gravitational Force (m/s²)",
    labelAge: "🎂 Drive Co-processor Age (Years)",
    
    // Telemetry labels
    sumTitle: "🖥️ Q.E.M.A.D. Telemetry Console",
    sumLabelRows: "Database Array Size",
    sumLabelCols: "Feature Dimensions",
    sumLabelIntensity: "Mean Intensity (T)",
    sumLabelCoherence: "Mean Coherence (%)",
    
    // Button
    submitBtn: "⚡ Compute Resonance Waveform",
    
    // Output Card
    resultTitle: "🔮 Resonance Frequency Result",
    resultDesc: "Electromagnetic frequency successfully estimated by Random Forest model.",
    
    // Deploy Section
    deployTitle: "🛠️ Antigravity Hover Stabilization",
    sliderLabel: "Target Local Gravity Force",
    recLabel1: "Optimal Field Intensity (T)",
    recLabel2: "Optimal Spin Coherence (%)",
    recLabel3: "Optimal Particle Density (kg/m³)"
  }
};

let currentTheme = 'clinical';
let summaryDataCached = null;

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
  // Sync form initial label markers
  document.querySelectorAll('form.grid-form input').forEach(input => {
    updateValLabel(input);
  });
  
  // Load saved theme
  const savedTheme = localStorage.getItem('app-theme') || 'clinical';
  toggleDashboardMode(savedTheme);
  
  // Fetch telemetry and status
  fetchSystemStatus();
  fetchSummaryTelemetry();
  
  // Initialize dynamic deployer values
  handleSliderChange(9.81);
  
  // Initialize interactive canvas particles
  initCanvasParticles();
});

// Sync Numeric inputs with dynamic preview badges
function updateValLabel(inputElement) {
  const badgeId = `val-${inputElement.id.replace('electromagnetic_', '').replace('quantum_', '').replace('particle_', '').replace('local_', '')}`;
  const badge = document.getElementById(badgeId);
  if (badge) {
    let val = parseFloat(inputElement.value);
    badge.textContent = isNaN(val) ? "0.0" : val.toFixed(inputElement.step.includes('.') ? inputElement.step.split('.')[1].length : 0);
  }
}

// Seamless Dual-Theme Layout Morphing
function toggleDashboardMode(mode) {
  currentTheme = mode;
  localStorage.setItem('app-theme', mode);
  
  const textMap = INTERFACE_TEXTS[mode];
  
  // Body Class Toggles
  if (mode === 'quantum') {
    body.classList.remove('clinical-mode');
    body.classList.add('quantum-mode');
    document.getElementById('toggle-clinical').classList.remove('active');
    document.getElementById('toggle-quantum').classList.add('active');
  } else {
    body.classList.remove('quantum-mode');
    body.classList.add('clinical-mode');
    document.getElementById('toggle-quantum').classList.remove('active');
    document.getElementById('toggle-clinical').classList.add('active');
  }
  
  // Morphs text
  document.title = textMap.docTitle;
  document.getElementById('dashboard-title').textContent = textMap.dashTitle;
  document.getElementById('dashboard-subtitle').textContent = textMap.dashSubtitle;
  document.getElementById('system-logo').textContent = textMap.logo;
  document.getElementById('config-title').textContent = textMap.configTitle;
  
  // Inputs Labels
  document.getElementById('label-intensity').textContent = textMap.labelIntensity;
  document.getElementById('label-coherence').textContent = textMap.labelCoherence;
  document.getElementById('label-density').textContent = textMap.labelDensity;
  document.getElementById('label-gravity').textContent = textMap.labelGravity;
  document.getElementById('label-age').textContent = textMap.labelAge;
  
  // Button
  document.getElementById('submit-button').querySelector('span').textContent = textMap.submitBtn;
  
  // Summary Titles & Labels
  document.getElementById('summary-title').textContent = textMap.sumTitle;
  document.getElementById('sum-label-rows').textContent = textMap.sumLabelRows;
  document.getElementById('sum-label-cols').textContent = textMap.sumLabelCols;
  document.getElementById('sum-label-intensity').textContent = textMap.sumLabelIntensity;
  document.getElementById('sum-label-coherence').textContent = textMap.sumLabelCoherence;
  
  // Deploy & Rec Labels
  document.getElementById('deploy-title').textContent = textMap.deployTitle;
  document.getElementById('slider-label-text').textContent = textMap.sliderLabel;
  document.getElementById('rec-label-1').textContent = textMap.recLabel1;
  document.getElementById('rec-label-2').textContent = textMap.recLabel2;
  document.getElementById('rec-label-3').textContent = textMap.recLabel3;
  
  // Update Results Text dynamically if not empty
  const outputText = output.textContent;
  if (!outputText.includes('Awaiting') && !outputText.includes('Requesting') && !outputText.includes('Error')) {
    renderPredictionResult(parseFloat(output.getAttribute('data-raw-value')));
  } else {
    output.textContent = mode === 'quantum' ? 'Awaiting field configuration sequence...' : 'Awaiting diagnostic data sequence...';
  }
  
  // Re-format status text
  fetchSystemStatus();
  // Update UI telemetry cached cards
  if (summaryDataCached) {
    updateSummaryUI(summaryDataCached);
  }
}

// Fetch Backend Status (/status)
async function fetchSystemStatus() {
  try {
    const response = await fetch('http://127.0.0.1:8000/status');
    if (!response.ok) throw new Error();
    const data = await response.json();
    
    if (data.status === 'ready') {
      statusText.textContent = currentTheme === 'quantum' ? 'Nodes Linked' : 'System Ready';
      statusText.style.color = '';
      statusDot.style.backgroundColor = '';
    }
  } catch (err) {
    statusText.textContent = 'Core Offline';
    statusText.style.color = '#ef4444';
    statusDot.style.backgroundColor = '#ef4444';
  }
}

// Fetch Backend Summary telemetry (/summary)
async function fetchSummaryTelemetry() {
  try {
    const response = await fetch('http://127.0.0.1:8000/summary');
    if (!response.ok) return;
    const data = await response.json();
    summaryDataCached = data;
    updateSummaryUI(data);
  } catch (err) {
    console.error("Could not load database telemetry:", err);
  }
}

function updateSummaryUI(data) {
  document.getElementById('sum-val-rows').textContent = data.rows ? data.rows.toLocaleString() : '---';
  document.getElementById('sum-val-cols').textContent = data.columns ? data.columns.toFixed(0) : '---';
  document.getElementById('sum-val-intensity').textContent = data.mean_intensity ? data.mean_intensity.toFixed(2) + (currentTheme === 'quantum' ? ' T' : ' mmol/L') : '---';
  document.getElementById('sum-val-coherence').textContent = data.mean_coherence ? data.mean_coherence.toFixed(1) + '%' : '---';
}

// Handle `/predict` submission
predictionForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    electromagnetic_field_intensity: parseFloat(document.getElementById('electromagnetic_field_intensity').value),
    quantum_spin_coherence: parseFloat(document.getElementById('quantum_spin_coherence').value),
    particle_density: parseFloat(document.getElementById('particle_density').value),
    local_gravitational_force: parseFloat(document.getElementById('local_gravitational_force').value),
    age: parseFloat(document.getElementById('age').value),
  };

  try {
    output.textContent = currentTheme === 'quantum' ? '⏳ Handshaking quantum nodes...' : '⏳ Compiling medical records...';
    
    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json();
      output.textContent = `❌ Error: ${error.detail ?? response.statusText}`;
      return;
    }

    const data = await response.json();
    const frequency = data.predicted_electromagnetic_frequency;
    
    // Save raw response value for toggles
    output.setAttribute('data-raw-value', frequency);
    renderPredictionResult(frequency);
    
  } catch (err) {
    output.textContent = `⚠️ Network error: ${err.message}`;
  }
});

function renderPredictionResult(rawVal) {
  const textMap = INTERFACE_TEXTS[currentTheme];
  document.getElementById('result-desc').textContent = textMap.resultDesc;
  
  if (currentTheme === 'quantum') {
    output.textContent = `🔮 ${rawVal.toFixed(4)} GHz`;
    output.style.color = '#38bdf8';
  } else {
    // scale frequency nicely to map to a diabetic risk percentage
    // typically raw values hover around 15-35. Let's map 10 to 10% and 40 to 95%
    let scaledRisk = Math.min(99.9, Math.max(1.0, ((rawVal - 8) / 32) * 100));
    output.textContent = `📊 Risk: ${scaledRisk.toFixed(2)}%`;
    output.style.color = scaledRisk > 60 ? '#ef4444' : (scaledRisk > 30 ? '#f59e0b' : '#10b981');
  }
}

// Antigravity Hover Stabilization System Control (/deploy)
let activePreset = 'earth';

async function setGravityPreset(gravity, planetId, buttonEl) {
  // Update presets visual
  document.querySelectorAll('.planet-presets button').forEach(btn => btn.classList.remove('active'));
  buttonEl.classList.add('active');
  activePreset = planetId;
  
  // Set slider value
  document.getElementById('gravity-slider').value = gravity;
  handleSliderChange(gravity, false);
}

function handleSliderChange(val, unsetPreset = true) {
  document.getElementById('slider-current-val').textContent = parseFloat(val).toFixed(2);
  
  if (unsetPreset) {
    // Unset active preset if they custom dragged
    const presets = { '9.81': 'earth', '3.71': 'mars', '1.62': 'moon', '0.00': 'zero' };
    let matchingPreset = presets[parseFloat(val).toFixed(2)];
    
    document.querySelectorAll('.planet-presets button').forEach(btn => btn.classList.remove('active'));
    if (matchingPreset) {
      document.querySelector(`.planet-presets button[onclick*="${matchingPreset}"]`).classList.add('active');
      activePreset = matchingPreset;
    } else {
      activePreset = 'custom';
    }
  }
  
  // Call debounced API
  fetchDeploymentRecommendations(parseFloat(val));
}

// Quick Debounce
let deployTimeout = null;
async function fetchDeploymentRecommendations(gravity) {
  clearTimeout(deployTimeout);
  deployTimeout = setTimeout(async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/deploy?gravity=${gravity}`);
      if (!response.ok) return;
      const data = await response.json();
      
      updateDeployRecommendationsUI(data);
    } catch (err) {
      console.error("Failed to fetch deploy configuration", err);
    }
  }, 100);
}

function updateDeployRecommendationsUI(data) {
  const val1 = data.recommended_field_intensity;
  const val2 = data.recommended_spin_coherence;
  const val3 = data.recommended_particle_density;
  
  // Render text based on theme
  if (currentTheme === 'quantum') {
    document.getElementById('rec-val-1').textContent = `${val1.toFixed(3)} T`;
    document.getElementById('rec-val-2').textContent = `${val2.toFixed(3)}%`;
    document.getElementById('rec-val-3').textContent = `${val3.toFixed(3)} kg/m³`;
  } else {
    // Clinical translation
    document.getElementById('rec-val-1').textContent = `${(val1 * 5).toFixed(1)} u/kg`;
    document.getElementById('rec-val-2').textContent = `${val2.toFixed(1)}%`;
    document.getElementById('rec-val-3').textContent = `${(val3 * 1.5).toFixed(1)} mg/dL`;
  }
  
  // Animate progress gauges
  // Max intensity is ~14. Peak spin coherence is 100%. Max particle density is ~35.
  const fill1 = Math.min(100, Math.max(0, (val1 / 15) * 100));
  const fill2 = Math.min(100, Math.max(0, (val2 / 100) * 100));
  const fill3 = Math.min(100, Math.max(0, (val3 / 25) * 100));
  
  document.getElementById('rec-fill-1').style.width = `${fill1}%`;
  document.getElementById('rec-fill-2').style.width = `${fill2}%`;
  document.getElementById('rec-fill-3').style.width = `${fill3}%`;
}


// ==========================================================================
// Floating Particle Grid Canvas Animation (Optimized: runs only in quantum)
// ==========================================================================
let canvas, ctx, animationFrameId;
let particles = [];
const particleCount = 65;
const connectionDistance = 110;

function initCanvasParticles() {
  canvas = document.getElementById('canvas-particles');
  if (!canvas) return;
  
  ctx = canvas.getContext('2d');
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);
  
  // Generate initial particles
  particles = [];
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.45,
      vy: (Math.random() - 0.5) * 0.45,
      radius: Math.random() * 2 + 1
    });
  }
  
  // Track mouse position
  window.addEventListener('mousemove', handleMouseMove);
  
  // Start active render loops
  animateParticles();
}

let mouse = { x: null, y: null, radius: 140 };
function handleMouseMove(event) {
  mouse.x = event.clientX;
  mouse.y = event.clientY;
}

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

function animateParticles() {
  animationFrameId = requestAnimationFrame(animateParticles);
  
  // If not quantum mode, clear canvas and wait
  if (currentTheme !== 'quantum') {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    return;
  }
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Draw & Update particles
  for (let i = 0; i < particles.length; i++) {
    const p = particles[i];
    
    // Float movement
    p.x += p.vx;
    p.y += p.vy;
    
    // Bounds wrap
    if (p.x < 0) p.x = canvas.width;
    if (p.x > canvas.width) p.x = 0;
    if (p.y < 0) p.y = canvas.height;
    if (p.y > canvas.height) p.y = 0;
    
    // Mouse Pull
    if (mouse.x !== null) {
      const dx = mouse.x - p.x;
      const dy = mouse.y - p.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < mouse.radius) {
        const force = (mouse.radius - dist) / mouse.radius;
        p.x -= dx * force * 0.02;
        p.y -= dy * force * 0.02;
      }
    }
    
    // Draw dot
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(168, 85, 247, 0.45)';
    ctx.fill();
    
    // Web lines
    for (let j = i + 1; j < particles.length; j++) {
      const p2 = particles[j];
      const dx = p.x - p2.x;
      const dy = p.y - p2.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      
      if (dist < connectionDistance) {
        const alpha = (1 - (dist / connectionDistance)) * 0.16;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.strokeStyle = `rgba(6, 182, 212, ${alpha})`;
        ctx.lineWidth = 0.85;
        ctx.stroke();
      }
    }
  }
}
