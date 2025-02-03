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
                <el-col :span="8" class="header-button"> <el-button type="danger">登录/注册</el-button> </el-col>
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
                        <el-tab-pane label="查询结果" name="second">查询结果</el-tab-pane>
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
                        <el-button class="code-in-button" type="success">保存并提交</el-button>
                    </div>
                </div>
        </div>
        <div class="code-footer" v-if="isConsoleVisible">
            <el-input
            type="textarea"
            :rows="4"
            readonly
            placeholder="请输入内容"
            v-model="logContent">
            </el-input>
        </div>
    </div>
    
    
</template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  import * as monaco from 'monaco-editor';
  import { useRoute, useRouter } from 'vue-router';
  import { getDetail } from "@/api/system/problem";  // 导入获取详情的 API
  
  const route = useRoute();
  const router = useRouter();  // 添加 router
  const editorContainer = ref(null);
  const isConsoleVisible = ref(false);
  const logContent = ref('');
  const activeName = ref('first');
  const problemTitle = ref('');
  const problemContent = ref('');
  let editor = null;
  let logInterval = null;
  let logLines = [];
  let i = 0;

  const log = (message) => {
    logContent.value = logContent.value + "\n" +  message
};


  const startStreaming = (code) => {
    
     logLines = [
      "正在准备执行...",
       `执行SQL: ${code}`,
      "开始连接数据库...",
       "验证权限...",
       "开始执行SQL...",
     ]
     logContent.value = logContent.value + "123"

     i = 0;
    logInterval = setInterval(() => {
       if(i < logLines.length){
          log(logLines[i++])
       } else{
            log("执行完毕")
         clearInterval(logInterval)
          logInterval = null
        }
    }, 200 + Math.random() * 300); // 随机间隔 200-500 毫秒
  };

const stopStreaming = ()=>{
      if(logInterval){
         clearInterval(logInterval)
         logInterval = null
      }
}


  function runCode() {
    console.log("nnnnn")
    isConsoleVisible.value = true;
    startStreaming("select * from");
    }

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
            
        }
    } catch (error) {
        console.error('获取问题详情失败:', error);
    }
};
  
  // 添加跳转到列表页的方法
  const goToList = () => {
    router.push('/codingList');
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
    height: 8vh;  /* 使用视窗高度 */
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

  </style>