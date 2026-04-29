<template>
  <Card class="stat">
    <template #content>
      <div class="stat-inner">
        <span class="accent" />
        <p class="label">{{ label }}</p>
        <p class="value">{{ value }}</p>
        <p class="muted">{{ hint }}</p>
      </div>
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
  position: relative;
  overflow: hidden;
  border: 1px solid var(--border);
  background:
    radial-gradient(circle at top right, rgba(56, 189, 248, 0.16), transparent 30%),
    linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.84));
  box-shadow: var(--shadow);
}

.stat :deep(.p-card-body) {
  padding: 1.1rem;
}

.stat::after {
  content: '';
  position: absolute;
  inset: auto -14% -40% auto;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(34, 197, 94, 0.18), transparent 70%);
  pointer-events: none;
}

.stat-inner {
  position: relative;
  z-index: 1;
}

.accent {
  display: block;
  width: 42px;
  height: 4px;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  margin-bottom: 0.85rem;
}

.label {
  margin: 0;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 0.74rem;
}

.value {
  margin: 0.35rem 0 0.2rem;
  font-size: 2rem;
  font-weight: 800;
  line-height: 1;
  color: #f8fafc;
}
</style>
