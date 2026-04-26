const promptEl = document.querySelector("#prompt");
const planOutput = document.querySelector("#planOutput");
const runOutput = document.querySelector("#runOutput");
const jobsEl = document.querySelector("#jobs");
const galleryEl = document.querySelector("#gallery");
const taskTypeEl = document.querySelector("#taskType");
const resolutionEl = document.querySelector("#resolution");
const customResolutionEl = document.querySelector("#customResolution");
const outputsEl = document.querySelector("#outputs");
const sourceImageEl = document.querySelector("#sourceImage");
const maskImageEl = document.querySelector("#maskImage");
const languageEl = document.querySelector("#language");
const composerEl = document.querySelector("#composer");
const planBtnEl = document.querySelector("#planBtn");

let progressShellEl = null;
let progressFillEl = null;
let progressPercentEl = null;
let progressStageEl = null;
let progressDetailEl = null;
let currentLanguage = "zh-CN";
let activePoll = null;

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
    customResolutionPlaceholder: "例如 1536x1024",
    customResolutionOption: "自定义",
    outputsLabel: "张数",
    sourceLabel: "原图路径",
    sourcePlaceholder: "D:\\images\\source.png 或相对路径",
    maskLabel: "蒙版路径",
    maskPlaceholder: "D:\\images\\mask.png，用于局部重绘",
    planButton: "预览任务",
    runButton: "开始生成",
    generatedImages: "生成结果",
    galleryEmpty: "运行后会在这里显示生成图片。",
    galleryNoOutput: "这个任务目前还没有图片输出。",
    plannedJob: "任务预览",
    executionResult: "执行结果",
    recentJobs: "最近任务",
    previewJob: "查看",
    deleteJob: "删除",
    deleteConfirm: "删除这条任务记录以及对应输出文件？",
    statusReady: "尚未开始",
    statusPlanning: "正在预览任务",
    statusPlanReady: "任务预览已更新",
    statusQueued: "排队中",
    statusRunning: "生成中",
    statusCompleted: "已完成",
    statusBlocked: "已阻止",
    statusError: "出错了",
    progressTitle: "生成进度",
    progressPreparing: "正在准备任务...",
    progressQueued: "等待执行",
    progressLoading: "正在加载模型",
    progressGenerating: "正在生成图像",
    progressSaving: "正在保存结果",
    progressCompleted: "生成完成",
    progressBlocked: "任务未能执行",
    progressError: "生成失败",
    jobEmpty: "还没有历史任务。",
    jobPromptFallback: "未填写提示词",
    historyNoOutput: "暂无预览",
    fieldTaskType: "任务类型",
    fieldResolution: "分辨率",
    fieldOutputs: "张数",
    fieldBackend: "后端",
    fieldStatus: "状态",
    fieldPrompt: "提示词",
    fieldAdaptedPrompt: "模型提示词",
    fieldNegativePrompt: "负面提示词",
    fieldPromptLanguage: "输入语言",
    fieldCreated: "创建时间",
    fieldJobId: "任务 ID",
    fieldImages: "图片输出",
    fieldMessage: "消息",
    emptyPlan: "点击“预览任务”后会显示任务参数。",
    emptyResult: "开始生成后会显示执行结果。",
    invalidResolution: "自定义分辨率格式应为 1024x1024。",
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
    customResolutionPlaceholder: "Example: 1536x1024",
    customResolutionOption: "Custom",
    outputsLabel: "Images",
    sourceLabel: "Source Image Path",
    sourcePlaceholder: "D:\\images\\source.png or relative path",
    maskLabel: "Mask Image Path",
    maskPlaceholder: "D:\\images\\mask.png for inpaint",
    planButton: "Preview Task",
    runButton: "Start Generation",
    generatedImages: "Generated Images",
    galleryEmpty: "Run a prompt to render images here.",
    galleryNoOutput: "No image outputs for this job yet.",
    plannedJob: "Task Preview",
    executionResult: "Execution Result",
    recentJobs: "Recent Jobs",
    previewJob: "Open",
    deleteJob: "Delete",
    deleteConfirm: "Delete this job record and all generated files?",
    statusReady: "Not started",
    statusPlanning: "Preparing task preview",
    statusPlanReady: "Task preview updated",
    statusQueued: "Queued",
    statusRunning: "Running",
    statusCompleted: "Completed",
    statusBlocked: "Blocked",
    statusError: "Error",
    progressTitle: "Generation Progress",
    progressPreparing: "Preparing job...",
    progressQueued: "Waiting to start",
    progressLoading: "Loading model",
    progressGenerating: "Generating image",
    progressSaving: "Saving outputs",
    progressCompleted: "Generation complete",
    progressBlocked: "Task could not run",
    progressError: "Generation failed",
    jobEmpty: "No recent jobs yet.",
    jobPromptFallback: "No prompt provided",
    historyNoOutput: "No preview",
    fieldTaskType: "Task Type",
    fieldResolution: "Resolution",
    fieldOutputs: "Images",
    fieldBackend: "Backend",
    fieldStatus: "Status",
    fieldPrompt: "Prompt",
    fieldAdaptedPrompt: "Model Prompt",
    fieldNegativePrompt: "Negative Prompt",
    fieldPromptLanguage: "Input Language",
    fieldCreated: "Created",
    fieldJobId: "Job ID",
    fieldImages: "Image Outputs",
    fieldMessage: "Message",
    emptyPlan: "Click Preview Task to inspect parameters.",
    emptyResult: "Generation results will appear here.",
    invalidResolution: "Custom resolution should look like 1024x1024.",
  },
  ja: {
    appName: "エージェント生成工房",
    eyebrow: "ローカル AI 創作エージェント",
    subtitle: "自然言語を入力すると、Animagine が実画像を生成します。",
    languageLabel: "言語",
    modeLabel: "モード",
    modeTextToImage: "テキストから画像",
    modeImageToImage: "画像から画像",
    modeInpaint: "部分再描画",
    resolutionLabel: "解像度",
    customResolutionPlaceholder: "例: 1536x1024",
    customResolutionOption: "カスタム",
    outputsLabel: "枚数",
    sourceLabel: "元画像パス",
    sourcePlaceholder: "D:\\images\\source.png または相対パス",
    maskLabel: "マスク画像パス",
    maskPlaceholder: "D:\\images\\mask.png（部分再描画用）",
    planButton: "タスク確認",
    runButton: "生成開始",
    generatedImages: "生成結果",
    galleryEmpty: "実行すると、ここに生成画像が表示されます。",
    galleryNoOutput: "このタスクにはまだ画像出力がありません。",
    plannedJob: "タスク確認",
    executionResult: "実行結果",
    recentJobs: "最近のタスク",
    previewJob: "表示",
    deleteJob: "削除",
    deleteConfirm: "このタスク記録と生成ファイルを削除しますか？",
    statusReady: "未開始",
    statusPlanning: "タスク確認を準備中",
    statusPlanReady: "タスク確認を更新しました",
    statusQueued: "待機中",
    statusRunning: "生成中",
    statusCompleted: "完了",
    statusBlocked: "停止",
    statusError: "エラー",
    progressTitle: "生成進捗",
    progressPreparing: "タスクを準備しています...",
    progressQueued: "開始待ち",
    progressLoading: "モデルを読み込み中",
    progressGenerating: "画像を生成中",
    progressSaving: "結果を保存中",
    progressCompleted: "生成完了",
    progressBlocked: "タスクを実行できませんでした",
    progressError: "生成に失敗しました",
    jobEmpty: "まだ履歴がありません。",
    jobPromptFallback: "プロンプト未入力",
    historyNoOutput: "プレビューなし",
    fieldTaskType: "タスク種別",
    fieldResolution: "解像度",
    fieldOutputs: "枚数",
    fieldBackend: "バックエンド",
    fieldStatus: "状態",
    fieldPrompt: "プロンプト",
    fieldAdaptedPrompt: "モデル用プロンプト",
    fieldNegativePrompt: "ネガティブプロンプト",
    fieldPromptLanguage: "入力言語",
    fieldCreated: "作成日時",
    fieldJobId: "ジョブ ID",
    fieldImages: "画像出力",
    fieldMessage: "メッセージ",
    emptyPlan: "タスク確認を押すとパラメータが表示されます。",
    emptyResult: "生成結果はここに表示されます。",
    invalidResolution: "カスタム解像度は 1024x1024 の形式で入力してください。",
  },
};

