export function fetchBodies() {
  return fetch("/bodies").then((res) => res.json());
}

export function createBody(newBody) {
  return fetch("/bodies", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newBody),
  }).then((res) => res.json());
}
