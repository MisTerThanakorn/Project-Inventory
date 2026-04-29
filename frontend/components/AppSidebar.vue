<template>
  <aside class="sidebar card m-4">
    <div class="brand">
      <div class="logo">PI</div>
      <div class="brand-copy">
        <h1>Project Inventory</h1>
        <p class="muted">Inventory control for modern teams</p>
      </div>
    </div>

    <nav class="nav">
      <NuxtLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        custom
        v-slot="{ navigate, href, isActive }"
      >
        <a :href="href" class="nav-item" :class="{ active: isActive }" @click.prevent="handleNavigate(navigate)">
          <i :class="item.icon" />
          <span>{{ item.label }}</span>
        </a>
      </NuxtLink>
    </nav>

    <div class="footer">
      <p class="muted">{{ t('sidebar.caption') }}</p>
      <Tag severity="success" rounded value="Ready for desktop, iPad, and mobile" />
    </div>
  </aside>
</template>

<script setup lang="ts">
const { t } = useI18n();
const emit = defineEmits<{
  (event: 'navigate'): void;
}>();

const navItems = computed(() => [
  { to: '/dashboard', label: t('nav.dashboard'), icon: 'pi pi-chart-bar' },
  { to: '/items', label: t('nav.items'), icon: 'pi pi-warehouse' },
  { to: '/login', label: t('nav.login'), icon: 'pi pi-sign-in' }
]);

const handleNavigate = (navigate: () => void) => {
  navigate();
  emit('navigate');
};
</script>

<style scoped>
.sidebar {
  padding: 1.2rem;
  display: grid;
  gap: 1.2rem;
  min-height: calc(100vh - 2rem);
  border-radius: 24px;
  background: radial-gradient(circle at top right, rgba(56, 189, 248, 0.12), transparent 30%), rgba(15, 23, 42, 0.84);
}

.brand {
  display: flex;
  gap: 0.85rem;
  align-items: center;
}

.logo {
  width: 52px;
  height: 52px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  font-weight: 800;
  letter-spacing: 0.04em;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: #020617;
}

.brand-copy {
  min-width: 0;
}

.brand h1 {
  margin: 0;
  font-size: 1.05rem;
}

.brand p,
.footer p {
  margin: 0.25rem 0 0;
}

.nav {
  display: grid;
  gap: 0.6rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.95rem 1rem;
  border-radius: 14px;
  background: rgba(148, 163, 184, 0.08);
  border: 1px solid transparent;
  transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease;
}

.nav-item.active {
  border-color: rgba(56, 189, 248, 0.35);
  background: rgba(56, 189, 248, 0.12);
}

.nav-item:hover {
  transform: translateX(2px);
  background: rgba(148, 163, 184, 0.12);
}

.footer {
  margin-top: auto;
  padding-top: 0.25rem;
}

.footer :deep(.p-tag) {
  margin-top: 0.8rem;
  width: fit-content;
  background: rgba(34, 197, 94, 0.12);
  color: #d1fae5;
  border: 1px solid rgba(34, 197, 94, 0.18);
}

@media (max-width: 960px) {
  .sidebar {
    margin: 0;
    border-radius: 0;
    width: 100%;
    min-height: 100%;
  }
}
</style>
