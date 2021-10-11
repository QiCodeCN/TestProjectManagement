import request from '@/utils/request'

export function apiTestSearch(requestBody) {
  return request({
    url: '/api/test/search',
    method: 'post',
    data: requestBody
  })
}
