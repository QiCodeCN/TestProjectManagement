<template>
  <div class="dashboard-container">
    <div ref="LineChartBoard" style="width: 95%;height:500px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { requestStacked } from '@/api/board'

export default {
  name: 'Dashboard',
  mounted() {
    this.getApList()
  },
  methods: {
    getApList() {
      requestStacked().then(resp => {
        this.initStackedChart(resp.data)
      })
    },
    initStackedChart(data) {
      const chartDom = this.$refs['LineChartBoard']
      const myChart = echarts.init(chartDom)
      const series = []
      // 唯一处理需要额外逻辑处理的地方，根据接口数据动态生成series数据
      for (var key in data.series) {
        series.push(
          {
            name: key,
            type: 'line',
            stack: 'Total',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: data.series[key]
          }
        )
      }
      var option = {
        title: {
          text: '周需求提测趋势'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: data.note
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: data.weeks
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: series
      }
      option && myChart.setOption(option)
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
