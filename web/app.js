const promptEl = document.querySelector("#prompt");
const planOutput = document.querySelector("#planOutput");
const runOutput = document.querySelector("#runOutput");
const statusEl = document.querySelector("#status");
const jobsEl = document.querySelector("#jobs");
const galleryEl = document.querySelector("#gallery");
const taskTypeEl = document.querySelector("#taskType");
const resolutionEl = document.querySelector("#resolution");
const outputsEl = document.querySelector("#outputs");
const sourceImageEl = document.querySelector("#sourceImage");
const maskImageEl = document.querySelector("#maskImage");
const languageEl = document.querySelector("#language");
const pageTitleEl = document.querySelector("#pageTitle");

const translations = {
  "zh-CN": {
    appName: "灵构绘境",
    eyebrow: "本地 AI 创作代理",
    subtitle: "自然语言输入，Animagine 真实出图。",
    languageLabel: "语言",
    modeLabel: "模式",
    modeTextToImage: "文生图",
    modeImageToImage: "图生图",
    modeInpaint: "局部重绘",
    resolutionLabel: "分辨率",
    outputsLabel: "张数",
    sourceLabel: "原图路径",
    sourcePlaceholder: "D:\\images\\source.png 或相对路径",
    maskLabel: "蒙版路径",
    maskPlaceholder: "D:\\images\\mask.png，用于局部重绘",
    planButton: "规划",
    runButton: "运行",
    generatedImages: "生成结果",
    galleryEmpty: "运行后会在这里显示生成图片。",
    galleryNoOutput: "这个任务目前还没有图片输出。",
    plannedJob: "任务规划",
    executionResult: "执行结果",
    recentJobs: "最近任务",
    statusReady: "animagine 就绪",
    statusPlanning: "规划中",
    statusPlanReady: "规划完成",
    statusRunning: "生成中",
    statusError: "错误",
    statusJobLoaded: "任务已载入",
  },
  en: {
    appName: "Agentic GenStudio",
    eyebrow: "Local AI creation agent",
    subtitle: "Natural language in, Animagine-powered images out.",
    languageLabel: "Language",
    modeLabel: "Mode",
    modeTextToImage: "Text to Image",
    modeImageToImage: "Image to Image",
    modeInpaint: "Inpaint",
    resolutionLabel: "Resolution",
    outputsLabel: "Images",
    sourceLabel: "Source Image Path",
    sourcePlaceholder: "D:\\images\\source.png or relative path",
    maskLabel: "Mask Image Path",
    maskPlaceholder: "D:\\images\\mask.png for inpaint",
    planButton: "Plan",
    runButton: "Run",
    generatedImages: "Generated Images",
    galleryEmpty: "Run a prompt to render images here.",
    galleryNoOutput: "No image outputs for this job yet.",
    plannedJob: "Planned Job",
    executionResult: "Execution Result",
    recentJobs: "Recent Jobs",
    statusReady: "animagine ready",
    statusPlanning: "planning",
    statusPlanReady: "plan ready",
    statusRunning: "running",
    statusError: "error",
    statusJobLoaded: "job loaded",
  },
  ja: {
    appName: "エージェント生成工房",
    eyebrow: "ローカル AI クリエイションエージェント",
    subtitle: "自然言語を入力すると、Animagine が実画像を生成します。",
    languageLabel: "言語",
    modeLabel: "モード",
    modeTextToImage: "テキストから画像",
    modeImageToImage: "画像から画像",
    modeInpaint: "部分再描画",
    resolutionLabel: "解像度",
    outputsLabel: "枚数",
    sourceLabel: "元画像パス",
    sourcePlaceholder: "D:\\images\\source.png または相対パス",
    maskLabel: "マスク画像パス",
    maskPlaceholder: "D:\\images\\mask.png（部分再描画用）",
    planButton: "プラン",
    runButton: "実行",
    generatedImages: "生成結果",
    galleryEmpty: "実行すると、ここに生成画像が表示されます。",
    galleryNoOutput: "このジョブにはまだ画像出力がありません。",
    plannedJob: "ジョブ計画",
    executionResult: "実行結果",
    recentJobs: "最近のジョブ",
    statusReady: "animagine 準備完了",
    statusPlanning: "計画中",
    statusPlanReady: "計画完了",
    statusRunning: "生成中",
    statusError: "エラー",
    statusJobLoaded: "ジョブを読み込みました",
  },
};

