<template>
  <section class="stack">
    <section class="hero card">
      <div>
        <p class="eyebrow">{{ t('dashboard.title') }}</p>
        <h1>Keep stock moving with a clear, responsive workspace.</h1>
        <p class="muted">
          Monitor inventory, review low-stock items, and manage records from any screen size.
        </p>
      </div>
      <div class="hero-chip">
        <span class="chip-dot" />
        Live inventory overview
      </div>
    </section>

    <div class="auto-grid">
      <StatCard :label="t('dashboard.items')" :value="summary?.totalItems ?? 0" hint="All tracked items" />
      <StatCard :label="t('dashboard.lowStock')" :value="summary?.lowStockItems ?? 0" hint="Items below threshold" />
      <StatCard :label="t('dashboard.outOfStock')" :value="summary?.outOfStockItems ?? 0" hint="Needs replenishment" />
      <StatCard :label="t('dashboard.categories')" :value="summary?.totalCategories ?? 0" hint="Catalog structure" />
    </div>

    <section class="card section-card">
      <h3 class="section-title">{{ t('dashboard.categories') }}</h3>
      <p class="muted">{{ summary?.totalCategories ?? 0 }} categories available.</p>
    </section>

    <InventoryTable :title="t('items.title')" :items="items" />
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n();
const auth = useAuthStore();
const itemsStore = useItemsStore();

definePageMeta({
  middleware: 'auth'
});

const { items, summary } = storeToRefs(itemsStore);

onMounted(async () => {
  await Promise.all([auth.loadMe(), itemsStore.fetchSummary(), itemsStore.fetchItems()]);
});
</script>

<style scoped>
.hero {
  padding: 1.4rem;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  background:
    radial-gradient(circle at top right, rgba(56, 189, 248, 0.16), transparent 28%),
    rgba(15, 23, 42, 0.76);
}

.hero h1 {
  margin: 0.15rem 0 0.55rem;
  font-size: clamp(1.6rem, 3vw, 2.3rem);
  line-height: 1.1;
  max-width: 12ch;
}

.hero p {
  margin: 0;
  max-width: 62ch;
}

.hero-chip {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.75rem 0.9rem;
  border-radius: 999px;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.18);
  color: #d1fae5;
}

.chip-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: #22c55e;
  box-shadow: 0 0 0 5px rgba(34, 197, 94, 0.12);
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.72rem;
  color: var(--accent);
}

@media (max-width: 960px) {
  .hero {
    align-items: flex-start;
    flex-direction: column;
  }

  .hero h1 {
    max-width: none;
  }
}
</style>
