<template>
    <div class="problem-list-page">
        <!-- 头部搜索区域 -->
        <div class="search-header">
            <el-form :inline="true" :model="queryParams" class="search-form">
                <el-form-item label="题目标题">
                    <el-input
                        v-model="queryParams.problemTitle"
                        placeholder="请输入题目标题"
                        clearable
                        @keyup.enter="handleQuery"
                    />
                </el-form-item>
                <el-form-item label="问题类型">
                    <el-select 
                        class="custom-select"
                        v-model="queryParams.problemType" 
                        placeholder="请选择问题类型" 
                        clearable>
                        <el-option v-for="item in problemTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="难度层级">
                    <el-select 
                        class="custom-select"
                        v-model="queryParams.difficultyLevel" 
                        placeholder="请选择难度" 
                        clearable>
                        <el-option v-for="item in difficultyLevelOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
                    <el-button icon="Refresh" @click="resetQuery">重置</el-button>
                </el-form-item>
            </el-form>
        </div>

        <!-- 问题列表区域 -->
        <div class="problem-list">
            <el-table :data="problemList" style="width: 100%" @row-click="handleProblemClick">
                <el-table-column type="index" label="序号" width="60" />
                <el-table-column prop="problemTitle" label="题目标题" show-overflow-tooltip>
                    <template #default="{ row }">
                        <span class="list-problem-title">{{ row.problemTitle }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="problemType" label="问题类型" width="120">
                    <template #default="{ row }">
                        <el-tag :type="getTypeTagType(row.problemType)" :value="row.problemType">
                            {{ row.problemType }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="difficultyLevel" label="难度" width="100">
                    <template #default="{ row }">
                        <el-tag :type="getDifficultyTagType(row.difficultyLevel)">
                            {{ row.difficultyLevel }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="languageType" label="语言" width="100">
                    <template #default="{ row }">
                        <el-tag type="info">{{ row.languageType }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column fixed="right" label="操作" width="120">
                    <template #default="{ row }">
                        <el-button link type="primary" @click.stop="handleStart(row)">开始解答</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <div class="pagination-container">
                <el-pagination
                    v-model:current-page="queryParams.pageNum"
                    v-model:page-size="queryParams.pageSize"
                    :page-sizes="[10, 20, 30, 50]"
                    :total="total"
                    layout="total, sizes, prev, pager, next, jumper"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getPageList } from "@/api/system/problem";
import { useRouter } from 'vue-router';

const router = useRouter();
const total = ref(0);
const problemList = ref([]);
const queryParams = ref({
    pageNum: 1,
    pageSize: 10,
    problemTitle: '',
    problemType: '',
    difficultyLevel: ''
});

const problemTypeOptions = ref([
    { value: '选择题', label: '选择题' },
    { value: '编程题', label: '编程题' },
    { value: '填空题', label: '填空题' },
    { value: '问答题', label: '问答题' }
]);

const difficultyLevelOptions = ref([
    { value: '简单', label: '简单' },
    { value: '中等', label: '中等' },
    { value: '困难', label: '困难' }
]);



// 获取问题列表
const getList = async () => {
    try {
        const response = await getPageList(queryParams.value);
        problemList.value = response.data.rows;
        total.value = response.data.total;
    } catch (error) {
        console.error('获取问题列表失败:', error);
    }
};

// 搜索
const handleQuery = () => {
    queryParams.value.pageNum = 1;
    getList();
};

// 重置
const resetQuery = () => {
    queryParams.value = {
        pageNum: 1,
        pageSize: 10,
        problemTitle: '',
        problemType: '',
        difficultyLevel: ''
    };
    getList();
};

// 处理页面大小变化
const handleSizeChange = (val) => {
    queryParams.value.pageSize = val;
    getList();
};

// 处理页码变化
const handleCurrentChange = (val) => {
    queryParams.value.pageNum = val;
    getList();
};

// 开始解答
const handleStart = (row) => {
    router.push({
        path: '/codingPage',
        query: { 
            id: row.id,
            problemTitle: row.problemTitle,
            problemContent: row.problemContent
        }
    });
};

// 获取问题类型对应的标签类型
const getTypeTagType = (type) => {
    const typeMap = {
        '选择题': '',
        '编程题': 'success',
        '填空题': 'warning',
        '问答题': 'info'
    };
    return typeMap[type] || '';
};

// 获取难度对应的标签类型
const getDifficultyTagType = (difficulty) => {
    const difficultyMap = {
        '简单': 'success',
        '中等': 'warning',
        '困难': 'danger'
    };
    return difficultyMap[difficulty] || '';
};

// 处理行点击
const handleProblemClick = (row) => {
    handleStart(row);
};

onMounted(() => {
    getList();
});
</script>

<style scoped>
.problem-list-page {
    padding: 20px;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.search-header {
    margin-bottom: 20px;
    background: #fff;
    padding: 20px;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.problem-list {
    flex: 1;
    background: #fff;
    padding: 20px;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    overflow: auto;
}

.list-problem-title {
    color: #409EFF;
    cursor: pointer;
    font-size: 14px;
    font-weight: normal;
}

.list-problem-title:hover {
    text-decoration: underline;
}

.pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
}

.search-form {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

:deep(.el-form--inline .el-form-item) {
    margin-right: 0;
}

.custom-select {
    width: 120px;  /* 你可以根据需要调整这个值 */
}
</style> 