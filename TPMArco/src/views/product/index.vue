<template>
  <div>
    <a-form :model="productSearch" layout="inline">
      <a-form-item>
        <a-input v-model="productSearch.title" allow-clear placeholder="标题模糊搜索"/>
      </a-form-item>
      <a-form-item>
        <a-input v-model="productSearch.keyCode" allow-clear placeholder="唯一码精确搜索"/>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" @click="btnSearchClick">
          <template #icon>
            <icon-search />
          </template>
          搜索
        </a-button>
      </a-form-item>
    </a-form>
    <a-button type="primary" @click="addButtonClick">添加产品线</a-button>
    <a-modal v-model:visible="addModalVisible" title="添加产品"  @before-ok="addModalOk" @cancel="addModalCancel">
      <a-form :model="productForm">
        <a-form-item field="title" label="名称">
          <a-input v-model="productForm.title" placeholder="产品线名称"/>
        </a-form-item>
        <a-form-item field="keyCode" label="唯一吗">
          <a-input v-model="productForm.keyCode" placeholder="keycode不可重复"/>
        </a-form-item>
        <a-form-item field="desc" label="备注">
          <a-textarea v-model="productForm.desc" placeholder="一些备注说明"/>
        </a-form-item>
      </a-form>
    </a-modal>
    <a-modal v-model:visible="editModalVisible" title="编辑产品"  @before-ok="editModalOk" @cancel="editModalCancel">
      <a-form :model="productForm">
        <a-form-item field="id" label="编号" disabled>
          <a-input v-model="productForm.id" />
        </a-form-item>
        <a-form-item field="title" label="名称">
          <a-input v-model="productForm.title" placeholder="产品线名称"/>
        </a-form-item>
        <a-form-item field="keyCode" label="唯一吗">
          <a-input v-model="productForm.keyCode" placeholder="keycode不可重复"/>
        </a-form-item>
        <a-form-item field="desc" label="备注">
          <a-textarea v-model="productForm.desc" placeholder="一些备注说明"/>
        </a-form-item>
      </a-form>
    </a-modal>
    <a-table :columns="columns" :data="renderList" :pagination="false" >
      <template #optional="{ record }">
        <a-button type="text" @click="editButtonClick(record)">编辑</a-button>
        <a-popconfirm content="你确定要废弃此产品吗？" type="warning" @ok="removeButtonClick(record.id)">
          <a-button type="text">废弃</a-button>
        </a-popconfirm>
        <a-button type="text" @click="delBtnClick(record?.id)">删除</a-button>
      </template>
      <template #update="{ record }">
        <div>{{formatDate(record.update)}}</div>
      </template>
    </a-table>
    <a-pagination
      :total="productTotal"
      :page-size-options=[5,10,20,30,50]
      default-page-size="5"
      @change="pageChange"
      @pageSizeChange="pageSizeChange"
      show-total
      show-page-size

    />
    <a-modal v-model:visible="delModalVisible"
             title="删除产品"
             @before-ok="delModalOk"
             okText="删除"
             :okButtonProps="modalOkPros"
    >
      <div>确定彻底删除此产品吗？</div>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>
  import {
    apiProductList,
    apiProductAdd,
    apiProductUpdate,
    apiProductRemove,
    apiProductDelete,
    apiProductSearch,
    apiProductSearchPage
  } from '@/api/product';
  import { ref, reactive } from 'vue';
  import { TableData } from '@arco-design/web-vue/es/table/interface';
  import moment from "moment";
  import * as Console from "console";

  // 格式化时间，需要依赖 npm install moment
  // import moment from "moment";
  const formatDate = (date) => {
    return moment(date).format('YYYY-MM-DD');
  }

  const columns = [
    {
      title: 'ID', dataIndex: 'id',
      width: 50,
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
      title: '描述', dataIndex: 'desc',
      ellipsis: true,
      tooltip: true,
    },
    {
      title: '操作者',
      dataIndex: 'operator',
    },
    {
      title: '更新时间', dataIndex: 'update', slotName: 'update',
    },
    {
      title: '操作', slotName: 'optional', fixed: 'right',
      width: 220,
    }
  ];

  const renderList = ref<TableData[]>();
  // const fetchData = async () => {
  //   try {
  //     const { data } = await apiProductList();
  //     renderList.value = data;
  //   } catch (err) {
  //     console.log(err);
  //   }
  // };

  // fetchData();

  // 添加/编辑使用表单对象
  const productForm=reactive({
    id: undefined,
    title: undefined,
    keyCode: undefined,
    desc: undefined,
    operator: 'Mega Qi'
  })

  const productTotal = ref<number>();
  const productSearch = reactive({
    title: undefined,
    keyCode: undefined,
    pageSize: 5,
    currentPage: 1
  })
  const pageChange = (current: number) => {
    console.log(current)
    productSearch.currentPage=current
    btnSearchClick()
  }
  const pageSizeChange = (pageSize: number) => {
    console.log(pageSize)
    productSearch.pageSize=pageSize
    btnSearchClick()
  }
  const btnSearchClick = async () => {
    // const res = await apiProductSearch(productSearch);
    const res = await apiProductSearchPage(productSearch);
    if (res.code === 20000) {
      renderList.value = res.data
      productTotal.value = res.total
    } else {
      console.log("产品搜索失败");
    }
  };
  btnSearchClick();

  /* 产品添加对话框start */
  const addModalVisible = ref(false); // 新增控制显示和隐藏布尔值，默认为flase
  const addButtonClick = () => {  // 新增产品线按钮触发事件
    addModalVisible.value = true; // 新增赋值为True显示
  };
  const addModalOk = async () => { // 添加对话框确定按钮，提交数据操作
    const res = await apiProductAdd(productForm);
    if (res.code === 20000) {
      addModalVisible.value = false; // 新增对话框
      btnSearchClick(); // 添加成功重新请求列表
    } else {
      console.log("产品添加失败");
    }
  };
  const addModalCancel = () => { // 对话框取消按钮，赋值使其关闭对话框
    addModalVisible.value = false;
  }
  /* 产品添加对话框end */

  /* 产品编辑部分start */
  const editModalVisible = ref(false); // 控制显示和隐藏编辑对话框布尔值，默认为flase
  const editButtonClick = (record) => {  // 修改产品线按钮触发事件
    productForm.id = record.id;
    productForm.title = record.title;
    productForm.keyCode = record.keyCode;
    productForm.desc = record.desc;
    editModalVisible.value = true; // 编辑显隐赋值为True显示
  };
  const editModalOk = async () => { // 编辑对话框确定按钮，提交数据操作
    const res = await apiProductUpdate(productForm);
    if (res.code === 20000) {
      editModalVisible.value = false; // 新增对话框
      btnSearchClick(); // 添加成功重新请求列表
    } else {
      console.log("产品修改失败");
    }
  };
  const editModalCancel = () => { // 编辑对话框取消按钮，赋值使其关闭对话框
    editModalVisible.value = false;
  }
  /* 产品编辑部分end */

  /* 产品删除部分 */
  const removeButtonClick = async (id) => {
    const res = await apiProductRemove(id);
    if (res.code === 20000) {
      btnSearchClick(); // 删除成功重新请求列表
    } else {
      console.log("产品删除失败");
    }
  }
  // 控制删除确认对话框
  const delModalVisible = ref(false);
  const delId = ref("");
  const modalOkPros = {
    status: 'warning'
  };
  const delBtnClick = (id) => {
    delId.value = id;
    delModalVisible.value = true;
  };
  const delModalOk = async () => {
    const res = await apiProductRemove(delId.value);
    if (res.code === 20000) {
      delModalVisible.value = false;
      btnSearchClick();
    } else {
      console.log("产品移除失败");
    };
  };

</script>

<script lang="ts">
  export default {
    name: 'Product',
  };
</script>

<style scoped>
</style>
