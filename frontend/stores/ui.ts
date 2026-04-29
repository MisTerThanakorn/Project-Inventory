import { defineStore } from 'pinia';

export const useUiStore = defineStore('ui', () => {
  const sidebarOpen = ref(false);

  const openSidebar = () => {
    sidebarOpen.value = true;
  };

  const closeSidebar = () => {
    sidebarOpen.value = false;
  };

  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value;
  };

  return { sidebarOpen, openSidebar, closeSidebar, toggleSidebar };
});

