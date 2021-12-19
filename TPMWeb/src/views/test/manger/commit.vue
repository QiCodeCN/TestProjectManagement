<template>
  <div class="app-container">
    <el-header>
      <el-page-header @back="goBack" :content="testAction==='UPDATE'?'修改提测':'新建提测'"/>
    </el-header>
    <el-main>
      <el-form :model="requestForm" :rules="requestRules" ref="ruleForm" label-width="100px" >
        <el-form-item v-if="testAction==='UPDATE'" label="提测ID" prop="id">
          <el-input v-model="requestForm.id" style="width: 350px" disabled=""></el-input>
        </el-form-item>
        <el-form-item label="提测标题" prop="title">
          <el-input v-model="requestForm.title" placeholder="提测标题" style="width: 350px"></el-input>
        </el-form-item>
        <el-form-item label="服务应用" prop="appId">
          <el-select
             v-model="requestForm.appId"
             filterable
             remote
             reserve-keyword
             placeholder="请输入关键词（远程搜索)"
             :remote-method="remoteMethod"
             :loading="appIdloading"
             @change="appSelected"
             style="width: 300px">
            <el-option
              v-for="item in appIdList"
              :key="item.id"
              :label="item.appId"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="提测RD" prop="developer">
          <el-input v-model="requestForm.developer" placeholder="提测人研发" style="width: 350px"></el-input>
        </el-form-item>
        <el-form-item label="测试QA" prop="tester">
          <el-input v-model="requestForm.tester" placeholder="测试人" style="width: 350px"></el-input>
        </el-form-item>
        <el-form-item label="关系人" prop="CcMail">
          <el-input v-model="requestForm.CcMail" placeholder="邮件抄送人" style="width: 350px"></el-input>
        </el-form-item>
        <el-form-item label="提测版本" prop="version">
          <el-input v-model="requestForm.version" placeholder="部署版本号/分支/Tag" style="width: 350px"></el-input>
        </el-form-item>
        <el-form-item label="提测类型" prop="type">
          <el-select v-model="requestForm.type" clearable placeholder="请选择..." style="width: 300px">
            <el-option
              v-for="item in opsType"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="测试范围" prop="scope">
          <el-input v-model="requestForm.scope" type="textarea" :rows="3" placeholder="1.功能点 \n 2.测试点 \n 3.回归点" style="width: 350px"></el-input>
        </el-form-item>
        <el-form-item label="代码地址" prop="gitCode">
          <el-input v-model="requestForm.gitCode" placeholder="git代码地址" style="width: 350px"></el-input>
        </el-form-item>
        <el-form-item label="产品文档" prop="wiki">
          <el-input v-model="requestForm.wiki" placeholder="文档说明地址" style="width: 350px"></el-input>
        </el-form-item>
        <el-form-item label="更多信息" prop="more">
          <el-input v-model="requestForm.more" type="textarea" :rows="3" placeholder="其他补充信息" style="width: 350px"></el-input>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="requestForm.isEmail" true-label="true">发送邮件</el-checkbox>
        </el-form-item>
        <el-form-item>
          <!--<el-button type="primary" @click="onSubmit">{{testAction=='ADD'?'立即添加':'修改提测'}}</el-button>-->
          <el-button v-if="testAction==='ADD'" type="primary" @click="onSubmit">立即创建</el-button>
          <el-button v-if="testAction==='UPDATE'" type="primary" @click="onSubmit">修改提测</el-button>
          <el-button @click="onCancel">取   消</el-button>
        </el-form-item>
      </el-form>
    </el-main>
  </div>
</template>

<script>
import { apiAppsIds } from '@/api/apps'
import { reqCreate, apiTestInfo, reqUpdate } from '@/api/test'
import store from '@/store'

