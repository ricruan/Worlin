import request from '@/utils/request'

// 查询问题列表
export function getPageList(query) {
  return request({
    url: '/wr/problem/pagelist',
    method: 'get',
    params: query
  })
}

// 查询问题详细
export function getDetail(id) {
  return request({
    url: '/wr/problem/' + id,
    method: 'get'
  })
}

// 新增或修改问题
export function insertOrUpdate(data) {
  return request({
    url: '/wr/problem/inserOrUpdate',
    method: 'post',
    data: data
  })
}

// 删除问题
export function deleteBatch(ids) {
  return request({
    url: '/wr/problem/deleteBatch',
    method: 'delete',
    params: { ids }
  })
}


