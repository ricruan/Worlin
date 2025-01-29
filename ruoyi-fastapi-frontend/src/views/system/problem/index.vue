<template>
    <div class="app-container">
        <div v-if="!showEditPage">
            <el-form :model="queryParams" ref="queryRef" v-show="showSearch" :inline="true" label-width="68px">
            <el-form-item label="题目标题" prop="roleName">
                <el-input
                    v-model="queryParams.roleName"
                    placeholder="请输入题目标题"
                    clearable
                    style="width: 240px"
                    @keyup.enter="handleQuery"
                />
            </el-form-item>
            <el-form-item label="题目标签" prop="roleKey">
                <el-input
                    v-model="queryParams.roleKey"
                    placeholder="请输入题目标签"
                    clearable
                    style="width: 240px"
                    @keyup.enter="handleQuery"
                />
            </el-form-item>
            <el-form-item label="语言类型" prop="status">
                <el-select
                    v-model="queryParams.status"
                    placeholder="语言类型"
                    clearable
                    style="width: 240px"
                >
                    <el-option
                    v-for="dict in sys_normal_disable"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
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
                    v-hasPermi="['system:role:add']"
                >新增</el-button>
            </el-col>
            <el-col :span="1.5">
                <el-button
                    type="success"
                    plain
                    icon="Edit"
                    :disabled="single"
                    @click="handleUpdate"
                    v-hasPermi="['system:role:edit']"
                >修改</el-button>
            </el-col>
            <el-col :span="1.5">
                <el-button
                    type="danger"
                    plain
                    icon="Delete"
                    :disabled="multiple"
                    @click="handleDelete"
                    v-hasPermi="['system:role:remove']"
                >删除</el-button>
            </el-col>
            <el-col :span="1.5">
                <el-button
                    type="warning"
                    plain
                    icon="Download"
                    @click="handleExport"
                    v-hasPermi="['system:role:export']"
                >切换</el-button>
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
    
        <!-- 添加或修改角色配置对话框 -->
        <el-dialog :title="title" v-model="open" width="500px" append-to-body>
            <el-form ref="roleRef" :model="form" :rules="rules" label-width="100px">
                <el-form-item label="角色名称" prop="roleName">
                    <el-input v-model="form.roleName" placeholder="请输入角色名称" />
                </el-form-item>
                <el-form-item prop="roleKey">
                    <template #label>
                    <span>
                        <el-tooltip content="控制器中定义的权限字符，如：@PreAuthorize(`@ss.hasRole('admin')`)" placement="top">
                            <el-icon><question-filled /></el-icon>
                        </el-tooltip>
                        权限字符
                    </span>
                    </template>
                    <el-input v-model="form.roleKey" placeholder="请输入权限字符" />
                </el-form-item>
                <el-form-item label="角色顺序" prop="roleSort">
                    <el-input-number v-model="form.roleSort" controls-position="right" :min="0" />
                </el-form-item>
                <el-form-item label="状态">
                    <el-radio-group v-model="form.status">
                    <el-radio
                        v-for="dict in sys_normal_disable"
                        :key="dict.value"
                        :value="dict.value"
                    >{{ dict.label }}</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="菜单权限">
                    <el-checkbox v-model="menuExpand" @change="handleCheckedTreeExpand($event, 'menu')">展开/折叠</el-checkbox>
                    <el-checkbox v-model="menuNodeAll" @change="handleCheckedTreeNodeAll($event, 'menu')">全选/全不选</el-checkbox>
                    <el-checkbox v-model="form.menuCheckStrictly" @change="handleCheckedTreeConnect($event, 'menu')">父子联动</el-checkbox>
                    <el-tree
                    class="tree-border"
                    :data="menuOptions"
                    show-checkbox
                    ref="menuRef"
                    node-key="id"
                    :check-strictly="!form.menuCheckStrictly"
                    empty-text="加载中，请稍候"
                    :props="{ label: 'label', children: 'children' }"
                    ></el-tree>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="form.remark" type="textarea" placeholder="请输入内容"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" @click="submitForm">确 定</el-button>
                    <el-button @click="cancel">取 消</el-button>
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
                    <el-input v-model="editPageForm.problem_title"></el-input>
                </el-form-item>
                <el-form-item label="问题标签">
                    <el-input v-model="editPageForm.problem_tags"></el-input>
                </el-form-item>
                <el-form-item label="语言类型">
                    <el-input v-model="editPageForm.language_type"></el-input>
                </el-form-item>
                <el-form-item label="问题类型">
                    <el-input v-model="editPageForm.problem_type"></el-input>
                </el-form-item>
                <el-form-item label="难度层级">
                    <el-input v-model="editPageForm.difficulty_level"></el-input>
                </el-form-item>
                <el-form-item label="问题内容">
                    <editor v-model="editPageForm.problem_content"></editor>
                </el-form-item>
                <el-form-item label="预设代码">
                    <MysqlEditor v-model="editPageForm.preset_code" :results="results" :headers="headers" :errorMessage="errorMessage"  @execute="handleSQL" ref="PreEditor"></MysqlEditor>
                </el-form-item>
                <el-form-item label="测试用例">
                    <MysqlEditor v-model="editPageForm.test_cases_answers" :results="results" :headers="headers" :errorMessage="errorMessage"  @execute="handleSQL" ref="AnsEditor"></MysqlEditor>
                </el-form-item>
                <el-form-item label="是否启用">
                    <el-switch
                    v-model="editPageForm.enable_flag"
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
 import { getPageList } from "@/api/system/problem";

 import { roleMenuTreeselect, treeselect as menuTreeselect } from "@/api/system/menu";
 
 const router = useRouter();
 const { proxy } = getCurrentInstance();
 const { sys_normal_disable } = proxy.useDict("sys_normal_disable");
 
 const roleList = ref([]);
 const open = ref(false);
 const loading = ref(true);
 const showSearch = ref(true);
 const ids = ref([]);
 const single = ref(true);
 const multiple = ref(true);
 const total = ref(0);
 const title = ref("");
 const dateRange = ref([]);
 const menuOptions = ref([]);
 const menuExpand = ref(false);
 const menuNodeAll = ref(false);
 const deptExpand = ref(true);
 const deptNodeAll = ref(false);
 const deptOptions = ref([]);
 const openDataScope = ref(false);
 const menuRef = ref(null);
 const deptRef = ref(null);
