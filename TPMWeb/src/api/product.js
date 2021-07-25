import request from '@/utils/request'

export function apiProductList() {
  return request({
    url: '/api/product/list',
    method: 'get'
  })
}

export function apiProductCreate(requestBody) {
  return request({
    url: '/api/product/create',
    method: 'post',
    data: requestBody
  })
}

