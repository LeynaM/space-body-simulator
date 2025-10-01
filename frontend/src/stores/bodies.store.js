import { create } from "zustand";

export const useBodiesStore = create((set) => ({
  bodies: [],
  createBody: (newBody) =>
    set((state) => ({
      bodies: [...state.bodies, newBody],
    })),
}));
