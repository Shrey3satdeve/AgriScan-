/**
 * AgriScan — Frontend JavaScript
 * Handles image upload, drag-and-drop, API calls, and results rendering.
 * Enhanced with AgriScan Pro features for professional agricultural utility.
 */

// ─── DOM References ──────────────────────────────────────────────────────────
const dropZone         = document.getElementById('drop-zone');
const dropInner        = document.getElementById('drop-inner');
const fileInput        = document.getElementById('file-input');
const previewImg       = document.getElementById('preview-img');
const clearBtn         = document.getElementById('clear-btn');
const analyzeBtn       = document.getElementById('analyze-btn');
const analyzeBtnText   = document.querySelector('.analyze-btn__text');
const analyzeBtnIcon   = document.querySelector('.analyze-btn__icon');
const analyzeBtnSpinner= document.querySelector('.analyze-btn__spinner');
const demoNotice       = document.getElementById('demo-notice');
const statusDot        = document.getElementById('status-dot');

const resultsSection   = document.getElementById('results-section');
const uploadSection    = document.getElementById('upload-section');
const newAnalysisBtn   = document.getElementById('new-analysis-btn');

// Result elements
const severityBadge    = document.getElementById('severity-badge');
const resultDiseaseName= document.getElementById('result-disease-name');
const resultCrop       = document.getElementById('result-crop');
const resultDescription= document.getElementById('result-description');
const confidencePct    = document.getElementById('confidence-pct');
const confidenceBar    = document.getElementById('confidence-bar');
const displayOriginal  = document.getElementById('display-original');
const displayGradcam   = document.getElementById('display-gradcam');
const gradcamUnavail   = document.getElementById('gradcam-unavailable');
const symptomsList     = document.getElementById('symptoms-list');
const treatmentList    = document.getElementById('treatment-list');
const preventionList   = document.getElementById('prevention-list');
const top5Chart        = document.getElementById('top5-chart');

// Pro elements
const farmSizeSlider   = document.getElementById('farm-size-slider');
const farmSizeVal      = document.getElementById('farm-size-val');
const financialLossVal = document.getElementById('financial-loss');
const riskMeterFill    = document.getElementById('risk-meter-fill');
const weatherRiskText  = document.getElementById('weather-risk-text');
const nutrientList     = document.getElementById('nutrient-list');

// ─── Image tabs ──────────────────────────────────────────────────────────────
const tabOriginal      = document.getElementById('tab-original');
const tabGradcam       = document.getElementById('tab-gradcam');

// ─── State ───────────────────────────────────────────────────────────────────
let selectedFile = null;
let currentProData = {
  impact_factor: 0,
  market_price_acre: 0
};
let currentLang = localStorage.getItem('agriscan_lang') || 'en';

// ─── Multi-Language Logic ────────────────────────────────────────────────────
const langSelect = document.getElementById('language-select');

function initLanguage() {
  if (langSelect) {
    langSelect.value = currentLang;
    langSelect.addEventListener('change', (e) => {
      currentLang = e.target.value;
      localStorage.setItem('agriscan_lang', currentLang);
      updateUIStrings();
    });
  }
  updateUIStrings();
}

function updateUIStrings() {
  const elements = document.querySelectorAll('[data-i18n]');
  const langData = translations[currentLang] || translations.en;

  elements.forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (langData[key]) {
      // Use innerHTML for elements that might contain tags like <strong> or <span>
      if (el.children.length > 0 || el.tagName === 'STRONG' || el.tagName === 'SPAN') {
        el.innerHTML = langData[key];
      } else {
        el.textContent = langData[key];
      }
    }
  });

  // Update dynamic placeholders if needed
  if (analyzeBtn && !analyzeBtn.disabled) {
    const btnText = document.querySelector('.analyze-btn__text');
    if (btnText) btnText.textContent = langData.analyze_btn;
  }
}

// Initialize!
initLanguage();

// ─── Server Health Check ─────────────────────────────────────────────────────
async function checkHealth() {
  try {
    const res = await fetch('/health');
    if (res.ok) {
      const data = await res.json();
      statusDot.className = 'status-dot status-dot--online';
      statusDot.title = `Model loaded: ${data.model_loaded ? 'Live AI' : 'Virtual Demo'} · Classes: ${data.num_classes}`;
      // Show/Hide demo notice based on health check too
      if (!data.model_loaded && demoNotice) {
        demoNotice.classList.remove('hidden');
      }
    } else {
      throw new Error('Server error');
    }
  } catch {
    statusDot.className = 'status-dot status-dot--offline';
    statusDot.title = 'Server offline';
  }
}
checkHealth();

