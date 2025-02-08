<template>
    <div class="app-container">
        <div v-if="!showEditPage">
            <el-form :model="queryParams" ref="queryRef" v-show="showSearch" :inline="true" label-width="68px">
            <el-form-item label="题目标题" prop="problemTitle">
                <el-input
                    v-model="queryParams.problemTitle"
                    placeholder="请输入题目标题"
                    clearable
                    style="width: 240px"
                    @keyup.enter="handleQuery"
                />
            </el-form-item>
            <el-form-item label="题目标签" prop="problemTags">
                <el-input
                    v-model="queryParams.problemTags"
                    placeholder="请输入题目标签"
                    clearable
                    style="width: 240px"
                    @keyup.enter="handleQuery"
                />
            </el-form-item>
            <el-form-item label="语言类型" prop="languageType">
                <el-select
                    v-model="queryParams.languageType"
                    placeholder="请选择语言类型"
                    clearable
                    style="width: 240px"
                >
                    <el-option
                        v-for="item in languageTypeOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
                <el-button icon="Refresh" @click="resetQuery">重置</el-button>
            </el-form-item>
        </el-form>
        <el-row :gutter="10" class="mb8">
            <el-col :span="1.5">
                <el-button
                    type="primary"
                    plain
                    icon="Plus"
                    @click="handleAdd"
                >新增</el-button>
            </el-col>
            <el-col :span="1.5">
                <el-button
                    type="danger"
                    plain
                    icon="Delete"
                    :disabled="multiple"
                    @click="handleDelete"
                >删除</el-button>
            </el-col>
            <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
        </el-row>
    
        <!-- 表格数据 -->
        <el-table v-loading="loading" :data="roleList" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" align="center" />
            <el-table-column label="题目标题" prop="problemTitle" width="120" />
            <el-table-column label="题目标签" prop="problemTags" :show-overflow-tooltip="true" width="150" />
            <el-table-column label="题目内容" prop="problemContent" :show-overflow-tooltip="true" width="150" />
            <el-table-column label="语言类型" prop="languageType" :show-overflow-tooltip="true" width="150" />
            <el-table-column label="问题类型" prop="problemType" width="100" />
            <el-table-column label="难度等级" prop="difficultyLevel" width="100" />
            <el-table-column label="预设代码" prop="presetCode" :show-overflow-tooltip="true" width="150" />
            <el-table-column label="测试用例/答案" prop="testCasesAnswers" :show-overflow-tooltip="true" width="150" />
            <el-table-column label="是否启用" align="center" width="100">
                <template #default="scope">
                    <el-switch
                    v-model="scope.row.enableFlag"
                    active-value="1"
                    inactive-value="0"
                    @change="handleStatusChange(scope.row)"
                    ></el-switch>
                </template>
            </el-table-column>
            <el-table-column label="创建时间" align="center" prop="createTime">
                <template #default="scope">
                    <span>{{ parseTime(scope.row.createTime) }}</span>
                </template>
            </el-table-column>
            <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
                <template #default="scope">
                <el-tooltip content="修改" placement="top">
                    <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:problem:edit']"></el-button>
                </el-tooltip>
                <el-tooltip content="删除" placement="top">
                    <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:problem:remove']"></el-button>
                </el-tooltip>
                </template>
            </el-table-column>
        </el-table>
        <pagination
            v-show="total > 0"
            :total="total"
            v-model:page="queryParams.pageNum"
            v-model:limit="queryParams.pageSize"
            @pagination="getList"
        />
    
    
    
        <!-- 分配角色数据权限对话框 -->
        <el-dialog :title="title" v-model="openDataScope" width="500px" append-to-body>
            <el-form :model="form" label-width="80px">
                <el-form-item label="角色名称">
                    <el-input v-model="form.roleName" :disabled="true" />
                </el-form-item>
                <el-form-item label="权限字符">
                    <el-input v-model="form.roleKey" :disabled="true" />
                </el-form-item>
                <el-form-item label="权限范围">
                    <el-select v-model="form.dataScope" @change="dataScopeSelectChange">
                    <el-option
                        v-for="item in dataScopeOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="数据权限" v-show="form.dataScope == 2">
                    <el-checkbox v-model="deptExpand" @change="handleCheckedTreeExpand($event, 'dept')">展开/折叠</el-checkbox>
                    <el-checkbox v-model="deptNodeAll" @change="handleCheckedTreeNodeAll($event, 'dept')">全选/全不选</el-checkbox>
                    <el-checkbox v-model="form.deptCheckStrictly" @change="handleCheckedTreeConnect($event, 'dept')">父子联动</el-checkbox>
                    <el-tree
                    class="tree-border"
                    :data="deptOptions"
                    show-checkbox
                    default-expand-all
                    ref="deptRef"
                    node-key="id"
                    :check-strictly="!form.deptCheckStrictly"
                    empty-text="加载中，请稍候"
                    :props="{ label: 'label', children: 'children' }"
                    ></el-tree>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" @click="submitDataScope">确 定</el-button>
                    <el-button @click="cancelDataScope">取 消</el-button>
                </div>
            </template>
        </el-dialog>

        <!-- 分配角色数据权限对话框 -->
        <el-dialog :title="title" v-model="openDataScope" width="500px" append-to-body>
            <el-form :model="form" label-width="80px">
                <el-form-item label="角色名称">
                    <el-input v-model="form.roleName" :disabled="true" />
                </el-form-item>
                <el-form-item label="权限字符">
                    <el-input v-model="form.roleKey" :disabled="true" />
                </el-form-item>
                <el-form-item label="权限范围">
                    <el-select v-model="form.dataScope" @change="dataScopeSelectChange">
                    <el-option
                        v-for="item in dataScopeOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="数据权限" v-show="form.dataScope == 2">
                    <el-checkbox v-model="deptExpand" @change="handleCheckedTreeExpand($event, 'dept')">展开/折叠</el-checkbox>
                    <el-checkbox v-model="deptNodeAll" @change="handleCheckedTreeNodeAll($event, 'dept')">全选/全不选</el-checkbox>
                    <el-checkbox v-model="form.deptCheckStrictly" @change="handleCheckedTreeConnect($event, 'dept')">父子联动</el-checkbox>
                    <el-tree
                    class="tree-border"
                    :data="deptOptions"
                    show-checkbox
                    default-expand-all
                    ref="deptRef"
                    node-key="id"
                    :check-strictly="!form.deptCheckStrictly"
                    empty-text="加载中，请稍候"
                    :props="{ label: 'label', children: 'children' }"
                    ></el-tree>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" @click="submitDataScope">确 定</el-button>
                    <el-button @click="cancelDataScope">取 消</el-button>
                </div>
            </template>
        </el-dialog>
       
        </div>

        <div v-if="showEditPage" class="edit-page-container">
            <div class="edit-page-header">
                <el-button 
                class="edit-page-header-item "
                type="warning" 
                plain 
                icon="Close"
                @click="handleExport"
                >返回</el-button>
                <el-button 
                class="edit-page-header-item "
                type="primary"
                plain 
                icon="Close"
                @click="submit"
                >提交</el-button>
            </div>
            
            <el-form ref="editFormRef" :model="editPageForm" class="edit-form-content">
                <el-form-item label="问题标题">
                    <el-input v-model="editPageForm.problemTitle"></el-input>
                </el-form-item>
                <el-form-item label="问题标签">
                    <el-input v-model="editPageForm.problemTags"></el-input>
                </el-form-item>
                <el-form-item label="语言类型">
                    <el-input v-model="editPageForm.languageType"></el-input>
                </el-form-item>
                <el-form-item label="问题类型">
                    <el-input v-model="editPageForm.problemType"></el-input>
                </el-form-item>
                <el-form-item label="难度层级">
                    <el-input v-model="editPageForm.difficultyLevel"></el-input>
                </el-form-item>
                <el-form-item label="问题内容">
                  <div style="width: 100%;">
                    <editor v-model="editPageForm.problemContent" ></editor>
                  </div>
                </el-form-item>
                <el-form-item label="预设代码">
                  <MysqlEditor 
                        v-model="editPageForm.presetCode" 
                        :results="results" 
                        :headers="headers" 
                        :errorMessage="errorMessage"  
                        @execute="handleSQL" 
                        ref="PreEditor"
                    />
                </el-form-item>
                <el-form-item label="测试用例">
                  <MysqlEditor 
                            v-model="editPageForm.testCasesAnswers"
                            :pre-sql="editPageForm.presetCode"
                        />
                </el-form-item>
                <el-form-item label="是否启用">
                    <el-switch
                    v-model="editPageForm.enableFlag"
                    active-color="#13ce66"
                    inactive-color="#ff4949">
                    </el-switch>
                </el-form-item>
            </el-form>
        </div>
    </div>
 </template>
 
 <script setup name="Problem">

 import { addRole, changeRoleStatus, dataScope, delRole, getRole, listRole, updateRole, deptTreeSelect } from "@/api/system/role";
 import { getPageList,getDetail,insertOrUpdate,deleteBatch } from "@/api/system/problem";

 import MysqlEditor from "@/components/MysqlEditor/index.vue";
 
 const router = useRouter();
 const { proxy } = getCurrentInstance();
 
 const roleList = ref([]);
 const loading = ref(true);
 const showSearch = ref(true);
 const ids = ref([]);
 const single = ref(true);
 const multiple = ref(true);
 const total = ref(0);
 const dateRange = ref([]);

