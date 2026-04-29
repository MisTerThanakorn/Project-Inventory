<template>
  <section class="stack dashboard">
    <section class="hero card">
      <div class="hero-copy">
        <p class="eyebrow">{{ t('dashboard.title') }}</p>
        <h1>{{ t('dashboard.headline') }}</h1>
        <p class="muted">
          {{ t('dashboard.subtitle') }}
        </p>

        <div class="hero-actions">
          <NuxtLink to="/items/new" class="action-link">
            <Button :label="t('dashboard.addItem')" icon="pi pi-plus" />
          </NuxtLink>
          <NuxtLink to="/items" class="action-link">
            <Button
              :label="t('dashboard.viewItems')"
              icon="pi pi-list"
              severity="secondary"
              outlined
            />
          </NuxtLink>
          <Button
            :label="t('dashboard.refresh')"
            icon="pi pi-refresh"
            text
            :loading="refreshing"
            @click="refreshDashboard"
          />
        </div>
      </div>

      <div class="hero-panel">
        <div class="ring-visual">
          <div class="progress-ring" :style="{ '--progress': `${healthyRate}%` }">
            <div class="progress-copy">
              <strong>{{ healthyRate }}%</strong>
              <span>{{ t('dashboard.healthy') }}</span>
            </div>
          </div>

          <div class="mini-metrics">
            <div class="mini-metric">
              <span>{{ t('dashboard.attention') }}</span>
              <strong>{{ attentionCount }}</strong>
            </div>
            <div class="mini-metric">
              <span>{{ t('dashboard.categories') }}</span>
              <strong>{{ totalCategories }}</strong>
            </div>
            <div class="mini-metric">
              <span>{{ t('dashboard.lastUpdated') }}</span>
              <strong>{{ lastSyncedLabel }}</strong>
            </div>
          </div>
        </div>

        <div class="panel-summary">
          <p class="section-kicker">{{ t('dashboard.quickActions') }}</p>
          <p class="muted">{{ t('dashboard.summaryCopy') }}</p>
        </div>
      </div>
    </section>

    <div class="auto-grid">
      <StatCard :label="t('dashboard.items')" :value="totalItems" :hint="t('dashboard.itemsHint')" />
      <StatCard
        :label="t('dashboard.lowStock')"
        :value="lowStockItems"
        :hint="t('dashboard.lowStockHint')"
      />
      <StatCard
        :label="t('dashboard.outOfStock')"
        :value="outOfStockItems"
        :hint="t('dashboard.outOfStockHint')"
      />
      <StatCard
        :label="t('dashboard.categories')"
        :value="totalCategories"
        :hint="t('dashboard.categoriesHint')"
      />
    </div>

    <div class="dashboard-grid">
      <section class="card section-card insight-card">
        <div class="section-head">
          <div>
            <p class="section-kicker">{{ t('dashboard.health') }}</p>
            <h3 class="section-title">{{ t('dashboard.healthTitle') }}</h3>
          </div>
          <Tag :value="healthLabel" :severity="healthSeverity" rounded />
        </div>

        <div class="bars">
          <div class="bar-row">
            <div class="bar-row-header">
              <span>{{ t('dashboard.healthy') }}</span>
              <strong>{{ healthyItems }}</strong>
            </div>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: `${healthyRate}%` }" />
            </div>
          </div>

          <div class="bar-row">
            <div class="bar-row-header">
              <span>{{ t('dashboard.lowStock') }}</span>
              <strong>{{ lowStockItems }}</strong>
            </div>
            <div class="bar-track">
              <div class="bar-fill is-warn" :style="{ width: `${lowStockRate}%` }" />
            </div>
          </div>

          <div class="bar-row">
            <div class="bar-row-header">
              <span>{{ t('dashboard.outOfStock') }}</span>
              <strong>{{ outOfStockItems }}</strong>
            </div>
            <div class="bar-track">
              <div class="bar-fill is-danger" :style="{ width: `${outOfStockRate}%` }" />
            </div>
          </div>
        </div>
      </section>

      <section class="card section-card insight-card">
        <div class="section-head">
          <div>
            <p class="section-kicker">{{ t('dashboard.watchlist') }}</p>
            <h3 class="section-title">{{ t('dashboard.watchlistTitle') }}</h3>
          </div>
          <Tag :value="`${attentionItems.length}`" severity="warn" rounded />
        </div>

        <div v-if="attentionItems.length" class="watchlist">
          <article v-for="item in attentionItems" :key="item.id" class="watch-item">
            <div class="watch-top">
              <div>
                <p class="watch-name">{{ item.name }}</p>
                <p class="watch-meta">
                  <span>{{ item.sku }}</span>
                  <span v-if="item.category?.name">{{ item.category.name }}</span>
                  <span v-if="item.location">{{ item.location }}</span>
                </p>
              </div>

              <Tag :value="statusLabel(item.status)" :severity="statusSeverity(item.status)" rounded />
            </div>

            <div class="watch-footer">
              <span>{{ item.quantity }} / {{ item.minQuantity }}</span>
              <span>{{ formatDate(item.updatedAt) }}</span>
            </div>
          </article>
        </div>

        <div v-else class="empty-state">
          {{ t('dashboard.emptyWatchlist') }}
        </div>
      </section>
    </div>

    <section class="card section-card">
      <div class="section-head">
        <div>
          <p class="section-kicker">{{ t('dashboard.recentActivity') }}</p>
          <h3 class="section-title">{{ t('dashboard.recentTitle') }}</h3>
        </div>
        <p class="muted">{{ recentItems.length }} {{ t('dashboard.itemsLower') }}</p>
      </div>

      <div class="recent-grid">
        <article v-for="item in recentItems" :key="item.id" class="recent-item">
          <div class="recent-copy">
            <p class="recent-name">{{ item.name }}</p>
            <p class="muted">{{ item.sku }} - {{ item.category?.name || t('dashboard.noCategory') }}</p>
          </div>
          <div class="recent-meta">
            <Tag :value="statusLabel(item.status)" :severity="statusSeverity(item.status)" rounded />
            <span class="muted">{{ formatDate(item.updatedAt) }}</span>
          </div>
        </article>
      </div>
    </section>

    <InventoryTable :title="t('items.title')" :items="items" />
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n();
const auth = useAuthStore();
const itemsStore = useItemsStore();
const refreshing = ref(false);
const lastSynced = ref<string | null>(null);

