import {Item} from './Item'

export interface Cart {
  id: string;
  items: Record<string, Item>;
  active: boolean;
  createdAt: Date;
  updatedAt: Date;
  total: number;
  saleDate: Date;
  ref: string;
  receiver: number;
  rec_desc: string;
}