let currentLanguage = "zh-CN";

function pretty(value) {
  return JSON.stringify(value, null, 2);
}

function t(key) {
  return translations[currentLanguage][key] || key;
}

function applyLanguage(language) {
  currentLanguage = translations[language] ? language : "zh-CN";
  document.documentElement.lang = currentLanguage;
  localStorage.setItem("agentic-genstudio-language", currentLanguage);
  languageEl.value = currentLanguage;
  document.title = t("appName");
  if (pageTitleEl) {
    pageTitleEl.textContent = t("appName");
  }

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.placeholder = t(node.dataset.i18nPlaceholder);
  });

  const optionLabels = {
    text_to_image: t("modeTextToImage"),
    image_to_image: t("modeImageToImage"),
    inpaint: t("modeInpaint"),
  };
  for (const option of taskTypeEl.options) {
    option.textContent = optionLabels[option.value] || option.value;
  }

  if (!runOutput.textContent.trim() || runOutput.textContent.includes("No image outputs")) {
    renderGallery({});
  }
}

async function postJSON(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || response.statusText);
  }
  return data;
}

function buildPayload() {
  return {
    prompt: promptEl.value,
    task_type: taskTypeEl.value,
    resolution: resolutionEl.value,
    outputs: Number(outputsEl.value),
    source_image: sourceImageEl.value.trim(),
    mask_image: maskImageEl.value.trim(),
  };
}

function syncModeUI() {
  const mode = taskTypeEl.value;
  sourceImageEl.disabled = mode === "text_to_image";
  maskImageEl.disabled = mode !== "inpaint";
  if (mode === "text_to_image") {
    sourceImageEl.value = "";
    maskImageEl.value = "";
  } else if (mode === "image_to_image") {
    maskImageEl.value = "";
  }
}

async function refreshJobs() {
  const response = await fetch("/api/jobs?limit=12");
  const data = await response.json();
  jobsEl.innerHTML = "";
  for (const job of data.jobs || []) {
    const item = document.createElement("button");
    item.className = "job";
    item.type = "button";
    item.innerHTML = `<strong>${job.task_type}</strong><span>${job.prompt}</span>`;
    item.addEventListener("click", async () => {
      const detail = await fetch(`/api/jobs/${job.job_id}`).then((r) => r.json());
      planOutput.textContent = pretty(detail.job);
      runOutput.textContent = pretty(detail.result || {});
      renderGallery(detail.result || {});
      statusEl.textContent = detail.result?.status || t("statusJobLoaded");
    });
    jobsEl.appendChild(item);
  }
}

function renderGallery(result) {
  const urls = result.output_urls || [];
  galleryEl.innerHTML = "";
  galleryEl.classList.toggle("empty", urls.length === 0);
  if (!urls.length) {
    galleryEl.innerHTML = `<div class="empty-state">${t("galleryNoOutput")}</div>`;
    return;
  }
  for (const url of urls) {
    const figure = document.createElement("figure");
    figure.className = "shot";
    figure.innerHTML = `<img src="${url}" alt="Generated output"><figcaption>${url.split("/").pop()}</figcaption>`;
    galleryEl.appendChild(figure);
  }
}

document.querySelector("#planBtn").addEventListener("click", async () => {
  statusEl.textContent = t("statusPlanning");
  try {
    const data = await postJSON("/api/plan", buildPayload());
    planOutput.textContent = pretty(data.job);
    statusEl.textContent = t("statusPlanReady");
  } catch (error) {
    statusEl.textContent = t("statusError");
    planOutput.textContent = error.message;
  }
});

document.querySelector("#composer").addEventListener("submit", async (event) => {
  event.preventDefault();
  statusEl.textContent = t("statusRunning");
  try {
    const data = await postJSON("/api/run", buildPayload());
    planOutput.textContent = pretty(data.job);
    runOutput.textContent = pretty(data.result);
    renderGallery(data.result);
    statusEl.textContent = data.result.status;
    await refreshJobs();
  } catch (error) {
    statusEl.textContent = t("statusError");
    runOutput.textContent = error.message;
  }
});

taskTypeEl.addEventListener("change", syncModeUI);
languageEl.addEventListener("change", () => applyLanguage(languageEl.value));

refreshJobs();
renderGallery({});
applyLanguage(localStorage.getItem("agentic-genstudio-language") || "zh-CN");
syncModeUI();
