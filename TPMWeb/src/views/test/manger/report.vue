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
        <el-form-item label="提测类型" prop="status" :rules="{ required: true, message: '必须选择一个结果', trigger: 'blur' }">
          <el-select v-model="reportForm.status" clearable placeholder="请选择..." style="width: 300px">
            <el-option
              v-for="item in opsStauts"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="结论描述" prop="test_desc">
          <el-input v-model="reportForm.test_desc" type="textarea" :rows="3" placeholder="测试结论总结" style="width: 350px" />
        </el-form-item>
        <el-form-item label="风险提示" prop="test_risks">
          <el-input v-model="reportForm.test_risks" type="textarea" :rows="3" placeholder="风险提示详细说明" style="width: 350px" />
        </el-form-item>
        <el-form-item label="测试CASE" prop="test_desc">
          <el-input v-model="reportForm.test_desc" type="textarea" :rows="5" placeholder="测试点 或 详细的测试CASE链接或者附件" style="width: 350px" />
        </el-form-item>
        <el-form-item label="缺陷列表" prop="test_bugs">
          <el-input v-model="reportForm.test_desc" type="textarea" :rows="2" placeholder="提交的BUG列表或者管理工具相关搜索过滤地址" style="width: 350px" />
        </el-form-item>
        <el-form-item label="附件" prop="test_file">
          <el-upload
            :limit="1"
            :file-list="fileList"
            :auto-upload="true"
            action="http://127.0.0.1:5000/api/report/upload"
            :on-success="uploadFile"
          >
            <el-button size="small" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="备注" prop="test_desc">
          <el-input v-model="reportForm.test_note" type="textarea" :rows="3" placeholder="其他一些说明" style="width: 350px" />
        </el-form-item>
      </el-form>
    </el-main>
  </div>
</template>

<script>
export default {
  name: 'Reporot',
  data() {
    return {
      reportAction: '',
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
        test_note: ''
      },
      fileList: []
    }
  },
  mounted() {
    if (this.$route.query.action) {
      this.reportAction = this.$route.query.action
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
    uploadFile(response, file, fileList) {
      if (response.code === 40000) {
        this.$message({
          message: '格式不正确或者上传异常',
          type: 'warning'
        })
      } else {
        this.$message({
          message: '上传成功',
          type: 'success'
        })
        this.reportForm.test_file = file.name
      }
    }
  }
}
</script>

<style scoped>

</style>
