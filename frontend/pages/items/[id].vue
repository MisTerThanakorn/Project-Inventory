<template>
  <section class="grid">
    <div class="card panel">
      <h1>Edit item</h1>
      <p class="muted">Adjust item details and save changes.</p>
    </div>

    <ItemForm v-if="form" :model-value="form" :submit-label="t('common.save')" @submit="submit" />
  </section>
</template>

<script setup lang="ts">
import type { InventoryItemInput } from '~/types/inventory';

const route = useRoute();
const { t } = useI18n();
const auth = useAuthStore();
const itemsStore = useItemsStore();
const form = ref<InventoryItemInput | null>(null);

definePageMeta({
  middleware: 'auth'
});

onMounted(async () => {
  const response = await $fetch<{ success: boolean; data: any }>(`/api/items/${route.params.id}`, {
    headers: {
      Authorization: `Bearer ${auth.token.value}`
    }
  });

  const item = response.data;
  form.value = {
    sku: item.sku,
    name: item.name,
    description: item.description || '',
    quantity: item.quantity,
    minQuantity: item.minQuantity,
    location: item.location || '',
    price: Number(item.price),
    status: item.status,
    categoryId: item.category?.id || null
  };
});

const submit = async (payload: InventoryItemInput) => {
  await itemsStore.saveItem(payload, String(route.params.id));
  await navigateTo('/items');
};
</script>

<style scoped>
.panel {
  padding: 1rem 1.1rem;
}
</style>
