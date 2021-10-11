<template>
  <div class="app-container">
    <el-page-header @back="goBack" content="提测">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="活动名称" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
      </el-form>
    </el-page-header>
  </div>
</template>

<script>
export default {
  name: 'Commit',
  data() {
    return {
      ruleForm: {
        name: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入活动名称', trigger: 'blur' },
          { min: 3, message: '长度在大于3个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    goBack() {
      this.$router.push('test')
    }
  }
}
</script>

<style scoped>

</style>
