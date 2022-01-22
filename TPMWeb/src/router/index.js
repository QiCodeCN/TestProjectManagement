import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  },
  {
    path: '/tmp',
    component: Layout,
    redirect: '/tmp',
    meta: { title: '测试管理', icon: 'testmanger' },
    children: [
      {
        path: '/test',
        name: 'test',
        component: () => import('@/views/test/index'),
        meta: { title: '提测管理', icon: 'request' }
      },
      {
        path: '/commit',
        name: 'commit',
        hidden: true,
        component: () => import('@/views/test/manger/commit'),
        meta: { title: '需求提测' }
      },
      {
        path: '/report',
        name: 'report',
        hidden: true,
        component: () => import('@/views/test/manger/report'),
        meta: { title: '测试报告' }
      },
      {
        path: 'mytest',
        name: 'mytest',
        component: () => import('@/views/test/mydev'),
        meta: { title: '我的提测', icon: 'mydev' }
      },
      {
        path: 'mydev',
        name: 'mydev',
        component: () => import('@/views/test/mydev'),
        meta: { title: '我的测试', icon: 'mytest' }
      }
    ]
  },
  {
    path: '/settings',
    component: Layout,
    redirect: '/settings',
    meta: { title: '基础管理', icon: '设置' },
    children: [{
      path: 'product',
      name: 'Product',
      component: () => import('@/views/product/product'),
      meta: { title: '项目产品分类', icon: '项目管理' }
    },
    {
      path: 'apps',
      name: 'apps',
      component: () => import('@/views/product/apps'),
      meta: { title: '服务应用管理', icon: '应用管理' }
    }
    ]
  },
  {
    path: '/demo',
    component: Layout,
    redirect: '/demo',
    meta: { title: '演示Demo' },
    children: [{
      path: 'upload',
      name: 'Upload',
      component: () => import('@/views/demo/uploadDemo'),
      meta: { title: '文件上传Demo' }
    },
    {
      path: 'chart',
      name: 'chart',
      component: () => import('@/views/demo/echartsDemo'),
      meta: { title: 'Echarts Demo' }
    }]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