function t(key) {
  return translations[currentLanguage]?.[key] || key;
}

function statusTextFromState(state) {
  const map = {
    queued: t("statusQueued"),
    running: t("statusRunning"),
    completed: t("statusCompleted"),
    blocked: t("statusBlocked"),
    error: t("statusError"),
  };
  return map[state] || t("statusReady");
}

function progressTextFromStage(stage) {
  const map = {
    queued: t("progressQueued"),
    preparing: t("progressPreparing"),
    loading_model: t("progressLoading"),
    starting: t("progressGenerating"),
    generating: t("progressGenerating"),
    saving: t("progressSaving"),
    completed: t("progressCompleted"),
    blocked: t("progressBlocked"),
    error: t("progressError"),
  };
  return map[stage] || t("progressPreparing");
}

function currentResolution() {
  if (resolutionEl.value !== "custom") {
    return resolutionEl.value;
  }
  return customResolutionEl.value.trim().toLowerCase();
}

function validateResolution(value) {
  return /^\d{3,5}x\d{3,5}$/.test(value);
}

function truncate(text, length = 110) {
  if (!text) {
    return t("jobPromptFallback");
  }
  return text.length > length ? `${text.slice(0, length)}...` : text;
}

function escapeHtml(text) {
  return String(text ?? "").replace(/[&<>"']/g, (char) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    };
    return entities[char];
  });
}

