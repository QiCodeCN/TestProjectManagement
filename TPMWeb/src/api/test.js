import request from '@/utils/request'

export function apiTestSearch(requestBody) {
  return request({
    url: '/api/test/search',
    method: 'post',
    data: requestBody
  })
}

export function reqCreate(body) {
  return request({
    url: '/api/test/create',
    method: 'post',
    data: body
  })
}

export function apiTestInfo(id) {
  return request({
    url: '/api/test/info',
    method: 'get',
    params: { id }
  })
}

export function reqUpdate(body) {
  return request({
    url: '/api/test/update',
    method: 'post',
    data: body
  })
}

export function changeStatus(body) {
  return request({
    url: '/api/test/change',
    method: 'post',
    data: body
  })
}

export function reportSave(body) {
  return request({
    url: '/api/report/save',
    method: 'post',
    data: body
  })
}

export function reportTestInfo(id) {
  return request({
    url: '/api/report/info',
    method: 'get',
    params: { id }
  })
}
