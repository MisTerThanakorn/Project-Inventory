<template>
  <Card class="stat">
    <template #content>
      <p class="label">{{ label }}</p>
      <p class="value">{{ value }}</p>
      <p class="muted">{{ hint }}</p>
    </template>
  </Card>
</template>

<script setup lang="ts">
defineProps<{
  label: string;
  value: string | number;
  hint: string;
}>();
</script>

<style scoped>
.stat {
  height: 100%;
}

.stat :deep(.p-card-body) {
  padding: 1.1rem;
}

.label {
  margin: 0;
  color: var(--muted);
}

.value {
  margin: 0.35rem 0;
  font-size: 1.8rem;
  font-weight: 800;
}
</style>
