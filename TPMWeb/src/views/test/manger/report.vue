<template>
  <div class="app-container">
    <el-header>
      <el-page-header :content="reportAction==='UPDATE'?'修改结果':'报告结果'" @back="goBack" />
    </el-header>
    <el-main>
      <el-form ref="ruleForm" :model="reportForm" label-width="100px">
        <el-form-item v-if="reportAction==='UPDATE'" label="编号" prop="id">
          <el-input v-model="reportForm.id" style="width: 350px" disabled="" />
        </el-form-item>
        <el-form-item label="测试结果" prop="status" :rules="{ required: true, message: '必须选择一个结果', trigger: 'blur' }">
          <el-select v-model="reportForm.status" clearable placeholder="请选择..." style="width: 300px">
            <el-option
              v-for="item in opsStauts"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="结论描述" prop="test_desc" :rules="{ required: true, message: '结论不能空', trigger: 'blur' }">
          <el-input v-model="reportForm.test_desc" type="textarea" :rows="3" placeholder="测试结论总结" style="width: 350px" />
        </el-form-item>
        <el-form-item label="风险提示" prop="test_risks">
          <el-input v-model="reportForm.test_risks" type="textarea" :rows="3" placeholder="风险提示详细说明" style="width: 350px" />
        </el-form-item>
        <el-form-item label="测试CASE" prop="test_cases">
          <el-input v-model="reportForm.test_cases" type="textarea" :rows="5" placeholder="测试点 或 详细的测试CASE链接或者附件" style="width: 350px" />
        </el-form-item>
        <el-form-item label="缺陷列表" prop="test_bugs">
          <el-input v-model="reportForm.test_bugs" type="textarea" :rows="2" placeholder="提交的BUG列表或者管理工具相关搜索过滤地址" style="width: 350px" />
        </el-form-item>
        <el-form-item label="附件" prop="test_file">
          <el-upload
            ref="uploadItem"
            :limit="1"
            :file-list="fileList"
            action="http://127.0.0.1:5000/api/report/upload"
            :http-request="uploadeFile"
            :on-success="uploadSuccess"
            :show-file-list="false"
          >
            <el-button size="small" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">{{tips}}</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="备注" prop="test_desc">
          <el-input v-model="reportForm.test_note" type="textarea" :rows="3" placeholder="其他一些说明" style="width: 350px" />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="reportForm.isEmail" true-label="true">发送邮件</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button v-if="reportAction==='ADD'" type="primary" @click="onSubmit">添加报告</el-button>
          <el-button v-if="reportAction==='UPDATE'" type="primary" @click="onSubmit">修改报告</el-button>
          <el-button @click="onCancel">取   消</el-button>
        </el-form-item>
      </el-form>
    </el-main>
  </div>
</template>

<script>
import { reportSave, reportTestInfo } from '@/api/test'
import axios from 'axios'
import store from '@/store'

export default {
  name: 'Reporot',
  data() {
    return {
      op_user: store.getters.name,
      reportAction: 'ADD',
      testId: '',
      // 测试状态 3-通过 4-失败 9-废弃
      opsStauts: [
        { label: '测试通过', value: 3 },
        { label: '验证失败', value: 4 },
        { label: '废弃测试', value: 9 }
      ],
      // 测试结果提交所需要的字段
      reportForm: {
        id: undefined,
        status: '',
        test_desc: '',
        test_risks: '',
        test_cases: '',
        test_bugs: '',
        test_file: '',
        test_note: '',
        isEmail: 'true'
      },
      fileList: [],
      tips: '只能上传jpg/png/zip/pdf文件，且不超过10M'
    }
  },
  mounted() {
    // console.log(this.$route.params)
    this.reportAction = this.$route.params.action
    if (this.$route.params.action === 'ADD') {
      this.reportForm.id = this.$route.params.id
    } else {
      this.reportForm.id = this.$route.params.id
      this.getReportInfo()
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1)
    },
    getReportInfo() {
      reportTestInfo(this.reportForm.id).then(response => {
        this.reportForm = response.data
      })
    },
    uploadSuccess(response, file, fileList) {
      if (response.code === 40000) {
        this.$message({
          message: '格式不正确或者上传异常',
          type: 'warning'
        })
        this.fileList = []
      } else {
        this.$message({
          message: '上传成功',
          type: 'success'
        })
      }
      this.$refs.upload.clearFiles()
      this.tips = file.name
    },
    uploadeFile(params) {
      const fd = new FormData()
      fd.append('file', params.file)
      fd.append('FileName', params.file.name)
      fd.append('async', true)
      const config = {
        headers: { 'Content-Type': 'multipart/form-data' }
      }
      axios
        .post(params.action, fd, config)
        .then(res => {
          this.$refs.uploadItem.clearFiles()
          this.tips = params.file.name
          this.reportForm.test_file = params.file.name
        })
        .catch(Error => {
          console.log(Error)
          this.fileList = []
          this.$message({
            message: '大小不符合要求或服务器异常',
            type: 'warning'
          })
        })
    },
    onSubmit() {
      this.$refs['ruleForm'].validate((valid) => {
        if (valid) {
          this.reportForm.createUser = this.op_user
          this.reportForm.updateUser = this.op_user
          reportSave(this.reportForm).then(response => {
            // 如果request.js没有拦截即表示成功，给出对应提示和操作
            this.$notify({
              title: '成功',
              message: '报告添加成功！',
              type: 'success'
            })
            // 回到列表页面
            this.$router.push({ name: 'test', params: { needUp: 'true' }})
          })
        } else {
          return false
        }
      })
    },
    onCancel() {
      this.$router.push({ name: 'test' })
    }
  }
}
</script>

<style scoped>

</style>