function formatDate(value) {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function detailRow(label, value) {
  if (value === undefined || value === null || value === "" || (Array.isArray(value) && !value.length)) {
    return "";
  }
  return `
    <div class="detail-row">
      <dt>${escapeHtml(label)}</dt>
      <dd>${escapeHtml(Array.isArray(value) ? value.join(", ") : value)}</dd>
    </div>
  `;
}

function renderPlan(job) {
  if (!job) {
    planOutput.innerHTML = `<div class="detail-empty">${t("emptyPlan")}</div>`;
    return;
  }
  planOutput.innerHTML = `
    <dl class="detail-list">
      ${detailRow(t("fieldTaskType"), job.task_type)}
      ${detailRow(t("fieldResolution"), job.resolution)}
      ${detailRow(t("fieldOutputs"), job.outputs)}
      ${detailRow(t("fieldBackend"), job.backend)}
      ${detailRow(t("fieldCreated"), formatDate(job.created_at))}
      ${detailRow(t("fieldJobId"), job.job_id)}
      ${detailRow(t("fieldPrompt"), job.prompt)}
      ${detailRow(t("fieldPromptLanguage"), job.parameters?.prompt_language)}
      ${detailRow(t("fieldAdaptedPrompt"), job.parameters?.positive_prompt)}
      ${detailRow(t("fieldNegativePrompt"), job.parameters?.negative_prompt)}
    </dl>
  `;
}

function renderResult(result) {
  if (!result) {
    runOutput.innerHTML = `<div class="detail-empty">${t("emptyResult")}</div>`;
    return;
  }
  const urls = result.output_urls || [];
  const outputList = urls.length
    ? `<div class="detail-images">${urls.map((url, index) => `<a href="${url}" target="_blank">image_${String(index + 1).padStart(3, "0")}.png</a>`).join("")}</div>`
    : "";
  runOutput.innerHTML = `
    <dl class="detail-list">
      ${detailRow(t("fieldStatus"), statusTextFromState(result.status))}
      ${detailRow(t("fieldBackend"), result.backend)}
      ${detailRow(t("fieldMessage"), result.message)}
      ${detailRow(t("fieldJobId"), result.job_id)}
    </dl>
    ${urls.length ? `<div class="detail-section-title">${t("fieldImages")}</div>${outputList}` : ""}
  `;
}

function ensureProgressUI() {
  if (progressShellEl) {
    return;
  }
  const actions = document.querySelector(".actions");
  const shell = document.createElement("section");
  shell.className = "progress-shell";
  shell.id = "progressShell";
  shell.hidden = true;
  shell.innerHTML = `
    <div class="progress-header">
      <div>
        <div class="progress-title">${t("progressTitle")}</div>
        <div class="progress-stage" id="progressStage">${t("statusReady")}</div>
      </div>
      <strong class="progress-percent" id="progressPercent">0%</strong>
    </div>
    <div class="progress-track">
      <div class="progress-fill" id="progressFill"></div>
    </div>
    <div class="progress-detail" id="progressDetail">${t("progressPreparing")}</div>
  `;
  actions.insertAdjacentElement("afterend", shell);
  progressShellEl = shell;
  progressFillEl = shell.querySelector("#progressFill");
  progressPercentEl = shell.querySelector("#progressPercent");
  progressStageEl = shell.querySelector("#progressStage");
  progressDetailEl = shell.querySelector("#progressDetail");
}

function resetProgress() {
  ensureProgressUI();
  progressShellEl.hidden = false;
  progressFillEl.style.width = "0%";
  progressPercentEl.textContent = "0%";
  progressStageEl.dataset.state = "";
  progressStageEl.dataset.stage = "queued";
  progressStageEl.textContent = t("statusReady");
  progressDetailEl.textContent = t("progressPreparing");
}

function setProgress(progress = {}, state = "queued") {
  ensureProgressUI();
  const percent = Math.max(0, Math.min(100, Number(progress.percent ?? 0)));
  const stage = progress.stage || state || "queued";
  const detail = ["blocked", "error"].includes(stage)
    ? progress.detail || progressTextFromStage(stage)
    : progressTextFromStage(stage);

  progressShellEl.hidden = false;
  progressFillEl.style.width = `${percent}%`;
  progressPercentEl.textContent = `${percent}%`;
  progressStageEl.dataset.state = state || "";
  progressStageEl.dataset.stage = stage;
  progressStageEl.textContent = statusTextFromState(state);
  progressDetailEl.textContent = detail;
}

function syncResolutionUI() {
  const isCustom = resolutionEl.value === "custom";
  customResolutionEl.hidden = !isCustom;
  customResolutionEl.required = isCustom;
}

function applyLanguage(language) {
  currentLanguage = translations[language] ? language : "zh-CN";
  document.documentElement.lang = currentLanguage;
  document.title = t("appName");
  localStorage.setItem("agentic-genstudio-language", currentLanguage);
  languageEl.value = currentLanguage;

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.placeholder = t(node.dataset.i18nPlaceholder);
  });

  for (const option of taskTypeEl.options) {
    if (option.value === "text_to_image") option.textContent = t("modeTextToImage");
    if (option.value === "image_to_image") option.textContent = t("modeImageToImage");
    if (option.value === "inpaint") option.textContent = t("modeInpaint");
  }
  const customOption = [...resolutionEl.options].find((option) => option.value === "custom");
  if (customOption) {
    customOption.textContent = t("customResolutionOption");
  }

  if (progressShellEl) {
    const state = progressStageEl.dataset.state || "";
    const stage = progressStageEl.dataset.stage || "queued";
    progressStageEl.textContent = state ? statusTextFromState(state) : t("statusReady");
    if (!["blocked", "error"].includes(stage)) {
      progressDetailEl.textContent = progressTextFromStage(stage);
    }
    progressShellEl.querySelector(".progress-title").textContent = t("progressTitle");
  }

  renderPlan(window.currentPlan || null);
  renderResult(window.currentResult || null);
  refreshJobs();
  if (!window.currentResult) {
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

async function deleteJob(jobId) {
  const response = await fetch(`/api/jobs/${jobId}`, { method: "DELETE" });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || response.statusText);
  }
  return data;
}