//  以下是新增的
const showEditPage = ref(false);
 
 /** 数据范围选项*/
 const dataScopeOptions = ref([
   { value: "1", label: "全部数据权限" },
   { value: "2", label: "自定数据权限" },
   { value: "3", label: "本部门数据权限" },
   { value: "4", label: "本部门及以下数据权限" },
   { value: "5", label: "仅本人数据权限" }
 ]);
 
 const data = reactive({
   form: {},
   queryParams: {
     pageNum: 1,
     pageSize: 10,
     roleName: undefined,
     roleKey: undefined,
     status: undefined
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
 
 
 /** 查询角色列表 */
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
 function submit(){

 }
 /** 多选框选中数据 */
 function handleSelectionChange(selection) {
   ids.value = selection.map(item => item.roleId);
   single.value = selection.length != 1;
   multiple.value = !selection.length;
 }
 /** 角色状态修改 */
 function handleStatusChange(row) {
   let text = row.status === "0" ? "启用" : "停用";
   proxy.$modal.confirm('确认要"' + text + '""' + row.roleName + '"角色吗?').then(function () {
     return changeRoleStatus(row.roleId, row.status);
   }).then(() => {
     proxy.$modal.msgSuccess(text + "成功");
   }).catch(function () {
     row.status = row.status === "0" ? "1" : "0";
   });
 }
 /** 更多操作 */
 function handleCommand(command, row) {
   switch (command) {
     case "handleDataScope":
       handleDataScope(row);
       break;
     case "handleAuthUser":
       handleAuthUser(row);
       break;
     default:
       break;
   }
 }
 /** 分配用户 */
 function handleAuthUser(row) {
   router.push("/system/role-auth/user/" + row.roleId);
 }
 /** 查询菜单树结构 */
 function getMenuTreeselect() {
   menuTreeselect().then(response => {
     menuOptions.value = response.data;
   });
 }
 /** 所有部门节点数据 */
 function getDeptAllCheckedKeys() {
   // 目前被选中的部门节点
   let checkedKeys = deptRef.value.getCheckedKeys();
   // 半选中的部门节点
   let halfCheckedKeys = deptRef.value.getHalfCheckedKeys();
   checkedKeys.unshift.apply(checkedKeys, halfCheckedKeys);
   return checkedKeys;
 }
 /** 重置新增的表单以及其他数据  */
 function reset() {
   if (menuRef.value != undefined) {
     menuRef.value.setCheckedKeys([]);
   }
   menuExpand.value = false;
   menuNodeAll.value = false;
   deptExpand.value = true;
   deptNodeAll.value = false;
   form.value = {
     roleId: undefined,
     roleName: undefined,
     roleKey: undefined,
     roleSort: 0,
     status: "0",
     menuIds: [],
     deptIds: [],
     menuCheckStrictly: true,
     deptCheckStrictly: true,
     remark: undefined
   };
   proxy.resetForm("roleRef");
 }
 /** 添加角色 */
 function handleAdd() {
   reset();
   getMenuTreeselect();
   open.value = true;
   title.value = "添加角色";
 }
 /** 修改角色 */
 function handleUpdate(row) {
   reset();
   const roleId = row.roleId || ids.value;
   const roleMenu = getRoleMenuTreeselect(roleId);
   getRole(roleId).then(response => {
     form.value = response.data;
     form.value.roleSort = Number(form.value.roleSort);
     open.value = true;
     nextTick(() => {
       roleMenu.then((res) => {
         let checkedKeys = res.checkedKeys;
         checkedKeys.forEach((v) => {
           nextTick(() => {
             menuRef.value.setChecked(v, true, false);
           });
         });
       });
     });
     title.value = "修改角色";
   });
 }
 /** 根据角色ID查询菜单树结构 */
 function getRoleMenuTreeselect(roleId) {
   return roleMenuTreeselect(roleId).then(response => {
     menuOptions.value = response.menus;
     return response;
   });
 }
 /** 根据角色ID查询部门树结构 */
 function getDeptTree(roleId) {
   return deptTreeSelect(roleId).then(response => {
     deptOptions.value = response.depts;
     return response;
   });
 }
 /** 树权限（展开/折叠）*/
 function handleCheckedTreeExpand(value, type) {
   if (type == "menu") {
     let treeList = menuOptions.value;
     for (let i = 0; i < treeList.length; i++) {
       menuRef.value.store.nodesMap[treeList[i].id].expanded = value;
     }
   } else if (type == "dept") {
     let treeList = deptOptions.value;
     for (let i = 0; i < treeList.length; i++) {
       deptRef.value.store.nodesMap[treeList[i].id].expanded = value;
     }
   }
 }
 /** 树权限（全选/全不选） */
 function handleCheckedTreeNodeAll(value, type) {
   if (type == "menu") {
     menuRef.value.setCheckedNodes(value ? menuOptions.value : []);
   } else if (type == "dept") {
     deptRef.value.setCheckedNodes(value ? deptOptions.value : []);
   }
 }
 /** 树权限（父子联动） */
 function handleCheckedTreeConnect(value, type) {
   if (type == "menu") {
     form.value.menuCheckStrictly = value ? true : false;
   } else if (type == "dept") {
     form.value.deptCheckStrictly = value ? true : false;
   }
 }
 /** 所有菜单节点数据 */
 function getMenuAllCheckedKeys() {
   // 目前被选中的菜单节点
   let checkedKeys = menuRef.value.getCheckedKeys();
   // 半选中的菜单节点
   let halfCheckedKeys = menuRef.value.getHalfCheckedKeys();
   checkedKeys.unshift.apply(checkedKeys, halfCheckedKeys);
   return checkedKeys;
 }
 /** 提交按钮 */
 function submitForm() {
   proxy.$refs["roleRef"].validate(valid => {
     if (valid) {
       if (form.value.roleId != undefined) {
         form.value.menuIds = getMenuAllCheckedKeys();
         updateRole(form.value).then(response => {
           proxy.$modal.msgSuccess("修改成功");
           open.value = false;
           getList();
         });
       } else {
         form.value.menuIds = getMenuAllCheckedKeys();
         addRole(form.value).then(response => {
           proxy.$modal.msgSuccess("新增成功");
           open.value = false;
           getList();
         });
       }
     }
   });
 }
 /** 取消按钮 */
 function cancel() {
   open.value = false;
   reset();
 }
 /** 选择角色权限范围触发 */
 function dataScopeSelectChange(value) {
   if (value !== "2") {
     deptRef.value.setCheckedKeys([]);
   }
 }
 /** 分配数据权限操作 */
 function handleDataScope(row) {
   reset();
   const deptTreeSelect = getDeptTree(row.roleId);
   getRole(row.roleId).then(response => {
     form.value = response.data;
     openDataScope.value = true;
     nextTick(() => {
       deptTreeSelect.then(res => {
         nextTick(() => {
           if (deptRef.value) {
             deptRef.value.setCheckedKeys(res.checkedKeys);
           }
         });
       });
     });
     title.value = "分配数据权限";
   });
 }
 /** 提交按钮（数据权限） */
 function submitDataScope() {
   if (form.value.roleId != undefined) {
     form.value.deptIds = getDeptAllCheckedKeys();
     dataScope(form.value).then(response => {
       proxy.$modal.msgSuccess("修改成功");
       openDataScope.value = false;
       getList();
     });
   }
 }
 /** 取消按钮（数据权限）*/
 function cancelDataScope() {
   openDataScope.value = false;
   reset();
 }
 
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
        flex: 1; /* 使表单可以伸缩占据剩余空间 */
        overflow-y: auto; /*  表单内容可以滚动 */
        padding: 20px;
    }
</style>
 
 