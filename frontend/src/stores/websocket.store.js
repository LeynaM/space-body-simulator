import { create } from "zustand";

export const useWebsocketStore = create((set, get) => ({
  socket: null,

  connect: (onOpen, onMessage, onClose) => {
    if (get().socket) return;

    // Same origin as the page, so HTTPS deployments get wss:// automatically.
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const socket = new WebSocket(`${protocol}//${window.location.host}/ws`);

    socket.onopen = onOpen;
    socket.onmessage = onMessage;

    socket.onclose = () => {
      onClose();
      set({ socket: null });
    };

    set({ socket });
  },

  disconnect: () => {
    get().socket?.close();
  },
}));
