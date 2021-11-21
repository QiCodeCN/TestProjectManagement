<template>
  <!--app-container 框架内嵌的一个样式，可以尝试去掉看看效果有什么不同-->
  <div class="app-container">
    <div class="filter-container">
      <el-form :inline="true" :model="search">
        <el-form-item label="名称">
          <el-input v-model="search.title" placeholder="支持模糊查询" style="width: 200px;" clearable/>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="search.keyCode" placeholder="支持模糊查询" style="width: 200px;" clearable/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" plain @click="searchProduct()" icon="el-icon-search"></el-button>

        </el-form-item>
      </el-form>
      <el-button type="primary" icon="el-icon-plus" style="float:right" @click="dialogProduct()">新增</el-button>
    </div>
    <!--对话框嵌套表，使用el-dialog-->
    <!--<el-dialog v-bind:title="dialogProductStatus==='ADD'?'添加产品或项目':'修改产品或项目'" :visible.sync="dialogProductShow">-->
    <el-dialog :title="dialogProductStatus==='ADD'?'添加产品或项目':'修改产品或项目'" :visible.sync="dialogProductShow">
      <el-form :model="product">
        <el-form-item v-if="dialogProductStatus==='UPDATE'" label="编号" label-width="100px">
          <el-input v-model="product.id" style="width: 80%" disabled></el-input>
        </el-form-item>
        <el-form-item label="名称" label-width="100px">
          <el-input v-model="product.title" placeholder="请填写中文名称" style="width: 80%"></el-input>
        </el-form-item>
        <el-form-item  label="唯一码" label-width="100px">
          <el-input v-model="product.keyCode" placeholder="产品/项目唯一码" style="width: 80%"></el-input>
        </el-form-item>
        <el-form-item  label="备注" label-width="100px">
          <el-input v-model="product.desc" type="textarea" placeholder="备注说明" style="width: 80%"></el-input>
        </el-form-item>
      </el-form>
      <!--复用根据对话框，根据条件v-if 判断显示和隐藏-->
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogProductShow = false">取 消</el-button>
        <el-button v-if="dialogProductStatus === 'ADD'" type="primary" @click="pCreate()">添 加</el-button>
        <el-button v-if="dialogProductStatus === 'UPDATE'" type="primary" @click="pUpdate()">修 改</el-button>
      </span>
    </el-dialog>
    <!--样式组件 参考 https://element.eleme.cn/#/zh-CN/component/table-->
    <el-table :data="tableData"><!--:data 绑定data()的数组值,会动态根据其变化而变化-->
      <el-table-column prop="id" label="编号"/>
      <!--:data prop绑定{}中的key，label为自定义显示的列表头-->
      <el-table-column prop="title" label="名称"/>
      <el-table-column prop="keyCode" label="代号"/>
      <el-table-column prop="desc" label="描述" show-overflow-tooltip/>
      <el-table-column prop="operator" label="操作人"/>
      <el-table-column :formatter="formatDate" prop="update" label="操作时间"/>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-link icon="el-icon-edit" @click="dialogProductUpdate(scope.row)">编辑</el-link>
          <el-link icon="el-icon-circle-close" @click="pSoftRemove(scope.row.id)">停用</el-link>
          <el-link icon="el-icon-delete" @click="pHardRemove(scope.row.id)">删除</el-link>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
// 导入src/api/proudct 配置的请求列表方法
import { apiProductList, apiProductCreate, apiProductUpdate, apiProductDelete, apiProductRemove, apiProductSearch } from '@/api/product'
// 导入全局存储
import store from '@/store'
import moment from 'moment'

export default {
  name: 'Product', // 页面名称
  // data() 数据\属性，固定return中配置
  data() {
    return {
      // 获得登录的名字
      op_user: store.getters.name,
      // 搜索条件
      search: {
        title: undefined,
        keyCode: undefined
      },
      // 定义产品参数
      product: {
        id: undefined,
        title: undefined,
        keyCode: undefined,
        desc: undefined,
        operator: this.op_user
      },
      // 控制嵌套表单显示和隐藏
      dialogProductShow: false,
      dialogProductStatus: 'ADD',
      // 查询的数据
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
    },
    // 条件搜索功能
    searchProduct() {
      apiProductSearch(this.search).then(res => {
        this.tableData = res.data
      })
    },
    formatDate(row, column) {
      const date = row[column.property]
      if (date === undefined) {
        return ''
      }
      // 使用moment格式化时间，由于我的数据库是默认时区，偏移量设置0，各自根据情况进行配置
      return moment(date).utcOffset(0).format('YYYY-MM-DD HH:mm')
    },
    dialogProduct() {
      // 添加先初始化空状态
      this.product.id = undefined
      this.product.keyCode = ''
      this.product.title = ''
      this.product.desc = ''
      this.product.operator = this.op_user

      // 标记弹窗是添加操作
      this.dialogProductStatus = 'ADD'
      // 弹出对话框设置为true
      this.dialogProductShow = true
    },
    pCreate() {
      // 请求API进行添加
      apiProductCreate(this.product).then(response => {
        // 如果request.js没有拦截即表示成功，给出对应提示和操作
        this.$notify({
          title: '成功',
          message: '项目或产品添加成功',
          type: 'success'
        })
        // 关闭对话框
        this.dialogProductShow = false
        // 重新查询刷新数据显示
        this.getProductList()
      })
    },
    // 获取当前编辑行数数据并赋值给product
    dialogProductUpdate(row) {
      // 添加先初始化空状态
      this.product.id = row.id
      this.product.keyCode = row.keyCode
      this.product.title = row.title
      this.product.desc = row.desc
      this.product.operator = this.op_user

      // 标记弹窗是修改操作
      this.dialogProductStatus = 'UPDATE'
      // 弹出对话框设置为true
      this.dialogProductShow = true
    },
    pUpdate() {
      apiProductUpdate(this.product).then(res => {
        this.$notify({
          title: '成功',
          message: '项目或产品修改成功',
          type: 'success'
        })
        // 关闭对话框
        this.dialogProductShow = false
        // 重新查询刷新数据显示
        this.getProductList()
      })
    },
    pHardRemove(id) {
      this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        apiProductDelete(id).then(res => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          // 重新查询刷新数据显示
          this.getProductList()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    pSoftRemove(id) {
      this.$confirm('此操作将停用不显示, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        apiProductRemove(id).then(res => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          // 重新查询刷新数据显示
          this.getProductList()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>

<style scoped>

</style>
