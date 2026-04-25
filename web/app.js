const promptEl = document.querySelector("#prompt");
const planOutput = document.querySelector("#planOutput");
const runOutput = document.querySelector("#runOutput");
const statusEl = document.querySelector("#status");
const jobsEl = document.querySelector("#jobs");

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
    });
    jobsEl.appendChild(item);
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
    statusEl.textContent = data.result.status;
    await refreshJobs();
  } catch (error) {
    statusEl.textContent = "error";
    runOutput.textContent = error.message;
  }
});

refreshJobs();

