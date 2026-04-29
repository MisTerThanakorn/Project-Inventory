export interface InventoryCategory {
  id: string;
  name: string;
}

export interface InventoryUser {
  id: string;
  fullName: string;
  email: string;
}

export interface InventoryItem {
  id: string;
  sku: string;
  name: string;
  description?: string | null;
  quantity: number;
  minQuantity: number;
  location?: string | null;
  price: string;
  status: 'ACTIVE' | 'LOW_STOCK' | 'OUT_OF_STOCK' | 'DISCONTINUED';
  updatedAt: string;
  category?: InventoryCategory | null;
  createdBy?: InventoryUser | null;
}

export interface InventoryItemInput {
  sku: string;
  name: string;
  description?: string;
  quantity: number;
  minQuantity: number;
  location?: string;
  price: number;
  status: 'ACTIVE' | 'LOW_STOCK' | 'OUT_OF_STOCK' | 'DISCONTINUED';
  categoryId?: string | null;
}

export interface InventorySummary {
  totalItems: number;
  lowStockItems: number;
  outOfStockItems: number;
  totalCategories: number;
}

