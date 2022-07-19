import axios from 'axios';
import type { TableData } from '@arco-design/web-vue/es/table/interface';

export interface productInfo {
  id: string;
  keyCode: string;
}

export function apiProductList() {
  return axios.get<TableData[]>('/api/product/list');
}
