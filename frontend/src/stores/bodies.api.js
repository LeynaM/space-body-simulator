const API_BASE = "http://localhost:8000";

export function fetchBodies() {
  return fetch(`${API_BASE}/bodies`).then((res) => res.json());
}

export function createBody(newBody) {
  return fetch(`${API_BASE}/bodies`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newBody),
  }).then((res) => res.json());
}