//  以下是新增的
const showEditPage = ref(false);
const results = ref([]);
const headers = ref([]);
const errorMessage = ref("");
const PreEditor = ref(null);
const AnsEditor = ref(null);
 
 
 const data = reactive({
   form: {},
   queryParams: {
     pageNum: 1,
     pageSize: 10,
     problemTitle: '',
     problemTags: '',
     languageType: '',
     problemType: '',
     difficultyLevel: ''
   },
   rules: {
     roleName: [{ required: true, message: "角色名称不能为空", trigger: "blur" }],
     roleKey: [{ required: true, message: "权限字符不能为空", trigger: "blur" }],
     roleSort: [{ required: true, message: "角色顺序不能为空", trigger: "blur" }]
   },
 });
 
 /**
  * ↓编辑页面代码区域
  */
const editorContainer = ref(null);

const editPageData = reactive({
    editPageForm: {}
})

const { editPageForm } = toRefs(editPageData);

  /**
  * ↑编辑页面代码区域
  */
 const { queryParams, form, rules } = toRefs(data);
 
 
 /** 查询题目列表 */
 function getList() {
   loading.value = true;
   getPageList(proxy.addDateRange(queryParams.value, dateRange.value)).then(response => {
     roleList.value = response.data.rows;
     total.value = response.data.total;
     loading.value = false;
   });
 }
 /** 搜索按钮操作 */
 function handleQuery() {
   queryParams.value.pageNum = 1;
   getList();
 }
 /** 重置按钮操作 */
 function resetQuery() {
   dateRange.value = [];
   proxy.resetForm("queryRef");
   handleQuery();
 }
 /** 删除按钮操作 */
 function handleDelete(row) {
   const roleIds = row.roleId || ids.value;
   proxy.$modal.confirm('是否确认删除角色编号为"' + roleIds + '"的数据项?').then(function () {
     return delRole(roleIds);
   }).then(() => {
     getList();
     proxy.$modal.msgSuccess("删除成功");
   }).catch(() => {});
 }
 /** 导出按钮操作 */
 function handleExport() {
   showEditPage.value = !showEditPage.value;
 }
 async function submit(){
   try {
     // 构造提交的数据
     const submitData = {
       ...editPageForm.value,
       // 确保布尔值的正确转换
       enableFlag: editPageForm.value.enableFlag ? 1 : 0
     };

     // 调用更新接口
     const response = await insertOrUpdate(submitData);
     
     if (response.code === 200) {
       proxy.$modal.msgSuccess("保存成功");
       // 关闭编辑页面
       showEditPage.value = false;
       // 刷新列表
       getList();
     } else {
       proxy.$modal.msgError(response.msg || "保存失败");
     }
   } catch (error) {
     console.error("保存失败:", error);
     proxy.$modal.msgError("保存失败，请稍后重试");
   }
 }
 /** 多选框选中数据 */
 function handleSelectionChange(selection) {
   ids.value = selection.map(item => item.id);
   single.value = selection.length != 1;
   multiple.value = !selection.length;
 }





 /** 添加题目 */
 function handleAdd() {
  editPageForm.value = {};
  showEditPage.value = true;
 }
 /** 修改角色 */
 async function handleUpdate(row) {
   try {
     // 获取详情数据
     const problemId = row.id;
     const response = await getDetail(problemId);
     
     // 将数据赋值给编辑表单
     editPageForm.value = {
       ...response.data,
       presetCode: response.data.presetCode || '',
       testCasesAnswers: response.data.testCasesAnswers || '',
       enableFlag: response.data.enableFlag || 0
     };
     
     // 显示编辑页面
     showEditPage.value = true;
   } catch (error) {
     proxy.$modal.msgError('获取详情失败：' + (error.message || '未知错误'));
   }
 }


 // 添加 handleSQL 函数的实现
 const handleSQL = async (sql, editor) => {
   try {
     // 这里可以添加执行 SQL 的逻辑
     // 比如调用后端 API 执行 SQL
     console.log('执行 SQL:', sql);
     
     // 模拟设置结果
     results.value = [];
     headers.value = [];
     errorMessage.value = '';
     
   } catch (error) {
     errorMessage.value = error.message || '执行 SQL 失败';
   }
 };
 
 // 添加语言类型选项
 const languageTypeOptions = ref([
     { value: 'MySQL', label: 'MySQL' },
     { value: 'Oracle', label: 'Oracle' },
     { value: 'PostgreSQL', label: 'PostgreSQL' },
     { value: 'SQLServer', label: 'SQLServer' }
 ]);
 
 getList();
 </script>

<style lang="css" scoped>
    .edit-page-header {
        display: flex;

    }
    .edit-page-header-item {
        flex-grow: 1; 
    }

    .edit-page-container {
    height: 100%;
    display: flex;
    flex-direction: column;
        overflow: hidden;
    }
    .edit-page-header {
        position: sticky;
        top: 0;
        background-color: white;        
        z-index: 1;
        padding: 10px 20px;
        margin-bottom: 20px;
        border-bottom: 1px solid #ddd;   
    }
    .edit-page-header-item {
        margin-right: 10px;
    }

    .edit-form-content {
        flex: 1;
        overflow-y: auto;
        padding: 0 20px 20px;
    }
    
    .problem-form {
        height: 80vh; /* 设置固定高度 */
    }

    .editor-wrapper {
        /* height: 300px; */
        width: 100%;
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
        border: 1px solid #ebeef5;
        border-radius: 4px;
        overflow: hidden;
    }

    /* 调整表单项间距 */
    .el-form-item {
        margin-bottom: 18px;
    }

    .el-form-item__label {
        font-weight: 500;
    }
</style>
 
 