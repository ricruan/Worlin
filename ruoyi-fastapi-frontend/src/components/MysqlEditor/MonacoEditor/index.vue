<template>
    <div ref="editorContainer" class="monaco-editor-container"></div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch, computed, onBeforeUpdate } from 'vue';
import * as monaco from 'monaco-editor';

const props = defineProps({
    language: {
        type: String,
        default: 'sql'
    },
    value: {
        type: String,
        default: ''
    },
    options: {
        type: Object,
        default: () => ({})
    }
})

const emit = defineEmits(['update:value']);

const editorContainer = ref(null);
let editor = null;
let oldValue = '';
const defaultMinWidth = 600  // 新增： 默认最小宽度
const containerWidth = ref(0) // 新增： 保存容器宽度

const containerStyle = computed(()=>({
    minWidth: `${defaultMinWidth}px`,
  width: containerWidth.value > defaultMinWidth?  "100%" : `${defaultMinWidth}px` , // 根据父容器宽度来决定是否100%宽度
}))


const createEditor = () => {
    if(!editorContainer.value) return
      containerWidth.value =  editorContainer.value.offsetWidth; //初始化组件的时候获取宽度
   editor = monaco.editor.create(editorContainer.value, {
        value: props.value,
        language: props.language,
        ...props.options,
    });
    editor.onDidChangeModelContent((e) => {
      const newValue = editor.getValue();
      oldValue = newValue;
      emit('update:value', newValue);
    });
};


const updateEditor = () => {
    if (editor && props.value !== oldValue ) {
         editor.setValue(props.value)
         editor.updateOptions({
           ...props.options
         });
          oldValue = props.value;
    }
}

defineExpose({
    focus: () => {
        if (editor) editor.focus()
    },
    setValue: (value)=>{
        if(editor) editor.setValue(value)
    }
})
onMounted(() => {
    createEditor();
        oldValue = props.value
});

onBeforeUpdate(()=>{
    if(editorContainer.value) {
        containerWidth.value =  editorContainer.value.offsetWidth;  //每次父组件发生变化的时候更新容器宽度
    }
})

watch(() => props.value, updateEditor)
watch(()=> props.options, updateEditor, { deep: true})

onUnmounted(() => {
    if (editor) {
        editor.dispose();
    }
});
</script>

<style scoped>
.monaco-editor-container {
  height: 100%;
  width: 100%;
  display: inline-block; /* 修改这里为inline-block */
}
</style>