definePageMeta({
  middleware: 'auth'
});

const { items, summary } = storeToRefs(itemsStore);

const refreshDashboard = async () => {
  refreshing.value = true;
  try {
    await Promise.all([auth.loadMe(), itemsStore.fetchSummary(), itemsStore.fetchItems()]);
    lastSynced.value = new Date().toISOString();
  } finally {
    refreshing.value = false;
  }
};

const formatDate = (value: string) =>
  new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(value));

const sortedItems = computed(() =>
  [...items.value].sort((left, right) => new Date(right.updatedAt).getTime() - new Date(left.updatedAt).getTime())
);

const recentItems = computed(() => sortedItems.value.slice(0, 4));

const statusPriority = {
  OUT_OF_STOCK: 0,
  LOW_STOCK: 1,
  ACTIVE: 2,
  DISCONTINUED: 3
} as const;

const attentionItems = computed(() =>
  [...items.value]
    .filter((item) => item.status === 'LOW_STOCK' || item.status === 'OUT_OF_STOCK')
    .sort((left, right) => {
      const priorityDiff = statusPriority[left.status] - statusPriority[right.status];
      if (priorityDiff !== 0) return priorityDiff;
      return new Date(right.updatedAt).getTime() - new Date(left.updatedAt).getTime();
    })
    .slice(0, 4)
);

const totalItems = computed(() => summary.value?.totalItems ?? items.value.length);
const lowStockItems = computed(
  () => summary.value?.lowStockItems ?? items.value.filter((item) => item.status === 'LOW_STOCK').length
);
const outOfStockItems = computed(
  () => summary.value?.outOfStockItems ?? items.value.filter((item) => item.status === 'OUT_OF_STOCK').length
);
const totalCategories = computed(
  () =>
    summary.value?.totalCategories ??
    new Set(items.value.map((item) => item.category?.id).filter((id): id is string => Boolean(id))).size
);
const healthyItems = computed(() => Math.max(totalItems.value - lowStockItems.value - outOfStockItems.value, 0));
const attentionCount = computed(() => lowStockItems.value + outOfStockItems.value);
const healthyRate = computed(() => {
  if (!totalItems.value) return 0;
  return Math.round((healthyItems.value / totalItems.value) * 100);
});
const lowStockRate = computed(() => {
  if (!totalItems.value) return 0;
  return Math.round((lowStockItems.value / totalItems.value) * 100);
});
const outOfStockRate = computed(() => {
  if (!totalItems.value) return 0;
  return Math.round((outOfStockItems.value / totalItems.value) * 100);
});

const statusLabel = (status: string) => {
  if (status === 'ACTIVE') return 'In stock';
  if (status === 'LOW_STOCK') return 'Low stock';
  if (status === 'OUT_OF_STOCK') return 'Out of stock';
  return 'Discontinued';
};

const statusSeverity = (status: string): 'success' | 'warn' | 'danger' | 'secondary' => {
  if (status === 'ACTIVE') return 'success';
  if (status === 'LOW_STOCK') return 'warn';
  if (status === 'OUT_OF_STOCK') return 'danger';
  return 'secondary';
};

const healthLabel = computed(() => {
  if (!attentionCount.value) return 'Stable';
  if (outOfStockItems.value > 0) return 'Critical';
  return 'Watch';
});

