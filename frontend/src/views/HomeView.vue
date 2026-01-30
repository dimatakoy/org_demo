<script lang="ts" setup>
import { getDepartmentEmployees, getDepartments } from '@/shared/api/client'
import type { components } from '@/shared/api/schema'
import { useQuery } from '@tanstack/vue-query'
import { Tree } from 'primevue'
import { type TreeNode } from 'primevue/treenode'
import { computed, ref, shallowRef, watchEffect } from 'vue'

const departmentsQuery = useQuery({
  queryKey: ['departments'],
  queryFn: getDepartments,
})

const activeDepartment = ref<string | null>(null)
const activeNode = shallowRef<TreeNode | null>(null)

const departmentEmployeesQuery = useQuery({
  queryKey: ['department-employee', activeDepartment],
  async queryFn() {
    return getDepartmentEmployees({
      departmentId: activeDepartment.value,
      limit: 100_000,
    })
  },
  staleTime: Number.POSITIVE_INFINITY,
  enabled: () => activeDepartment.value !== null,
})

type Department = components['schemas']['DepartmentSchema']
const mapDepartmentToNode = (dept: Department): TreeNode => {
  return {
    key: String(dept.id),
    label: dept.title,
    data: {
      type: 'department',
      department: dept,
    },
    icon: 'pi pi-building',
    children: dept.children.map(mapDepartmentToNode),
    loading: true,
  }
}

type Employee = components['schemas']['EmployeeSchema']
function mapEmployeeToNode(employee: Employee) {
  return {
    key: `emp-${employee.id}`,
    label: `${employee.first_name} ${employee.last_name} ${employee.middle_name ?? ''}`,
    icon: 'pi pi-user',
    data: { type: 'employee', employee },
    leaf: true,
  }
}

const departments = computed(() => {
  if (departmentsQuery.isFetching.value) {
    return []
  }

  const items: TreeNode[] = departmentsQuery.data.value.items.map((department) => {
    return mapDepartmentToNode(department)
  })

  return items
})

async function onNodeExpand(node: TreeNode) {
  activeDepartment.value = node.key
  activeNode.value = node
  activeNode.value.loading = true
}

watchEffect(() => {
  if (departmentEmployeesQuery.isFetching.value) return
  if (activeNode.value === null) return

  if (departmentEmployeesQuery.data.value) {
    activeNode.value.children = [
      ...activeNode.value.children?.filter((child) => child.data.type === 'department'),
      ...departmentEmployeesQuery.data.value.items.map((e) => mapEmployeeToNode(e)),
    ]

    activeNode.value.loading = false
  }
})
</script>

<template>
  <Tree
    class="tree"
    :value="departments"
    @node-expand="onNodeExpand"
    selectionMode="multiple"
  ></Tree>
</template>

<style scoped>
.tree {
  font-family: system-ui, sans-serif;
}
</style>
