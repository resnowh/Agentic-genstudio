const promptEl = document.querySelector("#prompt");
const planOutput = document.querySelector("#planOutput");
const runOutput = document.querySelector("#runOutput");
const statusEl = document.querySelector("#status");
const jobsEl = document.querySelector("#jobs");
const galleryEl = document.querySelector("#gallery");

function pretty(value) {
  return JSON.stringify(value, null, 2);
}

async function postJSON(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || response.statusText);
  return data;
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
      statusEl.textContent = detail.result?.status || "job loaded";
    });
    jobsEl.appendChild(item);
  }
}

function renderGallery(result) {
  const urls = result.output_urls || [];
  galleryEl.innerHTML = "";
  galleryEl.classList.toggle("empty", urls.length === 0);
  if (!urls.length) {
    galleryEl.innerHTML = `<div class="empty-state">No image outputs for this job yet.</div>`;
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
  statusEl.textContent = "planning";
  try {
    const data = await postJSON("/api/plan", { prompt: promptEl.value });
    planOutput.textContent = pretty(data.job);
    statusEl.textContent = "plan ready";
  } catch (error) {
    statusEl.textContent = "error";
    planOutput.textContent = error.message;
  }
});

document.querySelector("#composer").addEventListener("submit", async (event) => {
  event.preventDefault();
  statusEl.textContent = "running";
  try {
    const data = await postJSON("/api/run", { prompt: promptEl.value });
    planOutput.textContent = pretty(data.job);
    runOutput.textContent = pretty(data.result);
    renderGallery(data.result);
    statusEl.textContent = data.result.status;
    await refreshJobs();
  } catch (error) {
    statusEl.textContent = "error";
    runOutput.textContent = error.message;
  }
});

refreshJobs();
renderGallery({});
