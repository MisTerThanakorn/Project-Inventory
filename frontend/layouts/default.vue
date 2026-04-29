<template>
  <div class="app-shell">
    <AppSidebar class="sidebar desktop-sidebar" @navigate="ui.closeSidebar" />

    <Drawer
      v-model:visible="ui.sidebarOpen"
      position="left"
      modal
      :show-close-icon="false"
      class="mobile-drawer"
    >
      <AppSidebar class="mobile-sidebar" @navigate="ui.closeSidebar" />
    </Drawer>

    <div class="content-shell">
      <AppTopbar @menu="ui.toggleSidebar" />
      <main class="content">
        <div class="page">
          <div class="page-inner container">
            <slot />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const ui = useUiStore();
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  position: relative;
}

.content-shell {
  min-height: 100vh;
  margin-left: 304px;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  width: 100%;
}

.page-inner {
  display: grid;
  gap: 1rem;
}

.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  width: 304px;
  z-index: 30;
}

.mobile-sidebar {
  height: 100%;
}

@media (max-width: 960px) {
  .content-shell {
    margin-left: 0;
  }

  .desktop-sidebar {
    display: none;
  }

  :deep(.mobile-drawer) {
    width: min(90vw, 340px);
    border: 0;
    background: transparent;
    box-shadow: none;
    padding: 0;
  }
}

@media (min-width: 961px) {
  :deep(.mobile-drawer) {
    display: none;
  }
}
</style>
