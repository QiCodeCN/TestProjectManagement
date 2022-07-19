<template>
  <a-table :columns="columns" :data="renderList" :pagination="false" />
</template>

<script lang="ts" setup>
  import { apiProductList } from '@/api/product';
  import { ref } from 'vue';
  import { TableData } from '@arco-design/web-vue/es/table/interface';

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
    },
    {
      title: '标识码',
      dataIndex: 'keyCode',
    },
    {
      title: '标题',
      dataIndex: 'title',
    },
    {
      title: '描述',
      dataIndex: 'desc',
    },
    {
      title: '操作者',
      dataIndex: 'operator',
    },
    {
      title: '更新时间',
      dataIndex: 'update',
    },
  ];

  const renderList = ref<TableData[]>();
  const fetchData = async () => {
    try {
      const { data } = await apiProductList();
      renderList.value = data;
    } catch (err) {
      console.log(err);
    }
  };
  fetchData();
</script>

<script lang="ts">
  export default {
    name: 'Product',
  };
</script>

<style scoped></style>
