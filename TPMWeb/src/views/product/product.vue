<template>
  <!--app-container 框架内嵌的一个样式，可以尝试去掉看看效果有什么不同-->
  <div class="app-container">
    <!--样式组件 参考 https://element.eleme.cn/#/zh-CN/component/table-->
    <el-table :data="tableData"><!--:data 绑定data()的数组值,会动态根据其变化而变化-->
      <el-table-column prop="id" label="编号"/>
      <!--:data prop绑定{}中的key，label为自定义显示的列表头-->
      <el-table-column prop="title" label="名称"/>
      <el-table-column prop="keyCode" label="代号"/>
      <!--<el-table-column prop="desc" label="描述"/>-->
      <el-table-column prop="operator" label="操作人"/>
      <el-table-column prop="update" label="操作时间"/>
    </el-table>
  </div>
</template>

<script>
// 倒入src/api/proudct 配置的请求列表方法
import { apiProductList } from '@/api/product'

export default {
  name: 'Product', // 页面名称
  // data() 数据\属性，固定return中配置
  data() {
    return {
      tableData: []
    }
  },
  // 页面生命周期中的创建阶段调用
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.getProductList()
  },
  methods: {
    // getProductList自定义方法名，提供其他地方调用this.getProductList
    getProductList() {
      // 固定格式调用api配置方法，并将返回结果回调给response
      apiProductList().then(response => {
        // console.log（）是调试打印，可以在chrome开发者工具中查看
        console.log(response.data)
        // 将返回的结果赋值给变量 tableData
        this.tableData = response.data
      })
    }
  }
}
</script>

<style scoped>

</style>
