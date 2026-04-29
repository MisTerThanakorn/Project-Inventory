<template>
  <section class="grid">
    <div class="card panel">
      <h1>{{ t('items.create') }}</h1>
      <p class="muted">Create a new inventory record.</p>
    </div>

    <ItemForm :model-value="form" :submit-label="t('common.save')" @submit="submit" />
  </section>
</template>

<script setup lang="ts">
import type { InventoryItemInput } from '~/types/inventory';

const { t } = useI18n();
const itemsStore = useItemsStore();

definePageMeta({
  middleware: 'auth'
});

const form = ref<InventoryItemInput>({
  sku: '',
  name: '',
  quantity: 0,
  minQuantity: 0,
  price: 0,
  status: 'ACTIVE',
  description: '',
  categoryId: null
});

const submit = async (payload: InventoryItemInput) => {
  await itemsStore.saveItem(payload);
  await navigateTo('/items');
};
</script>

<style scoped>
.panel {
  padding: 1rem 1.1rem;
}
</style>
