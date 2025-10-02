import { create } from "zustand";
import { fetchBodies, createBody } from "./bodies.api";

export const useBodiesStore = create((set) => ({
  bodies: [],
  loadBodies: async () => {
    const bodies = await fetchBodies();
    set({ bodies });
  },
  createBody: async (newBody) => {
    const created = await createBody(newBody);
    set((state) => ({
      bodies: [...state.bodies, created],
    }));
  },
  setBodies: (bodies) => set({ bodies }),
}));
