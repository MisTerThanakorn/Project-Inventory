<template>
  <section class="stack gap-6">
    <section
      class="card overflow-hidden border border-white/10 bg-slate-950/75 p-6 shadow-2xl"
    >
      <div class="flex flex-col gap-6">
        <div class="max-w-3xl">
          <p class="eyebrow">{{ t('items.title') }}</p>
          <h1 class="mt-2 text-3xl font-black tracking-tight text-slate-100 md:text-5xl">
            {{ t('items.headline') }}
          </h1>
          <p class="mt-4 max-w-2xl text-base leading-7 text-slate-400">
            {{ t('items.subtitle') }}
          </p>
        </div>

        <div class="flex flex-wrap gap-3">
          <NuxtLink to="/items/new" class="inline-flex">
            <Button :label="t('items.create')" icon="pi pi-plus" />
          </NuxtLink>
          <Button
            :label="t('items.refresh')"
            icon="pi pi-refresh"
            severity="secondary"
            outlined
            :loading="refreshing"
            @click="refreshItems"
          />
        </div>

        <div class="grid gap-3 text-sm text-slate-300 md:grid-cols-3">
          <div class="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
            <span class="block text-xs uppercase tracking-[0.18em] text-slate-500">
              {{ t('items.live') }}
            </span>
            <strong class="mt-1 block text-base text-slate-100">
              {{ lastSyncedLabel }}
            </strong>
          </div>
          <div class="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
            <span class="block text-xs uppercase tracking-[0.18em] text-slate-500">
              {{ t('items.totalItems') }}
            </span>
            <strong class="mt-1 block text-base text-slate-100">
              {{ totalItems }}
            </strong>
          </div>
          <div class="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
            <span class="block text-xs uppercase tracking-[0.18em] text-slate-500">
              {{ t('items.categories') }}
            </span>
            <strong class="mt-1 block text-base text-slate-100">
              {{ totalCategories }}
            </strong>
          </div>
        </div>
      </div>
    </section>

    <div class="auto-grid">
      <StatCard :label="t('items.totalItems')" :value="totalItems" :hint="t('items.totalHint')" />
      <StatCard :label="t('items.lowStock')" :value="lowStockItems" :hint="t('items.lowHint')" />
      <StatCard :label="t('items.outOfStock')" :value="outOfStockItems" :hint="t('items.outHint')" />
      <StatCard :label="t('items.categories')" :value="totalCategories" :hint="t('items.categoriesHint')" />
    </div>

    <section class="card overflow-hidden border border-white/10 bg-slate-950/70 p-6 shadow-2xl">
      <div class="flex flex-col gap-4 border-b border-white/10 pb-5 md:flex-row md:items-end md:justify-between">
        <div class="max-w-2xl">
          <p class="eyebrow">{{ t('items.quickActions') }}</p>
          <h2 class="mt-2 text-2xl font-semibold text-slate-100">{{ t('items.catalogTitle') }}</h2>
          <p class="mt-2 text-sm leading-6 text-slate-400">
            {{ t('items.catalogCopy') }}
          </p>
        </div>

        <div class="flex flex-wrap gap-3">
          <NuxtLink to="/items/new" class="inline-flex">
            <Button :label="t('items.create')" icon="pi pi-plus" />
          </NuxtLink>
        </div>
      </div>

      <div class="pt-5">
        <InventoryTable :title="t('items.tableTitle')" :items="items" />
      </div>
    </section>
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n();
const itemsStore = useItemsStore();
const { items, summary } = storeToRefs(itemsStore);

definePageMeta({
  middleware: 'auth'
});

const refreshing = ref(false);
const lastSynced = ref<string | null>(null);

const refreshItems = async () => {
  refreshing.value = true;
  try {
    await Promise.all([itemsStore.fetchItems(), itemsStore.fetchSummary()]);
    lastSynced.value = new Date().toISOString();
  } finally {
    refreshing.value = false;
  }
};

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

const lastSyncedLabel = computed(() => {
  if (!lastSynced.value) return t('items.live');
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(lastSynced.value));
});

onMounted(async () => {
  await refreshItems();
});
</script>

<style scoped>
.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.72rem;
  color: var(--accent);
}
</style>
