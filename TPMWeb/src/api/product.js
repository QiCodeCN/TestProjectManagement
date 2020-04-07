import request from '@/utils/request'

export function apiProductList() {
  return request({
    url: '/api/product/list',
    method: 'get'
  })
}

