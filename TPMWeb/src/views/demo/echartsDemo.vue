<template>
  <div class="app-container">
<!--    <div id="pieChartDemo"  style="width: 600px;height:400px;"></div>-->
    <div ref="pieChartDemo" style="width: 600px;height:400px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'EchartsDemo',
  mounted() {
    this.initPieChart()
  },
  methods: {
    initPieChart() {
      // var chartDom = document.getElementById('pieChartDemo')
      var chartDom = this.$refs['pieChartDemo']
      var myChart = echarts.init(chartDom)
      var option = {
        title: {
          text: '大奇测试开发',
          subtext: '文章类型分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: [
              { value: 20, name: '提测平台' },
              { value: 2, name: '性能测试' },
              { value: 1, name: '流量回放' },
              { value: 3, name: '好文分享' },
              { value: 5, name: '杂谈' }
            ]
          }
        ]
      }
      option && myChart.setOption(option)
    }
  }
}
</script>

<style scoped>

</style>