function buildPayload() {
  const resolution = currentResolution();
  if (!validateResolution(resolution)) {
    throw new Error(t("invalidResolution"));
  }
  return {
    prompt: promptEl.value,
    task_type: taskTypeEl.value,
    resolution,
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
  }
  if (mode === "image_to_image") {
    maskImageEl.value = "";
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

async function loadJob(jobId) {
  const detail = await fetch(`/api/jobs/${jobId}`).then((response) => response.json());
  window.currentPlan = detail.job || null;
  window.currentResult = detail.result || null;
  renderPlan(window.currentPlan);
  renderResult(window.currentResult);
  renderGallery(detail.result || {});
  if (detail.progress || detail.state) {
    setProgress(detail.progress || { percent: detail.result ? 100 : 0, stage: detail.state }, detail.state || detail.result?.status);
  }
}

async function refreshJobs() {
  const response = await fetch("/api/jobs?limit=50");
  const data = await response.json();
  jobsEl.innerHTML = "";

  const jobs = data.jobs || [];
  if (!jobs.length) {
    jobsEl.innerHTML = `<div class="empty-state">${t("jobEmpty")}</div>`;
    return;
  }

  for (const item of jobs) {
    const { job, preview_url: previewUrl } = item;
    const card = document.createElement("article");
    card.className = "job";
    card.innerHTML = `
      <div class="job-preview">
        ${
          previewUrl
            ? `<img src="${previewUrl}" alt="History preview">`
            : `<div class="job-preview-empty">${t("historyNoOutput")}</div>`
        }
      </div>
      <div class="job-body">
        <strong>${escapeHtml(job.task_type)}</strong>
        <span>${escapeHtml(truncate(job.prompt))}</span>
      </div>
      <div class="job-actions">
        <button type="button" class="job-open">${t("previewJob")}</button>
        <button type="button" class="job-delete">${t("deleteJob")}</button>
      </div>
    `;

    const image = card.querySelector(".job-preview img");
    if (image) {
      image.addEventListener("error", () => {
        card.querySelector(".job-preview").innerHTML = `<div class="job-preview-empty">${t("historyNoOutput")}</div>`;
      });
    }

    card.querySelector(".job-open").addEventListener("click", async () => {
      await loadJob(job.job_id);
    });

    card.querySelector(".job-delete").addEventListener("click", async () => {
      if (!window.confirm(t("deleteConfirm"))) {
        return;
      }
      await deleteJob(job.job_id);
      if (activePoll) {
        clearInterval(activePoll);
        activePoll = null;
      }
      window.currentPlan = null;
      window.currentResult = null;
      renderPlan(null);
      renderResult(null);
      renderGallery({});
      resetProgress();
      await refreshJobs();
    });

    jobsEl.appendChild(card);
  }
}

async function pollJob(jobId) {
  if (activePoll) {
    clearInterval(activePoll);
  }

  const tick = async () => {
    const detail = await fetch(`/api/jobs/${jobId}`).then((response) => response.json());
    window.currentPlan = detail.job || null;
    window.currentResult = detail.result || null;
    renderPlan(window.currentPlan);
    renderResult(window.currentResult);
    renderGallery(detail.result || {});
    if (detail.progress || detail.state) {
      setProgress(detail.progress || { percent: detail.result ? 100 : 0, stage: detail.state }, detail.state || detail.result?.status);
    }
    if (["completed", "blocked", "error"].includes(detail.state)) {
      clearInterval(activePoll);
      activePoll = null;
      await refreshJobs();
    }
  };

  await tick();
  activePoll = setInterval(() => {
    tick().catch((error) => {
      clearInterval(activePoll);
      activePoll = null;
      setProgress({ percent: 100, stage: "error", detail: error.message }, "error");
      window.currentResult = { status: "error", message: error.message };
      renderResult(window.currentResult);
    });
  }, 1000);
}

planBtnEl.addEventListener("click", async () => {
  resetProgress();
  setProgress({ percent: 0, stage: "preparing", detail: t("statusPlanning") }, "queued");
  try {
    const data = await postJSON("/api/plan", buildPayload());
    window.currentPlan = data.job;
    renderPlan(data.job);
    setProgress({ percent: 0, stage: "queued", detail: t("statusPlanReady") }, "queued");
  } catch (error) {
    setProgress({ percent: 100, stage: "error", detail: error.message }, "error");
    window.currentPlan = null;
    renderPlan(null);
  }
});

composerEl.addEventListener("submit", async (event) => {
  event.preventDefault();
  window.currentResult = null;
  renderResult(null);
  renderGallery({});
  resetProgress();
  setProgress({ percent: 1, stage: "queued", detail: t("progressPreparing") }, "queued");
  try {
    const data = await postJSON("/api/run_async", buildPayload());
    window.currentPlan = data.job;
    renderPlan(data.job);
    setProgress(data.progress || { percent: 1, stage: "queued" }, data.state || "queued");
    await pollJob(data.job.job_id);
  } catch (error) {
    setProgress({ percent: 100, stage: "error", detail: error.message }, "error");
    window.currentResult = { status: "error", message: error.message };
    renderResult(window.currentResult);
  }
});

taskTypeEl.addEventListener("change", syncModeUI);
resolutionEl.addEventListener("change", syncResolutionUI);
languageEl.addEventListener("change", () => applyLanguage(languageEl.value));

window.currentPlan = null;
window.currentResult = null;
ensureProgressUI();
resetProgress();
renderPlan(null);
renderResult(null);
renderGallery({});
syncModeUI();
syncResolutionUI();
applyLanguage(localStorage.getItem("agentic-genstudio-language") || "zh-CN");
