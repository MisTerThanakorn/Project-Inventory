import { defineStore } from 'pinia';
import type { InventoryItem, InventoryItemInput, InventorySummary } from '~/types/inventory';
import { useAuthStore } from './auth';

const demoItems: InventoryItem[] = [
  {
    id: 'demo-1',
    sku: 'INV-001',
    name: 'Wireless Scanner',
    description: 'Barcode scanner for warehouse operations',
    quantity: 18,
    minQuantity: 6,
    location: 'A1-04',
    price: '2490.00',
    status: 'ACTIVE',
    updatedAt: new Date().toISOString(),
    category: { id: 'cat-1', name: 'Hardware' },
    createdBy: { id: 'demo-user', fullName: 'Demo User', email: 'demo@inventory.local' }
  },
  {
    id: 'demo-2',
    sku: 'INV-002',
    name: 'Packing Labels',
    description: 'Thermal labels for outgoing shipments',
    quantity: 4,
    minQuantity: 10,
    location: 'B2-01',
    price: '320.00',
    status: 'LOW_STOCK',
    updatedAt: new Date().toISOString(),
    category: { id: 'cat-2', name: 'Supplies' },
    createdBy: { id: 'demo-user', fullName: 'Demo User', email: 'demo@inventory.local' }
  },
  {
    id: 'demo-3',
    sku: 'INV-003',
    name: 'Tablet Dock',
    description: 'Charging dock for inventory tablets',
    quantity: 0,
    minQuantity: 3,
    location: 'C1-07',
    price: '1590.00',
    status: 'OUT_OF_STOCK',
    updatedAt: new Date().toISOString(),
    category: { id: 'cat-1', name: 'Hardware' },
    createdBy: { id: 'demo-user', fullName: 'Demo User', email: 'demo@inventory.local' }
  }
];

const demoSummary: InventorySummary = {
  totalItems: demoItems.length,
  lowStockItems: demoItems.filter((item) => item.status === 'LOW_STOCK').length,
  outOfStockItems: demoItems.filter((item) => item.status === 'OUT_OF_STOCK').length,
  totalCategories: new Set(demoItems.map((item) => item.category?.id).filter(Boolean)).size
};

export const useItemsStore = defineStore('items', () => {
  const items = ref<InventoryItem[]>([]);
  const summary = ref<InventorySummary | null>(null);
  const pending = ref(false);

  const auth = useAuthStore();

  const authHeaders = () => {
    if (!auth.token) {
      return null;
    }

    return {
      Authorization: `Bearer ${auth.token}`
    };
  };

  const fetchItems = async () => {
    pending.value = true;
    try {
      const headers = authHeaders();
      if (!headers) {
        items.value = demoItems;
        return;
      }

      const response = await $fetch<{ success: boolean; data: InventoryItem[] }>('/api/items', {
        headers
      });
      items.value = response.data;
    } catch {
      items.value = demoItems;
    } finally {
      pending.value = false;
    }
  };

  const fetchSummary = async () => {
    const headers = authHeaders();
    if (!headers) {
      summary.value = demoSummary;
      return;
    }

    try {
      const response = await $fetch<{ success: boolean; data: InventorySummary }>(
        '/api/dashboard/summary',
        {
          headers
        }
      );
      summary.value = response.data;
    } catch {
      summary.value = demoSummary;
    }
  };

  const saveItem = async (input: InventoryItemInput, id?: string) => {
    const headers = authHeaders();
    if (!headers) {
      const savedItem: InventoryItem = {
        id: id || `demo-${Date.now()}`,
        sku: input.sku,
        name: input.name,
        description: input.description || null,
        quantity: input.quantity,
        minQuantity: input.minQuantity,
        location: input.location || null,
        price: input.price.toFixed(2),
        status: input.status,
        updatedAt: new Date().toISOString(),
        category: null,
        createdBy: { id: 'demo-user', fullName: 'Demo User', email: 'demo@inventory.local' }
      };
      return savedItem;
    }

    const response = await $fetch<{ success: boolean; data: InventoryItem }>(
      id ? `/api/items/${id}` : '/api/items',
      {
        method: id ? 'PATCH' : 'POST',
        headers,
        body: input
      }
    );

    return response.data;
  };

  return { items, summary, pending, fetchItems, fetchSummary, saveItem };
});
