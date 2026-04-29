<template>
  <header class="topbar card">
    <span class="topbar-glow topbar-glow-left" aria-hidden="true" />
    <span class="topbar-glow topbar-glow-right" aria-hidden="true" />

    <div class="topbar-inner">
      <div class="title-block">
        <button
          type="button"
          class="menu-btn"
          aria-label="Open menu"
          @click="emit('menu')"
        >
          <i class="pi pi-bars" />
        </button>

        <div class="copy-stack">
          <div class="eyebrow-row">
            <p class="eyebrow">{{ t('topbar.eyebrow') }}</p>
            <span class="section-chip">{{ routeLabel }}</span>
          </div>

          <h2 class="topbar-title">
            {{ title }}
          </h2>

          <p class="subtitle">
            {{ subtitle }}
          </p>
        </div>
      </div>

      <div class="actions">
        <div class="status-cluster">
          <div class="status-copy">
            <p class="eyebrow eyebrow-compact">{{ t('topbar.quickAccess') }}</p>
            <span class="status-pill">{{ t('topbar.live') }}</span>
          </div>
          <LanguageSwitcher />
        </div>

        <NuxtLink to="/items" class="manage-link">
          <i class="pi pi-box" />
          <span>{{ t('topbar.manageItems') }}</span>
        </NuxtLink>
      </div>
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

const routeLabel = computed(() => {
  if (route.path.startsWith('/items')) {
    return t('nav.items');
  }
  if (route.path.startsWith('/login')) {
    return t('nav.login');
  }
  return t('nav.dashboard');
});
</script>

<style scoped>
.topbar {
  position: relative;
  overflow: hidden;
  margin: 1rem 1rem 0;
  border-radius: 24px;
  background:
    radial-gradient(circle at top left, rgba(56, 189, 248, 0.16), transparent 28%),
    radial-gradient(circle at bottom right, rgba(34, 197, 94, 0.1), transparent 24%),
    rgba(15, 23, 42, 0.82);
}

.topbar-inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 340px);
  gap: 1rem;
  padding: 1rem 1.25rem;
  align-items: stretch;
}

.topbar-glow {
  position: absolute;
  inset: auto;
  width: 260px;
  aspect-ratio: 1;
  border-radius: 999px;
  filter: blur(48px);
  opacity: 0.45;
  pointer-events: none;
}

.topbar-glow-left {
  top: -150px;
  left: -120px;
  background: rgba(56, 189, 248, 0.26);
}

.topbar-glow-right {
  right: -130px;
  bottom: -170px;
  background: rgba(34, 197, 94, 0.18);
}

.title-block {
  min-width: 0;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.menu-btn {
  margin-top: 0.15rem;
  inline-size: 46px;
  block-size: 46px;
  flex-shrink: 0;
  display: inline-grid;
  place-items: center;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: #e5e7eb;
  transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease, color 0.18s ease;
}

.menu-btn:hover {
  transform: translateY(-1px);
  border-color: rgba(56, 189, 248, 0.3);
  background: rgba(255, 255, 255, 0.09);
  color: #ffffff;
}

.menu-btn:focus-visible,
.manage-link:focus-visible {
  outline: 2px solid rgba(56, 189, 248, 0.75);
  outline-offset: 3px;
}

.copy-stack {
  min-width: 0;
  display: grid;
  gap: 0.7rem;
}

.eyebrow-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.55rem;
}

.eyebrow {  
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.7rem;
  color: var(--muted);
  margin: 0;
}

.eyebrow-compact {
  margin-bottom: 0;
}

.section-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.32rem 0.7rem;
  border-radius: 999px;
  border: 1px solid rgba(56, 189, 248, 0.2);
  background: rgba(56, 189, 248, 0.08);
  color: #dbeafe;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.topbar-title {
  margin: 0;
  font-size: clamp(1.55rem, 3vw, 2.3rem);
  line-height: 1.05;
  letter-spacing: -0.03em;
  color: #f8fafc;
}

.subtitle {
  margin: 0;
  max-width: 64ch;
  font-size: 0.96rem;
  line-height: 1.65;
  color: var(--muted);
}

.actions {
  display: grid;
  gap: 0.85rem;
  align-content: center;
  padding-left: 1rem;
  border-left: 1px solid rgba(255, 255, 255, 0.08);
}

.status-cluster {
  display: grid;
  gap: 0.8rem;
}

.status-copy {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.34rem 0.72rem;
  border-radius: 999px;
  border: 1px solid rgba(34, 197, 94, 0.2);
  background: rgba(34, 197, 94, 0.1);
  color: #d1fae5;
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.status-pill::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--accent-2);
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1);
}

.manage-link {
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.8rem 1rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.03);
  color: #e2e8f0;
  font-size: 0.95rem;
  font-weight: 600;
  transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease, color 0.18s ease;
}

.manage-link:hover {
  transform: translateY(-1px);
  border-color: rgba(56, 189, 248, 0.35);
  background: rgba(56, 189, 248, 0.08);
  color: #ffffff;
}

.manage-link i {
  font-size: 0.95rem;
}

.actions :deep(.switcher) {
  justify-items: end;
  gap: 0.35rem;
}

.actions :deep(.switcher-select) {
  min-width: 160px;
}

@media (max-width: 960px) {
  .topbar {
    margin: 0 0 0.85rem;
    border-radius: 0 0 20px 20px;
  }

  .topbar-inner {
    grid-template-columns: 1fr;
    padding: 0.95rem 1rem 1rem;
  }

  .title-block {
    padding-bottom: 0.95rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .actions {
    width: 100%;
    padding-left: 0;
    border-left: 0;
  }

  .status-copy {
    align-items: flex-start;
  }

  .actions :deep(.switcher) {
    justify-items: start;
  }

  .actions :deep(.switcher-select) {
    min-width: 0;
    width: 100%;
  }

  .manage-link {
    width: 100%;
  }
}
</style>
