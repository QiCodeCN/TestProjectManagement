import request from '@/utils/request'

/**
 * 报表服务接口
 * @Author 大奇
 * @WeChat mrzcode
 */

export function requestStacked(data) {
  return request({
    url: '/api/dashboard/stacked',
    method: 'post',
    data
  })
}

export function requestMetaData(data) {
  return request({
    url: '/api/dashboard/metadata',
    method: 'post',
    data
  })
}