const healthSeverity = computed<'success' | 'warn' | 'danger'>(() => {
  if (!attentionCount.value) return 'success';
  if (outOfStockItems.value > 0) return 'danger';
  return 'warn';
});

const lastSyncedLabel = computed(() => (lastSynced.value ? formatDate(lastSynced.value) : 'Live'));

onMounted(async () => {
  await refreshDashboard();
});
</script>

<style scoped>
.dashboard {
  gap: 1rem;
}

.hero {
  padding: 1.4rem;
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.8fr);
  gap: 1rem;
  background:
    radial-gradient(circle at top right, rgba(56, 189, 248, 0.16), transparent 28%),
    radial-gradient(circle at bottom left, rgba(34, 197, 94, 0.12), transparent 24%),
    rgba(15, 23, 42, 0.76);
}

.hero-copy {
  display: grid;
  align-content: start;
  gap: 0.9rem;
}

.hero h1 {
  margin: 0;
  font-size: clamp(2rem, 4vw, 3.2rem);
  line-height: 1.02;
  max-width: 12ch;
}

.hero p {
  margin: 0;
  max-width: 62ch;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.35rem;
}

.action-link {
  display: flex;
}

.action-link :deep(.p-button) {
  width: 100%;
}

.hero-panel {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: rgba(2, 6, 23, 0.36);
}

.ring-visual {
  display: grid;
  grid-template-columns: 110px minmax(0, 1fr);
  gap: 1rem;
  align-items: center;
}

.progress-ring {
  width: 110px;
  aspect-ratio: 1;
  border-radius: 50%;
  background: conic-gradient(var(--accent-2) 0 var(--progress), rgba(148, 163, 184, 0.15) var(--progress) 100%);
  position: relative;
}

.progress-ring::after {
  content: '';
  position: absolute;
  inset: 12px;
  border-radius: 50%;
  background: rgba(15, 23, 42, 0.96);
  border: 1px solid var(--border);
}

.progress-copy {
  position: absolute;
  inset: 12px;
  z-index: 1;
  display: grid;
  place-items: center;
  text-align: center;
}

.progress-copy strong {
  display: block;
  font-size: 1.55rem;
  line-height: 1;
}

.progress-copy span {
  color: var(--muted);
  font-size: 0.82rem;
}

.mini-metrics {
  display: grid;
  gap: 0.75rem;
}

.mini-metric {
  padding: 0.8rem 0.9rem;
  border-radius: 18px;
  background: rgba(148, 163, 184, 0.06);
  border: 1px solid var(--border);
}

.mini-metric span {
  display: block;
  color: var(--muted);
  font-size: 0.88rem;
}

.mini-metric strong {
  display: block;
  margin-top: 0.2rem;
  font-size: 1.08rem;
}

.panel-summary {
  padding-top: 0.15rem;
}

.panel-summary .muted {
  max-width: none;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.insight-card {
  display: grid;
  gap: 1rem;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.section-kicker {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.72rem;
  color: var(--muted);
}

.section-title {
  margin: 0.35rem 0 0;
}

.bars {
  display: grid;
  gap: 0.85rem;
}

.bar-row {
  display: grid;
  gap: 0.4rem;
}

.bar-row-header {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  font-size: 0.94rem;
}

.bar-track {
  height: 10px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(148, 163, 184, 0.12);
  border: 1px solid var(--border);
}

.bar-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
}

.bar-fill.is-warn {
  background: linear-gradient(90deg, #f59e0b, #f97316);
}

.bar-fill.is-danger {
  background: linear-gradient(90deg, #f97316, var(--danger));
}

.watchlist {
  display: grid;
  gap: 0.75rem;
}

.watch-item {
  padding: 0.9rem 1rem;
  border-radius: 18px;
  background: rgba(148, 163, 184, 0.06);
  border: 1px solid var(--border);
  display: grid;
  gap: 0.65rem;
}

.watch-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
}

.watch-name {
  margin: 0;
  font-weight: 700;
}

.watch-meta,
.watch-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem 0.85rem;
  color: var(--muted);
  font-size: 0.88rem;
}

.watch-footer {
  justify-content: space-between;
}

.empty-state {
  padding: 1rem;
  border-radius: 18px;
  border: 1px dashed var(--border);
  background: rgba(148, 163, 184, 0.04);
  color: var(--muted);
}

.recent-grid {
  display: grid;
  gap: 0.75rem;
}

.recent-item {
  padding: 0.95rem 1rem;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: rgba(148, 163, 184, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.recent-copy,
.recent-meta {
  display: grid;
  gap: 0.35rem;
}

.recent-name {
  margin: 0;
  font-weight: 700;
}

@media (max-width: 960px) {
  .hero,
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .hero h1 {
    max-width: none;
  }

  .ring-visual {
    grid-template-columns: 1fr;
    justify-items: start;
  }

  .progress-ring {
    margin-inline: auto;
  }

  .watch-top,
  .recent-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .watch-footer {
    justify-content: flex-start;
  }
}
</style>