export default {
  name: 'Commit',
  data() {
    return {
      op_user: store.getters.name,
      testAction: '',
      testId: '',
      appIdloading: false,
      requestForm: {
        id: undefined,
        title: '',
        appId: '',
        appName: '',
        developer: '',
        tester: '',
        CcMail: '',
        version: '',
        type: '',
        scope: '',
        gitCode: '',
        wiki: '',
        more: '',
        isEmail: 'true',
        createUser: '',
        updateUser: ''
      },
      requestRules: {
        title: [
          { required: true, message: '请输入活动名称', trigger: 'blur' },
          { min: 3, message: '长度在大于3个字符', trigger: 'blur' }
        ],
        appId: [
          { required: true, message: '请选择对应的服务应用', trigger: 'change' }
        ],
        developer: [
          { required: true, message: '请填写提测人RD', trigger: 'change' }
        ],
        tester: [
          { required: true, message: '请填写对应的测试人Tester', trigger: 'change' }
        ]

      },
      opsType: [
        { label: '功能测试', value: 1 },
        { label: '性能测试', value: 2 },
        { label: '安全测试', value: 3 }
      ],
      appIdList: []
    }
  },
  mounted() {
    if (this.$route.params.action) {
      this.testAction = this.$route.params.action
    } else if (this.$route.query.action) {
      this.testAction = this.$route.query.action
    }
    if (this.$route.query.id) {
      this.testId = this.$route.query.id
      this.getTestInfo()
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1)
    },
    remoteMethod(query) {
      if (query !== '') {
        this.appIdloading = true
        setTimeout(() => {
          apiAppsIds(query).then(resp => {
            this.appIdList = resp.data
          })
          this.appIdloading = false
        }, 200)
      } else {
        this.appIdList = []
      }
    },
    appSelected() {
      // 判断获取选择应用的其他信息
      for (var it in this.appIdList) {
        if (this.appIdList[it].id === this.requestForm.appId) {
          // 以下判断为在字符为空的情况下添加，即认为没有人工再输入，快捷反填已知道信息
          if (!this.requestForm.developer) {
            this.requestForm.developer = this.appIdList[it].developer
          }
          if (!this.requestForm.tester) {
            this.requestForm.tester = this.appIdList[it].tester
          }
          if (!this.requestForm.CcMail) {
            this.requestForm.CcMail = this.appIdList[it].CcEmail
          }
          if (!this.requestForm.wiki) {
            this.requestForm.wiki = this.appIdList[it].wiki
          }
          if (!this.requestForm.gitCode) {
            this.requestForm.gitCode = this.appIdList[it].gitCode
          }
          // 填写apreqCreatepName信息，用于邮件发送不再额外查询
          this.requestForm.appName = this.appIdList[it].appName
        }
      }
    },
    onSubmit() {
      this.$refs['ruleForm'].validate((valid) => {
        if (valid) {
          if (this.testAction === 'ADD') {
            this.requestForm.id = undefined
            this.requestForm.createUser = this.op_user
            this.requestForm.updateUser = this.op_user
            reqCreate(this.requestForm).then(response => {
              // 如果request.js没有拦截即表示成功，给出对应提示和操作
              this.$notify({
                title: '成功',
                message: '提测添加成功',
                type: 'success'
              })
              // 回到列表页面
              this.$router.push({ name: 'test', params: { needUp: 'true' }})
            })
          } else {
            this.requestForm.updateUser = this.op_user
            reqUpdate(this.requestForm).then(response => {
              this.$notify({
                title: '成功',
                message: '提测修改成功',
                type: 'success'
              })
              // 回到列表页面
              this.$router.push({ name: 'test', params: { needUp: 'true' }})
            })
          }
        } else {
          return false
        }
      })
    },
    onCancel() {
      this.$router.push({ name: 'test' })
    },
    getTestInfo() {
      apiTestInfo(this.testId).then(response => {
        const data = response.data
        this.requestForm.id = data.id
        this.requestForm.title = data.title
        this.requestForm.developer = data.developer
        this.requestForm.tester = data.tester
        this.requestForm.CcMail = data.CcMail
        this.requestForm.version = data.version
        this.requestForm.type = data.type
        this.requestForm.scope = data.scope
        this.requestForm.gitCode = data.gitCode
        this.requestForm.wiki = data.wiki
        this.requestForm.more = data.more
        this.requestForm.appName = data.appName
        this.requestForm.isEmail = false
        this.remoteMethod(data.appName)
        setTimeout(() => {
          this.requestForm.appId = data.appId
        }, 300)
      })
    }
  }
}
</script>

<style scoped>

</style>
