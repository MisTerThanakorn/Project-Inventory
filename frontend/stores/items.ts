import { defineStore } from 'pinia';
import type { InventoryItem, InventoryItemInput, InventorySummary } from '~/types/inventory';
import { useAuthStore } from './auth';

export const useItemsStore = defineStore('items', () => {
  const items = ref<InventoryItem[]>([]);
  const summary = ref<InventorySummary | null>(null);
  const pending = ref(false);

  const auth = useAuthStore();

  const authHeaders = () => ({
    Authorization: `Bearer ${auth.token.value}`
  });

  const fetchItems = async () => {
    pending.value = true;
    try {
      const response = await $fetch<{ success: boolean; data: InventoryItem[] }>('/api/items', {
        headers: authHeaders()
      });
      items.value = response.data;
    } finally {
      pending.value = false;
    }
  };

  const fetchSummary = async () => {
    const response = await $fetch<{ success: boolean; data: InventorySummary }>(
      '/api/dashboard/summary',
      {
        headers: authHeaders()
      }
    );
    summary.value = response.data;
  };

  const saveItem = async (input: InventoryItemInput, id?: string) => {
    const response = await $fetch<{ success: boolean; data: InventoryItem }>(
      id ? `/api/items/${id}` : '/api/items',
      {
        method: id ? 'PATCH' : 'POST',
        headers: authHeaders(),
        body: input
      }
    );

    return response.data;
  };

  return { items, summary, pending, fetchItems, fetchSummary, saveItem };
});

