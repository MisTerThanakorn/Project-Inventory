<template>
  <section class="stack">
    <div class="card section-card toolbar">
      <div>
        <p class="eyebrow">{{ t('items.title') }}</p>
        <h1>Browse and manage stock records.</h1>
        <p class="muted">Fast access to every inventory item with a layout that works on all devices.</p>
      </div>
      <NuxtLink to="/items/new">
        <Button :label="t('items.create')" icon="pi pi-plus" />
      </NuxtLink>
    </div>

    <InventoryTable :title="t('items.title')" :items="items" />
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n();
const itemsStore = useItemsStore();
const { items } = storeToRefs(itemsStore);

definePageMeta({
  middleware: 'auth'
});

onMounted(async () => {
  await itemsStore.fetchItems();
});
</script>

<style scoped>
h1 {
  margin: 0;
  font-size: clamp(1.4rem, 2.5vw, 2rem);
  line-height: 1.15;
  max-width: 18ch;
}

.eyebrow {
  margin: 0 0 0.35rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.72rem;
  color: var(--accent);
}

@media (max-width: 640px) {
  :deep(.p-button) {
    width: 100%;
  }
}
</style>
