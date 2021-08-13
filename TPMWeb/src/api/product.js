import request from '@/utils/request'

// 调用信息查询结果
export function apiProductList() {
  return request({
    url: '/api/product/list',
    method: 'get'
  })
}

// 条件查询
export function apiProductSearch(params) {
  return request({
    url: '/api/product/search',
    method: 'get',
    params: params
  })
}

// 调用项目增加接口
export function apiProductCreate(requestBody) {
  return request({
    url: '/api/product/create',
    method: 'post',
    data: requestBody
  })
}

// 调用更新项目接口
export function apiProductUpdate(requestBody) {
  return request({
    url: '/api/product/update',
    method: 'post',
    data: requestBody
  })
}

// 调用真实删除数据库接口
export function apiProductDelete(id) {
  return request({
    url: '/api/product/delete',
    method: 'delete',
    params: {
      'id': id
    }
  })
}

// 软删除，更改数据状态
export function apiProductRemove(id) {
  return request({
    url: '/api/product/remove',
    method: 'post',
    params: {
      'id': id
    }
  })
}

