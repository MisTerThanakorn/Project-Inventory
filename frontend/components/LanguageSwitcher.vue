<template>
  <div class="switcher">
    <span class="muted">{{ t('language.label') }}</span>
    <Select
      :model-value="locale"
      :options="languageOptions"
      option-label="label"
      option-value="value"
      class="switcher-select"
      @update:model-value="setLocale"
    />
  </div>
</template>

<script setup lang="ts">
const { locale, setLocale, t } = useI18n();

const languageOptions = [
  { label: 'English', value: 'en' },
  { label: 'Thai', value: 'th' }
];
</script>

<style scoped>
.switcher {
  display: grid;
  gap: 0.35rem;
}

.switcher-select {
  min-width: 138px;
}
</style>
