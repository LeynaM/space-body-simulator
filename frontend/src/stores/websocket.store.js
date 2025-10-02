import { create } from "zustand";

export const useWebsocketStore = create((set, get) => ({
  socket: null,

  connect: (onOpen, onMessage, onClose) => {
    if (get().socket) return;

    const socket = new WebSocket("ws://localhost:8000/ws");

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
