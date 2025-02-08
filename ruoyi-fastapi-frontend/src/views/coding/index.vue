<template>
    <div class="code-page">
        <div class="code-header">
            <el-row style="height: 100%;">
                <el-col :span="8" class="header-button" style="justify-content: left;"> 
                    <div style="height: 100%; float: left;">
                        <img src="../../assets/images/worlin.png" class="image-content">
                    </div>
                    <el-button style="margin-left: 15%;" @click="goToList">问题列表</el-button>
                </el-col>
                <el-col :span="8" class="header-button"> <el-button >下一题</el-button> </el-col>
                <el-col :span="8" class="header-button"> <el-button type="danger">不要点我</el-button> </el-col>
            </el-row>
        </div>
        <div class="code-body">
                <div class="code-body-item">
                    <el-tabs v-model="activeName" @tab-click="handleClick">
                        <el-tab-pane label="问题内容" name="first">
                            <div class="problem-content">
                                <h2 class="problem-title">{{ problemTitle }}</h2>
                                <div class="problem-detail" v-html="problemContent"></div>
                            </div>
                        </el-tab-pane>
                        <el-tab-pane label="查询结果" name="second">
                            <div class="result-container">
                                <el-table v-if="queryResult.length > 0" :data="queryResult" height="500">
                                    <el-table-column 
                                        v-for="(value, key) in queryResult[0] || {}" 
                                        :key="key"
                                        :prop="key"
                                        :label="key"
                                    />
                                </el-table>
                                <div v-else class="empty-result">暂无查询结果</div>
                            </div>
                        </el-tab-pane>
                        <el-tab-pane label="用户讨论" name="third">用户讨论</el-tab-pane>
                        <el-tab-pane label="竞速排名" name="fourth">竞速排名</el-tab-pane>
                    </el-tabs>
                </div>
                <div class="code-body-item">
                    <div ref="editorContainer" style="height: 90%;"></div> 
                    <div style="height: 10%;" class="code-button">
                        <div class="code-in-button">
                            <el-button  @click="runCode" type="primary">点击运行</el-button>
                            <el-button  @click="closeConsole">隐藏日志栏</el-button>
                        </div>
                        <el-button class="code-in-button" type="success" @click="submitCode">保存并提交</el-button>
                    </div>
                </div>
        </div>
        <div class="code-footer" v-if="isConsoleVisible">
            <el-input
            type="textarea"
            :rows="4"
            readonly
            placeholder="请输入内容"
            v-model="logContent"
            style="height: 100%;"
            >
            </el-input>
        </div>
    </div>
    
    
