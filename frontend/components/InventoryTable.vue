<template>
  <section class="card table-wrap table-card">
    <div class="table-head">
      <h3>{{ title }}</h3>
      <slot name="actions" />
    </div>

    <DataTable :value="items" striped-rows responsive-layout="scroll" class="inventory-table">
      <Column field="sku" :header="t('items.sku')" />
      <Column field="name" :header="t('items.name')" />
      <Column field="quantity" :header="t('items.quantity')" />
      <Column :header="t('items.status')">
        <template #body="{ data }">
          <Tag :value="data.status" :severity="statusSeverity(data.status)" rounded />
        </template>
      </Column>
      <Column :header="t('items.category')">
        <template #body="{ data }">
          {{ data.category?.name || '-' }}
        </template>
      </Column>
      <Column :header="t('items.updatedAt')">
        <template #body="{ data }">
          {{ formatDate(data.updatedAt) }}
        </template>
      </Column>
    </DataTable>
  </section>
</template>

<script setup lang="ts">
import type { InventoryItem } from '~/types/inventory';

defineProps<{
  title: string;
  items: InventoryItem[];
}>();

const { t } = useI18n();

const formatDate = (value: string) =>
  new Intl.DateTimeFormat(undefined, { dateStyle: 'medium', timeStyle: 'short' }).format(
    new Date(value)
  );

const statusSeverity = (status: InventoryItem['status']) => {
  if (status === 'ACTIVE') return 'success';
  if (status === 'LOW_STOCK') return 'warn';
  if (status === 'OUT_OF_STOCK') return 'danger';
  return 'contrast';
};
</script>

<style scoped>
.table-wrap {
  padding: 1rem;
}

.table-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.9rem;
}

.inventory-table :deep(.p-datatable-table-container) {
  border-radius: 18px;
  overflow: hidden;
  background: rgba(2, 6, 23, 0.34);
  border: 1px solid var(--border);
}

.inventory-table :deep(.p-datatable-thead > tr > th) {
  background: rgba(148, 163, 184, 0.1);
  color: #e2e8f0;
  border-color: var(--border);
}

.inventory-table :deep(.p-datatable-tbody > tr > td) {
  border-color: var(--border);
  background: rgba(15, 23, 42, 0.34);
}

.inventory-table :deep(.p-datatable-tbody > tr:hover > td) {
  background: rgba(56, 189, 248, 0.08);
}

.inventory-table :deep(.p-tag) {
  font-size: 0.78rem;
}

@media (max-width: 640px) {
  .table-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
