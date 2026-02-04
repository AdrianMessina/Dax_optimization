import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true, // Falla si el puerto está en uso en lugar de usar otro
    open: true, // Abre el navegador automáticamente
  },
})