// ─── Drag & Drop ─────────────────────────────────────────────────────────────
if (dropZone) {
    dropZone.addEventListener('click', (e) => {
      if (e.target !== clearBtn) fileInput.click();
    });
    dropZone.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') fileInput.click();
    });

    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropZone.classList.add('drag-over');
    });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) setFile(file);
    });
}

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});

if (clearBtn) {
    clearBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      clearFile();
    });
}

function setFile(file) {
  selectedFile = file;
  const url = URL.createObjectURL(file);
  previewImg.src = url;
  previewImg.classList.remove('hidden');
  dropInner.classList.add('hidden');
  clearBtn.classList.remove('hidden');
  analyzeBtn.disabled = false;
}

function clearFile() {
  selectedFile = null;
  previewImg.src = '';
  previewImg.classList.add('hidden');
  clearBtn.classList.add('hidden');
  dropInner.classList.remove('hidden');
  analyzeBtn.disabled = true;
  fileInput.value = '';
}

// ─── Economic Impact Logic ───────────────────────────────────────────────────
if (farmSizeSlider) {
    farmSizeSlider.addEventListener('input', () => {
        const size = parseInt(farmSizeSlider.value);
        if (farmSizeVal) farmSizeVal.textContent = size;
        updateEconomicImpact(size);
    });
}

function updateEconomicImpact(acres) {
    if (!financialLossVal) return;
    const totalValue = acres * (currentProData.market_price_acre || 50000);
    const potentialLoss = Math.round(totalValue * (currentProData.impact_factor || 0.4));
    
    const formatter = new Intl.NumberFormat(currentLang === 'hi' || currentLang === 'mr' ? 'en-IN' : 'en-US', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    });
    
    financialLossVal.textContent = formatter.format(potentialLoss);
}

// ─── Image Tab Switching ──────────────────────────────────────────────────────
if (tabOriginal) tabOriginal.addEventListener('click', () => switchTab('original'));
if (tabGradcam) tabGradcam.addEventListener('click', () => switchTab('gradcam'));

function switchTab(tab) {
  if (tab === 'original') {
    tabOriginal.classList.add('active');
    tabGradcam.classList.remove('active');
    displayOriginal.classList.remove('hidden');
    displayGradcam.classList.add('hidden');
    gradcamUnavail.classList.add('hidden');
  } else {
    tabGradcam.classList.add('active');
    tabOriginal.classList.remove('active');
    displayOriginal.classList.add('hidden');
    if (displayGradcam.src && displayGradcam.src !== window.location.href && !displayGradcam.src.endsWith('/')) {
      displayGradcam.classList.remove('hidden');
      gradcamUnavail.classList.add('hidden');
    } else {
      displayGradcam.classList.add('hidden');
      gradcamUnavail.classList.remove('hidden');
    }
  }
}

// ─── Analysis ─────────────────────────────────────────────────────────────────
if (analyzeBtn) analyzeBtn.addEventListener('click', runAnalysis);

async function runAnalysis() {
  if (!selectedFile) return;

  analyzeBtn.disabled = true;
  analyzeBtnText.textContent = 'Analyzing...';
  analyzeBtnIcon.classList.add('hidden');
  analyzeBtnSpinner.classList.remove('hidden');

  try {
    const formData = new FormData();
    formData.append('image', selectedFile);

    const res = await fetch('/predict', { method: 'POST', body: formData });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || 'Unknown server error');
    }

    const data = await res.json();
    renderResults(data);
  } catch (err) {
    alert(`Analysis failed: ${err.message}\n\nIs the Flask server running?`);
  } finally {
    const langData = translations[currentLang] || translations.en;
    analyzeBtn.disabled = false;
    analyzeBtnText.textContent = langData.analyze_btn;
    analyzeBtnIcon.classList.remove('hidden');
    analyzeBtnSpinner.classList.add('hidden');
  }
}

