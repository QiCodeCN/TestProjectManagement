import axios from 'axios';
import type { TableData } from '@arco-design/web-vue/es/table/interface';

export interface productData {
  id: number;
  title: string;
  keyCode: string;
  desc: string;
  operator: string;
};

export function apiProductAdd(data: productData) {
  return axios.post('/api/product/create', data);
}

export function apiProductUpdate(data: productData) {
  return axios.post('/api/product/update', data);
}

export function apiProductDelete(id: number) {
  return axios.delete('/api/product/delete', {
    params: {id}
  });
}

export function apiProductRemove(id: number) {
  return axios.post(`/api/product/remove?id=${id}`);
}

export function apiProductList() {
  return axios.get<TableData[]>('/api/product/list');
}

export interface productParams {
  title: string;
  keyCode: string;
};
export function apiProductSearch(data: productParams) {
  return axios.get<TableData[]>('/api/product/search',{
    params: data
  });
}

export interface productPageParams {
  title: string;
  keyCode: string;
  pageSize: number,
  currentPage: number
};
export function apiProductSearchPage(data: productPageParams) {
  return axios.get<TableData[]>('/api/product/searchPage',{
    params: data
  });
}
