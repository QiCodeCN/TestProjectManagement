<template>
  <div class="dashboard-container">
    <div class="filter-container">
      <el-form :inline="true" :model="searchValue">
        <el-form-item label="日期选择">
          <el-date-picker
            v-model="searchValue.date"
            type="daterange"
            value-format="yyyy-MM-dd HH:mm:ss"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchBoard">刷新查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-switch
            v-model="stackedColumnMode"
            @change="changeBoardMode"
            active-text="分组模式"
            inactive-text="累积模式">
          </el-switch>
        </el-form-item>
      </el-form>
    </div>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>周需求分组量</span>
      </div>
      <div id="ColumnBoard" style="width: 95%;height:360px;" />
    </el-card>
    <br>
    <el-card class="box-card">
      <div ref="LineChartBoard" style="width: 95%;height:500px;" />
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { Column } from '@antv/g2plot'

import { requestStacked, requestMetaData } from '@/api/board'

export default {
  name: 'Dashboard',
  created() {
    this.getAppList()
    this.getMetaDate()
  },
  mounted() {
    this.stackedColumnPlot = new Column('ColumnBoard', {
      data: this.stackedColumnData,
      xField: 'weeks',
      yField: 'counts',
      seriesField: 'note',
      isGroup: this.stackedColumnMode ? 'true' : 'false',
      columnStyle: {
        radius: [20, 20, 0, 0]
      }
    })
    this.stackedColumnPlot.render()
  },
  data() {
    return {
      stackedColumnPlot: undefined,
      stackedColumnData: [],
      stackedColumnMode: true,
      searchValue: {
        date: []
      }
    }
  },
  methods: {
    getAppList() {
      requestStacked().then(resp => {
        this.initStackedChart(resp.data)
      })
    },
    getMetaDate() {
      const params = {
        date: this.searchValue.date
      }
      requestMetaData(params).then(resp => {
        this.stackedColumnData = resp.data
        this.stackedColumnPlot.changeData(this.stackedColumnData)
        // this.initStackedColumn(resp.data)
      })
    },
    // initStackedColumn(data) {
    //   const stackedColumnPlot = new Column('ColumnBoard', {
    //     data,
    //     xField: 'weeks',
    //     yField: 'counts',
    //     seriesField: 'note',
    //     isGroup: 'true',
    //     columnStyle: {
    //       radius: [20, 20, 0, 0]
    //     }
    //   })
    //   stackedColumnPlot.render()
    // },
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
    },
    searchBoard() {
      this.getMetaDate()
    },
    // 更改显示类型
    changeBoardMode() {
      const options = {
        isGroup: this.stackedColumnMode
      }
      this.stackedColumnPlot.update(options)
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