// ─── Render Results ───────────────────────────────────────────────────────────
function renderResults(data) {
  const { disease_info, confidence, top5, original_image, gradcam_image, is_simulated } = data;

  // Global demo notice
  if (is_simulated && demoNotice) {
    demoNotice.classList.remove('hidden');
  } else if (demoNotice) {
    demoNotice.classList.add('hidden');
  }

  // Severity badge
  if (severityBadge) {
      severityBadge.textContent = disease_info.severity;
      severityBadge.style.color = disease_info.severity_color;
      severityBadge.style.borderColor = disease_info.severity_color;
      severityBadge.style.background = disease_info.severity_color + '1a';
  }

  // Disease info
  if (resultDiseaseName) resultDiseaseName.textContent = disease_info.display_name;
  if (resultCrop) resultCrop.textContent = `🌿 ${disease_info.crop}`;
  if (resultDescription) resultDescription.textContent = disease_info.description;

  // Confidence meter
  const pct = Math.round(confidence * 100);
  if (confidencePct) confidencePct.textContent = `${pct}%`;
  
  const lowConfWarning = document.getElementById('low-confidence-warning');
  if (lowConfWarning) {
    if (disease_info.class === 'UNCERTAIN' || confidence < 0.5) {
      lowConfWarning.classList.remove('hidden');
    } else {
      lowConfWarning.classList.add('hidden');
    }
  }

  if (confidenceBar) {
      confidenceBar.style.width = '0%';
      setTimeout(() => { confidenceBar.style.width = `${pct}%`; }, 100);
  }

  // --- AgriScan Pro Logic ---
  currentProData.impact_factor = disease_info.impact_factor || 0.4;
  currentProData.market_price_acre = disease_info.market_price_acre || 50000;
  
  if (farmSizeSlider) {
      farmSizeSlider.value = 1;
      if (farmSizeVal) farmSizeVal.textContent = 1;
      updateEconomicImpact(1);
  }

  if (riskMeterFill) {
      const riskPct = (disease_info.impact_factor || 0.4) * 100;
      riskMeterFill.style.width = '0%';
      setTimeout(() => { riskMeterFill.style.width = `${riskPct}%`; }, 300);
  }
  if (weatherRiskText) {
      weatherRiskText.textContent = disease_info.weather_risk || "Monitor local conditions.";
  }
  if (nutrientList) {
      renderList(nutrientList, disease_info.nutrient_tips || []);
  }
  // --------------------------

  // Images
  if (displayOriginal) displayOriginal.src = `data:image/jpeg;base64,${original_image}`;
  if (gradcam_image && displayGradcam) {
    displayGradcam.src = `data:image/jpeg;base64,${gradcam_image}`;
    displayGradcam.classList.remove('hidden');
    if (gradcamUnavail) gradcamUnavail.classList.add('hidden');
  } else if (gradcamUnavail) {
    if (displayGradcam) displayGradcam.src = '';
    gradcamUnavail.classList.remove('hidden');
  }

  switchTab('original');

  renderList(symptomsList, disease_info.symptoms);
  renderList(treatmentList, disease_info.treatment);
  renderList(preventionList, disease_info.prevention);
  renderTop5(top5);

  if (uploadSection) uploadSection.classList.add('hidden');
  if (resultsSection) resultsSection.classList.remove('hidden');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function renderList(el, items) {
  if (el) el.innerHTML = items.map(item => `<li>${item}</li>`).join('');
}

function renderTop5(top5) {
  if (!top5Chart) return;
  const maxConf = Math.max(...top5.map(t => t.confidence));
  top5Chart.innerHTML = top5.map((item, i) => {
    const pct = Math.round(item.confidence * 100);
    const barWidth = maxConf > 0 ? (item.confidence / maxConf) * 100 : 0;
    const color = i === 0 ? '#22c55e' : i === 1 ? '#2dd4bf' : '#6b7280';
    const label = item.display_name || item.class.replace(/___/g, ' — ').replace(/_/g, ' ');
    return `
      <div class="top5-item">
        <span class="top5-item__label" title="${label}">${i + 1}. ${label}</span>
        <div class="top5-item__bar-wrap">
          <div class="top5-item__bar" style="width:0%;background:${color}" data-target="${barWidth}"></div>
        </div>
        <span class="top5-item__pct">${pct}%</span>
      </div>
    `;
  }).join('');

  setTimeout(() => {
    document.querySelectorAll('.top5-item__bar').forEach(bar => {
      bar.style.width = bar.dataset.target + '%';
    });
  }, 150);
}

// ─── New Analysis ─────────────────────────────────────────────────────────────
if (newAnalysisBtn) {
    newAnalysisBtn.addEventListener('click', () => {
      resultsSection.classList.add('hidden');
      uploadSection.classList.remove('hidden');
      clearFile();
      if (demoNotice) demoNotice.classList.add('hidden');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
