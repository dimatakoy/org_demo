<script lang="ts" setup>
import { getDepartmentEmployees, getDepartments } from '@/shared/api/client'
import type { components } from '@/shared/api/schema'
import { useQuery, useQueryClient } from '@tanstack/vue-query'
import { computed, ref, useTemplateRef, watchEffect } from 'vue'

import { BaseTree } from '@he-tree/vue'
import '@he-tree/vue/style/default.css'
import '@he-tree/vue/style/material-design.css'

const departmentsQuery = useQuery({
  queryKey: ['departments'],
  queryFn: getDepartments,
})

const client = useQueryClient()

const activeDepartment = ref(null)
const activeDepartmentId = computed(() => activeDepartment.value?.data.id)

const departmentEmployeesQuery = useQuery({
  queryKey: ['department-employees', activeDepartmentId],
  queryFn: async () => {
    const data = await getDepartmentEmployees({
      departmentId: activeDepartmentId.value,
      limit: 10_000,
    })

    return data
  },
  enabled: () => activeDepartment.value !== null,
})

type Department = components['schemas']['DepartmentSchema']
function mapItemToNode(item: Department) {
  return {
    id: item.id,
    text: item.title,
    children: item.children.map(mapItemToNode),
    type: 'department',
  }
}

const treeData = computed(() => {
  if (departmentsQuery.data.value) {
    return departmentsQuery.data.value.items.map(mapItemToNode)
  }

  return []
})

function onClickNode(node: any) {
  activeDepartment.value = node
}

const treeRef = useTemplateRef('tree')

watchEffect(() => {
  if (!activeDepartment.value) {
    return
  }

  if (departmentEmployeesQuery.data.value) {
    if (activeDepartment.value.employeesLoaded) return

    treeRef.value?.addMulti(
      departmentEmployeesQuery.data.value.items.map((e) => {
        return {
          id: e.id,
          text: `${e.last_name} ${e.first_name} ${e.middle_name ?? ''}`,
          children: [],
          type: 'employee',
        }
      }),
      activeDepartment.value,
    )

    activeDepartment.value.employeesLoaded = true
  }
})
</script>

<template>
  <BaseTree
    v-model="treeData"
    ref="tree"
    :virtualization="true"
    :default-open="false"
    @click:node="onClickNode"
  >
    <template #default="{ node, stat }">
      <button @click="stat.open = !stat.open" :disabled="node.children.length === 0">
        {{ stat.open ? '-' : '+' }}
      </button>

      {{ node.type === 'department' ? '🏢' : '🙋‍♂️' }}

      {{ node.text }}

      <strong
        >{{
          departmentEmployeesQuery.isFetching.value && activeDepartment.data.id === node.id
            ? 'Loading...'
            : ''
        }}
      </strong>
    </template>
  </BaseTree>
</template>

<style scoped>
.tree {
  font-family: system-ui, sans-serif;
}
</style>
