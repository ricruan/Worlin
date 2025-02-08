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
        <el-button-group>
          <el-button type="primary" @click="handleExecute" :loading="isLoading">
            执行 SQL
          </el-button>
          <el-button @click="clearSQL">清空 SQL</el-button>
          <el-button @click="toggleLogs">
            {{ showLogs ? '隐藏日志栏' : '显示日志栏' }}
          </el-button>
        </el-button-group>
      </div>
  
      
      </div>
      <div v-if="showLogs" class="result-container">
        <div v-for="(result, index) in results" :key="index" class="result-item">
          <div class="result-header">
            <el-tag :type="result.status === 'success' ? 'success' : 'danger'">
              {{ result.type.toUpperCase() }} ({{ result.seq }})
            </el-tag>
            <span class="sql-snippet">{{ result.sql }}</span>
          </div>

          <!-- 查询结果展示 -->
          <el-table v-if="result.status === 'success' && result.type === 'query'" :data="result.data">
            <el-table-column 
              v-for="(value, key) in result.data[0] || {}" 
              :key="key"
              :prop="key"
              :label="key"
            />
          </el-table>

          <!-- 执行结果信息 -->
          <div class="execution-info" >
            <el-tag effect="dark" :type="result.status === 'success' ? 'success' : 'danger'">
              {{ result.status === 'success' ? '成功' : '失败' }}
            </el-tag>
            <span v-if="result.rows_affected > 0" class="rows-affected">
              影响行数: {{ result.rows_affected }}
            </span>
            <span v-if="result.message" class="error-msg">
              错误信息: {{ result.message }}
            </span>
          </div>
        </div>

        <div v-if="errorMessage" class="error-message">
          <el-alert :title="errorMessage" type="error" />
        </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, watch, defineEmits, defineProps } from 'vue';
  import { ElButton, ElTable, ElTableColumn, ElAlert, ElButtonGroup } from 'element-plus';
  import MonacoEditor from "./MonacoEditor/index.vue"; // 导入 MonacoEditor 组件
  import { executeSQL } from '@/api/coding'
  
  const props = defineProps({
    modelValue: {  // 改为 modelValue 以支持 v-model
        type: String,
        default: ''
    },
    results: {
        type: Array,
        default: () => []
    },
    headers: {
        type: Array,
        default: () => []
    },
    errorMessage: {
        type: String,
        default: ''
    },
    problemId: Number, // 题目ID（如果需要）
    preSql: {  // 新增预设SQL属性
        type: String,
        default: ''
    }
  });
  
  const emit = defineEmits(['update:modelValue', 'execute']);
  
  
  const sqlCode = ref(props.modelValue);
  const results = ref([]);
  const errorMessage = ref('');
  const isLoading = ref(false);
  
  const monacoEditorRef = ref(null);
  const editorOptions = reactive({
    theme: 'vs-dark',
    fontSize: 14,
    minimap: { enabled: false },
  });
  
  const showLogs = ref(false)  // 新增显示日志状态
  
  const clearSQL = () => {
    sqlCode.value = "";
    if (monacoEditorRef.value) {
      monacoEditorRef.value.setValue('');
    }
    results.value = []
    errorMessage.value = ''
  }
  
  
  const buildFullSql = () => {
    let fullSql = props.preSql.trim()
    const currentSql = sqlCode.value.trim()
    
    // 处理预设SQL的结尾分号
    if (fullSql) {
      if (!fullSql.endsWith(';')) {
        fullSql += ';'
      }
      fullSql += '\n'  // 添加换行分隔
    }
    
    // 处理当前SQL的起始分号
    if (currentSql.startsWith(';')) {
      fullSql += currentSql.slice(1)
    } else {
      fullSql += currentSql
    }
    
    return fullSql
  }
  
  const handleExecute = async () => {
    if (!sqlCode.value.trim()) return
    
    showLogs.value = true  // 执行时自动显示日志
    isLoading.value = true
    errorMessage.value = ''
    
    try {
      const fullSql = buildFullSql()
      const { data } = await executeSQL(fullSql)
      results.value = data
    } catch (err) {
      errorMessage.value = err.message || '执行失败'
      results.value = [] 
    } finally {
      isLoading.value = false
    }
  };
  
  
  // 监听外部值的变化
  watch(() => props.modelValue, (newVal) => {
    if (newVal !== sqlCode.value) {
        sqlCode.value = newVal;
    }
  });
  
  // 监听内部值的变化
  watch(() => sqlCode.value, (newVal) => {
    emit('update:modelValue', newVal);
  });
  
  const toggleLogs = () => {
    showLogs.value = !showLogs.value
  }
  
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
    height: 300px;
    width: 100%;
    min-height: 300px; /* 最小高度保障 */
  }
  
  .editor-container {
    height: 90%;
    width: 100%;
  }
  
  .toolbar {
    width: 100%;
    height: 10%;
  }
  
  .result-container {
    width: 100%;
    overflow-y: auto; /* 当内容溢出组件高度时，添加垂直滚动条 */
    border: 1px solid #dcdcdc; /* 添加边框 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影 */
    scroll-behavior: smooth; /* 平滑滚动 */
  }

  .result-container::-webkit-scrollbar {
    display: none; /* 隐藏滚动条 */
  }

  .result-container {
    -ms-overflow-style: none; /* IE 和 Edge 隐藏滚动条 */
    scrollbar-width: none; /* Firefox 隐藏滚动条 */
  }

  .result-container {
    display: flex;
    flex-direction: column-reverse; /* 默认滑动至最下面 */
  }
  
  .result-container.hidden {
    max-height: 0;
    min-height: 0;
  }
  
  .result-item {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
  }
  
  .result-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .sql-snippet {
    margin-left: 10px;
    color: #666;
    font-family: monospace;
    font-size: 0.9em;
  }
  
  .execution-info {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px dashed #eee;
  }
  
  .rows-affected {
    margin-left: 15px;
    color: #67C23A;
  }
  
  .error-msg {
    margin-left: 15px;
    color: #F56C6C;
  }
  
  .error-message {
    margin-top: 15px;
  }
  </style>