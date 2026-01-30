import createClient from 'openapi-fetch'
import type { paths } from './schema'

const client = createClient<paths>({ baseUrl: import.meta.env['VITE_BACKEND_BASE_URL'] })

export async function getDepartments(options: { limit: number; offset: number }) {
  const { data, error } = await client.GET('/api/v1/departments/', {
    params: {
      query: {
        limit: options.limit,
        offset: options.offset,
      },
    },
  })

  if (error) {
    console.error(error)

    // TODO: add proper error handling
    return {
      items: [],
      count: 0,
    }
  }

  return data
}

export async function getDepartmentEmployees(options: {
  departmentId: number | string
  limit: number
  offset: number
}) {
  const { data, error } = await client.GET('/api/v1/departments/{department_id}/employees', {
    params: {
      path: {
        department_id: options.departmentId,
      },
      query: {
        limit: options.limit,
        offset: options.offset,
      },
    },
  })

  if (error) {
    console.error(error)

    return {
      items: [],
      count: 0,
    }
  }

  return data
}
