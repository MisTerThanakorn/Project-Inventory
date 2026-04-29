import Aura from '@primeuix/themes/aura';
import process from 'node:process';

export default defineNuxtConfig({
  ssr: true,
  typescript: {
    strict: true
  },
  runtimeConfig: {
    public: {
      backendUrl: process.env.NUXT_PUBLIC_BACKEND_URL || 'http://localhost:4000'
    }
  },
  modules: ['@pinia/nuxt', '@nuxtjs/i18n', '@primevue/nuxt-module'],
  primevue: {
    options: {
      ripple: true,
      inputVariant: 'filled',
      theme: {
        preset: Aura,
        options: {
          darkModeSelector: '.app-dark',
          cssLayer: false
        }
      }
    }
  },
  i18n: {
    defaultLocale: 'en',
    strategy: 'no_prefix',
    langDir: 'lang',
    locales: [
      { code: 'en', file: 'en.json', name: 'English' },
      { code: 'th', file: 'th.json', name: 'Thai' }
    ]
  },
  app: {
    head: {
      title: 'Project Inventory',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Inventory management system' }
      ]
    }
  },
  css: ['primeicons/primeicons.css', '~/assets/css/main.css']
});
