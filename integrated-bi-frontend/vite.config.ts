import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://192.168.224.128:8000',
        changeOrigin: true,
        rewrite: (path) => path,
      },
    },
  },
  // ─── Build prod (Render free tier = 512Mo, on optimise la mémoire) ──────
  build: {
    target: 'es2020',
    sourcemap: false,           // pas de source maps en prod = moins de RAM
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: {
        manualChunks: {
          // Découpe les grosses libs dans des chunks séparés → moins de RAM
          // par fichier à compresser, et meilleur cache navigateur.
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'chart-vendor': ['chart.js', 'vue-chartjs'],
          'ui-vendor': ['@headlessui/vue', 'lucide-vue-next', '@vueuse/core'],
        },
      },
    },
  },
})