</template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  import * as monaco from 'monaco-editor';
  import { useRoute, useRouter } from 'vue-router';
  import { getDetail } from "@/api/system/problem";  // 导入获取详情的 API
  import { executeSQL, validateSQL } from '@/api/coding'
  import { ElMessage } from 'element-plus'
  
  const route = useRoute();
  const router = useRouter();  // 添加 router
  const editorContainer = ref(null);
  const isConsoleVisible = ref(false);
  const logContent = ref('');
  const activeName = ref('first');
  const problemTitle = ref('');
  const problemContent = ref('');
  const queryResult = ref([]);
  const presetSql = ref('');
  let editor = null;

  const log = (message) => {
    logContent.value = logContent.value + "\n" +  message
};

  const runCode = async () => {
    try {
        log("开始执行代码");
        const userSql = editor.getValue().trim();
        let fullSql = '';
        
        // 处理预设SQL
        if (presetSql.value) {
            fullSql = presetSql.value.trim();
            // 确保预设SQL以分号结尾
            if (!fullSql.endsWith(';')) {
                fullSql += ';';
            }
            fullSql += '\n';  // 添加换行分隔
        }
        console.log(fullSql);
        console.log(userSql);
        // 在日志栏组件中打印准备执行的fullsql
        log(`准备执行的SQL: ${fullSql}`);
        // 处理用户SQL的起始分号
        if (userSql.startsWith(';')) {
            fullSql += userSql.slice(1);
        } else {
            fullSql += userSql;
        }
        
        const response = await executeSQL(fullSql);
        
        // 处理查询结果
        if (response.data.some(item => item.type === 'query')) {
            activeName.value = 'second';
            queryResult.value = response.data
                .filter(item => item.type === 'query' && item.status === 'success')
                .flatMap(item => item.data);
        }
        
        // 记录执行日志
        logContent.value = response.data
            .map(item => `${item.type.toUpperCase()} [${item.status}]: ${item.message}`)
            .join('\n');
            
    } catch (error) {
        logContent.value = `执行出错: ${error.message}`;
        queryResult.value = [];
    }
    isConsoleVisible.value = true;
};

    function closeConsole() {
        isConsoleVisible.value = false;
    }
  
  onMounted(() => {
      editor = monaco.editor.create(editorContainer.value, {
          value: 'Select * from',
          language: 'mysql',
          theme: 'vs-dark',
          automaticLayout: true
        // ... 其他配置项
      });
      
      // 获取问题详情
      getProblemDetail();
  });
  
  onUnmounted(() => {
      if (editor) {
          editor.dispose();
          editor = null;
      }
  });
  
  defineExpose({
      getValue(){
          return editor.getValue();
      }
  })
  
  // 获取问题详情
  const getProblemDetail = async () => {
    try {
        const id = route.query.id;
        if (id) {
            const response = await getDetail(id);
            const problem = response.data;
            problemTitle.value = problem.problemTitle;
            problemContent.value = problem.problemContent;
            presetSql.value = problem.presetCode || ''; // 获取预设SQL
        }
    } catch (error) {
        console.error('获取问题详情失败:', error);
    }
};
  
  // 添加跳转到列表页的方法
  const goToList = () => {
    router.push('/codingList');
  };
  
  const submitCode = async () => {
    try {
        const userSql = editor.getValue().trim();
        let fullSql = '';
        
        // 复用SQL拼接逻辑
        if (presetSql.value) {
            fullSql = presetSql.value.trim();
            if (!fullSql.endsWith(';')) {
                fullSql += ';';
            }
            fullSql += '\n';
        }
        
        if (userSql.startsWith(';')) {
            fullSql += userSql.slice(1);
        } else {
            fullSql += userSql;
        }

        const response = await validateSQL({
            problem_id: route.query.id,
            sql: fullSql
        });

        // 记录日志
        logContent.value = `验证结果: ${response.data.status}\n${response.data.error || ''}`;
        
        // 处理结果展示
        if (response.data.user_result) {
            activeName.value = 'second';
            queryResult.value = response.data.user_result
                .filter(item => item.type === 'query' && item.status === 'success')
                .flatMap(item => item.data);
        }

        // 显示验证结果弹窗
        if (response.data.status === 'success') {
            ElMessage.success({
                message: '答题正确！',
                duration: 3000
            });
        } else {
            ElMessage.error({
                message: '答案错误: ' + (response.data.error || '结果不匹配'),
                duration: 5000
            });
        }

    } catch (error) {
        logContent.value = `验证出错: ${error.message}`;
        queryResult.value = [];
        ElMessage.error('验证请求失败: ' + error.message);
    }
    isConsoleVisible.value = true;
};
  
  </script>
  
  <style>
   .monaco-editor{
     border: 1px solid black;
   }

   .question-content{
    border: 1px solid burlywood;
   }
   .coding-main-col{
    height: 100%;
   }

   .header-button{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
   }

   .image-content {
    max-width: 100%;   /* 图片最大宽度为 100% */
    max-height: 100%; /* 图片最大高度为 100% */
    display: block; /* 可以解决图片下方有空白的问题 */

}

   .code-button{
    display: flex;           /* 设置为 flex 容器 */
    justify-content: space-between;  /*  子元素分散对齐 */
    align-items: center;   /* 可选： 如果要垂直居中对齐子元素 */
    padding: 10px;
   }

   .code-header{
    box-shadow: 
        2px 2px 4px rgba(0, 0, 0, 0.2), 
        4px 4px 8px rgba(0, 0, 0, 0.1);
    height: 6vh;  /* 使用视窗高度 */
    flex-grow: 1; 
   }

   .code-body{
    display: flex;
    height: 90vh;  /* 固定高度，预留空间给header和footer */
    margin-top: 15px;
    overflow: hidden;  /* 防止内容溢出 */
   }

   .code-footer{
    /* height: 200px; */
   }

   .code-body-item{
    width: 50%;
    height: 100%;  /* 继承父元素高度 */
    overflow: auto;  /* 允许内容滚动 */
   }

   /* 让 el-tabs 容器也是 flex 布局 */
   .code-body-item :deep(.el-tabs) {
    display: flex;
    flex-direction: column;
    height: 100%;
   }

   /* 让 tab 内容区域可以滚动 */
   .code-body-item :deep(.el-tabs__content) {
    flex: 1;
    overflow: hidden;
   }

   /* 让每个 tab-pane 都填满高度 */
   .code-body-item :deep(.el-tab-pane) {
    height: 100%;
   }

   .code-in-button {
    /* padding: 10px; */
   }

   .code-page{
    height: 100vh;  /* 使用视窗高度 */
    display: flex;
    flex-direction:column;
   }

   .problem-content {
    padding: 20px;
    height: calc(100% - 40px);  /* 减去tabs的高度 */
    overflow-y: auto;  /* 允许垂直滚动 */
    box-sizing: border-box; /* 添加这行 */
}

.problem-title {
    margin-bottom: 20px;
    color: #333;
    font-size: 24px;
}

.problem-detail {
    line-height: 1.6;
    color: #666;
}

/* 确保富文本内容正确显示 */
.problem-detail :deep(p) {
    margin-bottom: 16px;
}

.problem-detail :deep(pre) {
    background-color: #f5f5f5;
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
}

.problem-detail :deep(code) {
    background-color: #f5f5f5;
    padding: 2px 4px;
    border-radius: 2px;
}

.result-container {
    padding: 20px;
    height: calc(100% - 40px);
    overflow: auto;
}

.empty-result {
    color: #999;
    text-align: center;
    padding: 20px;
}

/* 优化弹窗样式 */
.el-message {
    font-size: 16px;
    min-width: 300px;
}
.el-message-success {
    background: #f0f9eb;
    border-color: #e1f3d8;
}
.el-message-error {
    background: #fef0f0;
    border-color: #fde2e2;
}

  </style>