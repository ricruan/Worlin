import request from '@/utils/request'

// 执行SQL
export function executeSQL(sql) {
  return request({
    url: '/coding/execute',
    method: 'post',
    data: {
      sql: sql
    }
  })
} 

// 验证SQL
export function validateSQL(data) {
  return request({
    url: '/coding/validate',
    method: 'post',
    data: data
  })
} 