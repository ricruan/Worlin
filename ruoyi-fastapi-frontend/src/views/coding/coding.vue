<template>
    <div class="code-page">
        <div class="code-header">
            <el-row style="height: 100%;">
                <el-col :span="8" class="header-button" style="justify-content: left;"> 
                    <div style="height: 100%; float: left;">
                        <img src="../../assets/images/worlin.png" class="image-content">
                    </div>
                    <el-button style="margin-left: 15%;">问题列表</el-button> </el-col>
                <el-col :span="8" class="header-button"> <el-button >下一题</el-button> </el-col>
                <el-col :span="8" class="header-button"> <el-button type="danger">登录/注册</el-button> </el-col>
            </el-row>
        </div>
        <div class="code-body">
                <div class="code-body-item">
                    <el-tabs v-model="activeName" @tab-click="handleClick">
                        <el-tab-pane label="问题内容" name="first">问题内容</el-tab-pane>
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
  
  const editorContainer = ref(null);
  const isConsoleVisible = ref(false);
  const logContent = ref('');
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
    height: 8%;
    flex-grow: 1; 
   }

   .code-body{
    display: flex;
    flex-grow: 1; 
    margin-top: 15px;
   }

   .code-footer{
    flex-grow: 1; 
    height: 20%;
   }

   .code-body-item{
    width: 50%;
    flex-grow: 1;          /* 让子元素平分父容器宽度 */
   }

   .code-in-button {
    /* padding: 10px; */
   }

   .code-page{
    height: 100%;
    display: flex;
    flex-direction:column;
   }


  </style>