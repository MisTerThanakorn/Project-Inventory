<template>
  <form class="card form" @submit.prevent="submit">
    <div class="grid cols-2">
      <label class="field">
        <span>{{ t('items.sku') }}</span>
        <InputText v-model="model.sku" required fluid />
      </label>
      <label class="field">
        <span>{{ t('items.name') }}</span>
        <InputText v-model="model.name" required fluid />
      </label>
      <label class="field">
        <span>{{ t('items.quantity') }}</span>
        <InputNumber v-model="model.quantity" :min="0" fluid />
      </label>
      <label class="field">
        <span>{{ t('items.minQuantity') }}</span>
        <InputNumber v-model="model.minQuantity" :min="0" fluid />
      </label>
      <label class="field">
        <span>{{ t('items.price') }}</span>
        <InputNumber
          v-model="model.price"
          :min="0"
          :min-fraction-digits="2"
          :max-fraction-digits="2"
          fluid
        />
      </label>
      <label class="field">
        <span>{{ t('items.status') }}</span>
        <Select v-model="model.status" :options="statusOptions" option-label="label" option-value="value" fluid />
      </label>
    </div>

    <label class="field">
      <span>{{ t('items.description') }}</span>
      <Textarea v-model="model.description" rows="4" auto-resize fluid />
    </label>

    <div class="actions">
      <Button type="submit" :label="submitLabel" icon="pi pi-save" />
      <NuxtLink to="/items">
        <Button :label="t('common.cancel')" severity="secondary" outlined />
      </NuxtLink>
    </div>
  </form>
</template>

<script setup lang="ts">
import type { InventoryItemInput } from '~/types/inventory';

const props = defineProps<{
  modelValue: InventoryItemInput;
  submitLabel: string;
}>();

const emit = defineEmits<{
  (event: 'submit', value: InventoryItemInput): void;
}>();

const { t } = useI18n();

const statusOptions = [
  { label: 'ACTIVE', value: 'ACTIVE' },
  { label: 'LOW_STOCK', value: 'LOW_STOCK' },
  { label: 'OUT_OF_STOCK', value: 'OUT_OF_STOCK' },
  { label: 'DISCONTINUED', value: 'DISCONTINUED' }
];

const model = reactive<InventoryItemInput>({ ...props.modelValue });

watch(
  () => props.modelValue,
  (value) => {
    Object.assign(model, value);
  },
  { deep: true, immediate: true }
);

const submit = () => emit('submit', { ...model });
</script>

<style scoped>
.form {
  padding: 1.1rem;
  display: grid;
  gap: 1rem;
}

.actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.actions :deep(.p-button) {
  min-width: 140px;
}

@media (max-width: 640px) {
  .form {
    padding: 1rem;
  }

  .actions :deep(.p-button) {
    width: 100%;
    min-width: 0;
  }
}
</style>
