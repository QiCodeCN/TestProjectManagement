import { DEFAULT_LAYOUT } from '@/router/constants';

export default {
  path: '/config',
  name: 'Config',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.config',
    requiresAuth: true,
    icon: 'icon-settings',
    order: 0,
  },
  children: [
    {
      path: '/product',
      name: 'Product',
      component: ()=> import('@/views/product/index.vue'),
      meta: {
        locale: 'menu.config.product',
        requiresAuth: false,
      }
    }
  ],
};
