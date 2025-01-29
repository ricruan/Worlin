<template>
    <div class="mysql-code-editor">
  
      <div class="editor-container">
        <MonacoEditor
          ref="monacoEditorRef"
          language="mysql"
          v-model:value="sqlCode"
          :options="editorOptions"
        />
      </div>
          <div class="toolbar">
        <el-button-group v-if="sqlCode.length > 0">
          <el-button type="primary" @click="handleExecute">执行 SQL</el-button>
          <el-button @click="clearSQL">清空 SQL</el-button>
         </el-button-group>
      </div>
  
      <div class="result-container" v-if="results && results.length > 0">
        <el-table
          :data="results"
           stripe
        >
            <el-table-column
                  v-for="(header, index) in headers"
                    :key="index"
                  :prop="header"
                  :label="header"
               >
                </el-table-column>
        </el-table>
           <div class="result-message" v-if="errorMessage">
              <el-alert :title="errorMessage" type="error" show-icon />
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, watch, defineEmits, defineProps } from 'vue';
  import { ElButton, ElTable, ElTableColumn, ElAlert, ElButtonGroup } from 'element-plus';
  import MonacoEditor from "./MonacoEditor/index.vue"; // 导入 MonacoEditor 组件
  
  const props = defineProps({
    results:{
      type:Array,
        default:()=>[]
    },
      headers:{
          type: Array,
            default:()=>[]
      },
      errorMessage:{
          type: String,
          default: ""
      }
  })
  
  const emit = defineEmits(['execute']);
  
  
  const sqlCode = ref('');
  
  const monacoEditorRef = ref(null);
  const editorOptions = reactive({
    theme: 'vs-dark',
    fontSize: 14,
    minimap: { enabled: false },
  });
  
  
  const clearSQL = () => {
    sqlCode.value = "";
    if (monacoEditorRef.value) {
      monacoEditorRef.value.setValue('');
    }
  }
  
  
  const handleExecute = () => {
    emit('execute', sqlCode.value);
  };
  
  
  watch(()=> sqlCode.value, (newValue)=>{
      console.log("sql code change:", newValue);
  })
  
  onMounted(() => {
    if (monacoEditorRef.value) {
      monacoEditorRef.value.focus();
    }
  });
  </script>
  
  <style scoped>
  .mysql-code-editor {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
  }
  
  
  .editor-container {
    flex: 1;
    padding: 10px;
    min-height: 300px;
       width: 100%;
  }
  .toolbar {
      padding: 10px;
      display: flex;
      justify-content: space-between;
      border-top: 1px solid #ddd;
  }
  
  .result-container {
    padding: 10px;
    border-top: 1px solid #ddd;
    max-height: 300px;
    overflow-y: auto;
  }
  .result-message {
      margin-top: 10px;
  }
  </style>