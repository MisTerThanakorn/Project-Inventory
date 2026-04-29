<template>
  <header class="topbar">
    <div class="title-block">
      <Button class="menu-btn" icon="pi pi-bars" text rounded aria-label="Open menu" @click="emit('menu')" />
      <p class="eyebrow">{{ t('topbar.eyebrow') }}</p>
      <h2>{{ title }}</h2>
      <p class="subtitle muted">{{ subtitle }}</p>
    </div>

    <div class="actions">
      <LanguageSwitcher />
      <NuxtLink to="/items">
        <Button :label="t('topbar.manageItems')" icon="pi pi-box" severity="secondary" outlined />
      </NuxtLink>
    </div>
  </header>
</template>

<script setup lang="ts">
const { t } = useI18n();
const route = useRoute();
const emit = defineEmits<{
  (event: 'menu'): void;
}>();

const title = computed(() => {
  if (route.path.startsWith('/items')) {
    return t('nav.items');
  }
  if (route.path.startsWith('/login')) {
    return t('nav.login');
  }
  return t('nav.dashboard');
});

const subtitle = computed(() => {
  if (route.path.startsWith('/login')) {
    return 'Secure access for your inventory workspace';
  }
  if (route.path.startsWith('/items')) {
    return 'Browse, edit, and organize stock records';
  }
  return 'A responsive control center for your operations';
});
</script>

<style scoped>
.topbar {
  margin: 1rem 1rem 0;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  border: 1px solid var(--border);
  border-radius: 24px;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.7), rgba(15, 23, 42, 0.46));
  backdrop-filter: blur(18px);
}

.title-block {
  min-width: 0;
}

.menu-btn {
  display: none;
  margin-bottom: 0.8rem;
}

.eyebrow {
  margin: 0 0 0.2rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 0.72rem;
  color: var(--muted);
}

h2 {
  margin: 0;
  font-size: clamp(1.35rem, 2vw, 1.7rem);
}

.subtitle {
  margin: 0.4rem 0 0;
  max-width: 46ch;
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

@media (max-width: 960px) {
  .topbar {
    margin: 0;
    padding: 1rem;
    border-radius: 0 0 20px 20px;
    flex-direction: column;
  }

  .menu-btn {
    display: inline-flex;
  }

  .actions {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
  }
}
</style>
