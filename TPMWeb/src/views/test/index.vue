<template>
  <div class="app-container">
    <div class="filter-container">
      <el-form :inline="true" :model="search">
        <el-form-item label="归属分类">
          <el-select v-model="search.productId">
            <el-option value="" label="所有" />
            <el-option
              v-for="item in optsProduct"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="应用ID">
          <el-input v-model="search.appId" placeholder="服务ID关键词" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="测试人">
          <el-input v-model="search.tester" placeholder="默认测试" style="width: 210px;" clearable />
        </el-form-item>
        <el-form-item label="提测人">
          <el-input v-model="search.developer" placeholder="默认测试" style="width: 210px;" clearable />
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="search.pickTime"
            type="datetimerange"
            :picker-options="pickerOptions"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            align="right"
          />
        </el-form-item>
        <el-form-item label="测试状态">
          <el-select v-model="search.status" placeholder="请选择">
            <el-option value="" label="所有" />
            <el-option key="1" label="已提测" value="1" />
            <el-option key="2" label="测试中" value="2" />
            <el-option key="3" label="通过" value="3" />
            <el-option key="4" label="失败" value="4" />
            <el-option key="9" label="废弃" value="9" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" plain @click="searchClick()">查询</el-button>
        </el-form-item>
      </el-form>
      <el-button type="primary" icon="el-icon-plus" style="float:right" @click="doCommit()">新建提测</el-button>
    </div>
    <div>
      <el-table :data="testData">
        <!--:data prop绑定{}中的key，label为自定义显示的列表头-->
        <el-table-column prop="appId" label="应用ID" />
        <el-table-column prop="title" label="提测标题" show-overflow-tooltip />
        <el-table-column :formatter="formatStatus" prop="status" label="测试状态" />
        <el-table-column :formatter="formatType" prop="type" label="类型" />
        <el-table-column prop="developer" label="提测人" />
        <el-table-column prop="tester" label="测试人" />
        <el-table-column prop="updateUser" label="更新人" />
        <el-table-column :formatter="formatDate" prop="updateDate" label="更新时间" />
        <el-table-column label="操作" width="300">
          <template slot-scope="scope">
            <!--<label>菜单逻辑判断一列</label>-->
            <el-link v-if="scope.row.status===1" type="primary" @click="startTest(scope.row)">开始测试</el-link>
            <el-link v-if="scope.row.status===2" type="primary">添加结果</el-link>
            <el-link v-if="scope.row.status===3 || scope.row.status == 4" type="primary">查看报告</el-link>
            <el-link v-if="scope.row.status===9" type="primary">删除结果</el-link>
            <!--<label>菜单逻辑判断二列</label>-->
            <el-divider direction="vertical" />
            <el-link v-if="[1,2].includes(scope.row.status)" type="primary" @click="doUpdate(scope.row)">编辑提测</el-link>
            <el-link v-if="[3,4,9].includes(scope.row.status)" type="primary">编辑结果</el-link>
            <el-divider direction="vertical" />
            <el-link type="primary">提测详情</el-link>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <br>
      <el-pagination
        background
        :current-page.sync="pageValues.currentPage"
        :page-size="pageValues.pageSize"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[5, 10, 20, 30, 50]"
        :total="pageValues.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { apiAppsProduct } from '@/api/apps'
import { apiTestSearch } from '@/api/test.js'
import moment from 'moment'

export default {
  name: 'Test',
  data() {
    return {
      // 条件查询变量定义
      search: {
        productId: '',
        appId: '',
        developer: '',
        tester: '',
        status: '',
        pickTime: ''
      },
      // 范围日期组件的快捷选项配置
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date()
            const start = new Date() // 当前时间
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7) // 单位毫秒加减计算
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }]
      },
      optsProduct: [],
      testData: [],
      pageValues: {
        pageSize: 10,
        currentPage: 1,
        total: 0
      }
    }
  },
  mounted() {
    if (this.$route.params.needUp && this.$route.params.needUp.needUp === 'true') {
      this.searchClick()
    }
  },
  created() {
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
    formatStatus(row, column) {
      const status = row[column.property]
      switch (status) {
        case 1:
          return '已提测'
        case 2:
          return '测试中'
        case 3:
          return '通过'
        case 4:
          return '失败'
        case 9:
          return '已废弃'
        default:
          return '未知状态'
      }
    },
    formatType(row, column) {
      const type = row[column.property]
      switch (type) {
        case 1:
          return '功能测试'
        case 2:
          return '性能测试'
        case 3:
          return '安全测试'
        default:
          return '未知状态'
      }
    },
    productList() {
      apiAppsProduct().then(resp => {
        this.optsProduct = resp.data
      })
    },
    searchClick() {
      const body = {
        pageSize: this.pageValues.pageSize,
        currentPage: this.pageValues.currentPage,
        productId: this.search.productId,
        appId: this.search.appId,
        tester: this.search.tester,
        developer: this.search.developer,
        pickTime: this.search.pickTime,
        status: this.search.status
      }
      apiTestSearch(body).then(response => {
        // 将返回的结果赋值给表格自动匹配
        this.testData = response.data
        this.pageValues.total = response.total
      })
    },
    handleSizeChange(val) {
      this.pageValues.pageSize = val
      this.searchClick()
    },
    handleCurrentChange(val) {
      this.pageValues.currentPage = val
      this.searchClick()
    },
    doCommit() {
      this.$router.push({ name: 'commit', params: { action: 'ADD' }})
    },
    doUpdate(row) {
      this.$router.push({ path: '/commit?action=UPDATE&id=' + row.id })
    },
    startTest() {
      console.log('开始测试')
    }
  }
}
</script>

<style scoped>
  .el-pagination {
    text-align: right;
  }
</style>
