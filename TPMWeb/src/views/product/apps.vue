<template>
  <div class="app-container">
    <div class="filter-container">
      <el-form :inline="true" :model="search">
        <el-form-item label="归属分类">
          <el-select v-model="search.productId" filterable="true" clearable>
            <el-option value="" label="所有"></el-option>
            <el-option
              v-for="item in options"
              :key="item.id"
              :label="item.title"
              :value="item.id">
              <span style="float: left">{{ item.keyCode }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.title }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="应用ID">
          <el-input v-model="search.appId" placeholder="服务ID关键词" style="width: 200px;" clearable/>
        </el-form-item>
        <el-form-item label="描 述">
          <el-input v-model="search.note" placeholder="描述模糊搜索" style="width: 200px;" clearable/>
        </el-form-item>
        <br>
        <el-form-item label="研  发">
          <el-input v-model="search.developer" placeholder="默认研发" style="width: 210px;" clearable/>
        </el-form-item>
        <el-form-item label="产  品">
          <el-input v-model="search.producer" placeholder="默认产品" style="width: 210px;" clearable/>
        </el-form-item>
        <el-form-item label="测  试">
          <el-input v-model="search.tester" placeholder="默认测试" style="width: 210px;" clearable/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" plain @click="searchClick()">搜索</el-button>
        </el-form-item>
      </el-form>
      <el-button type="primary" icon="el-icon-plus" style="float:right" @click="addApp()">添加应用</el-button>
    </div>
    <!--:data 绑定data()的数组值,会动态根据其变化而变化-->
    <el-table :data="tableData">
      <!--:data prop绑定{}中的key，label为自定义显示的列表头-->
      <el-table-column prop="appId" label="应用ID"/>
      <el-table-column prop="note" label="描述" show-overflow-tooltip/>
      <el-table-column prop="title" label="归属分类"/>
      <el-table-column prop="developer" label="默认研发" />
      <el-table-column prop="producer" label="默认产品"/>
      <el-table-column prop="tester" label="默认测试"/>
      <el-table-column prop="updateUser" label="更新人"/>
      <el-table-column :formatter="formatDate" prop="updateDate" label="更新时间"/>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-link icon="el-icon-edit" @click="updateApp(scope.row)">修改</el-link>
        </template>
      </el-table-column>
    </el-table>
    <br>
    <div>
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page.sync="search.currentPage"
        :page-size="search.pageSize"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[5, 10, 20, 30, 50]"
        :total=total>
      </el-pagination>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import { apiAppsProduct, apiAppsSearch } from '@/api/apps'

export default {
  name: 'Apps',
  data() {
    return {
      search: {
        productId: '',
        appId: '',
        note: '',
        developer: '',
        producer: '',
        tester: '',
        pageSize: 10,
        currentPage: 1
      },
      options: [],
      total: 0,
      tableData: []
    }
  },
  // 页面生命周期中的创建阶段调用
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.productList()
    this.searchClick()
  },
  methods: {
    formatDate(row, column) {
      const date = row[column.property]
      if (date === undefined) {
        return ''
      }
      // 使用moment格式化时间，由于我的数据库是默认时区，偏移量设置0，各自根据情况进行配置
      return moment(date).utcOffset(0).format('YYYY-MM-DD HH:mm')
    },
    productList() {
      apiAppsProduct().then(resp => {
        this.options = resp.data
      })
    },
    searchClick() {
      apiAppsSearch(this.search).then(response => {
        // 将返回的结果赋值给表格自动匹配
        this.tableData = response.data
        this.total = response.total
      })
    },
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`)
      this.search.pageSize = val
      this.searchClick()
    },
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.search.currentPage = val
      this.searchClick()
    },
    addApp() {
      this.$message({
        message: '我是待实现的CASE',
        type: 'warning'
      })
    },
    updateApp() {
      this.$message({
        message: '我是待实现的CASE',
        type: 'warning'
      })
    }
  }
}
</script>

<style scoped>
  .el-pagination {
    text-align: right;
  }
</style>
