<template>
  <div class="app-container">
    <div>
      <!-- 以下为表格的搜索功能 -->
      <el-row>
        <el-input style="width: 150px" size="mini"/>
        <el-button size="mini" style="margin-left: 10px" type="topsmallcss" round icon="el-icon-search">搜索</el-button>
        <el-button size="mini" round style="margin-left: 10px" type="topsmallcss" icon="el-icon-refresh-right">重置</el-button>
        <div style="float: right; overflow: hidden">
          <el-button class="filter-item" style="margin-left: 10px" type="addcss" size="mini" round icon="el-icon-circle-plus-outline"></el-button>
          <el-button v-waves :loading="downloadLoading" class="filter-item" type="topsmallcss" style="margin-left: 10px" size="mini"  round icon="el-icon-document-copy"></el-button>
          <upload-excel-component :on-success="handleSuccess" :before-upload="beforeUpload" style="display: inline" />
          <el-button v-waves :loading="downloadLoading" class="filter-item" type="topsmallcss" style="margin-left: 10px" size="mini" round icon="el-icon-download"></el-button>
        </div>
      </el-row>
    </div>
  </div>
</template>