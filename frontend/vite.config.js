import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // The client calls the API on its own origin, which in production is Caddy
  // routing these paths to the backend. Dev needs the same routing locally.
  server: {
    proxy: {
      '/bodies': 'http://localhost:8001',
      '/health': 'http://localhost:8001',
      '/ws': {
        target: 'ws://localhost:8001',
        ws: true,
      },
    },
  },
})
